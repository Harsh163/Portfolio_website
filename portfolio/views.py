import zipfile, os
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Experience, Education, Certification, Recommendation, About, Skill,Project
import csv
from datetime import datetime


def index(request):
    experiences = Experience.objects.all().order_by('-start_date')
    educations = Education.objects.all().order_by('-start_date')
    certifications = Certification.objects.all().order_by('id')
    recommendations = Recommendation.objects.all()
    about = About.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()

        # 💡 Preprocess skills into a list
    for cert in certifications:
        cert.skills_list = [s.strip() for s in cert.skills.split(',')] if cert.skills else []

    context = {
        'experiences': experiences,
        'educations': educations,
        'certifications': certifications,
        'recommendations': recommendations,
        'about': about,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'portfolio/index.html', context)


def inner_page(request):
    return render(request, 'portfolio/inner-page.html')


def portfolio_details(request):
    return render(request, 'portfolio/portfolio-details.html')


def is_harsh(user):
    return user.is_superuser and user.username.lower() == 'harsh'


@user_passes_test(is_harsh)
def upload_linkedin_zip(request):
    if request.method == 'POST' and request.FILES.get('linkedin_zip'):
        uploaded_file = request.FILES['linkedin_zip']
        zip_path = default_storage.save('linkedin_data.zip', uploaded_file)
        zip_full_path = os.path.join(settings.MEDIA_ROOT, zip_path)

        extract_dir = os.path.join(settings.MEDIA_ROOT, 'linkedin_data')
        with zipfile.ZipFile(zip_full_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        def load_csv(file, callback):
            file_path = Path(extract_dir) / file
            if file_path.exists():
                with open(file_path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        callback(row)

        def parse_date_safe(date_str):
            if not date_str or date_str.strip() == '':
                return None
            for fmt in ('%b-%y', '%Y-%m-%d', '%b-%Y', '%b %Y', '%Y'):  # ✅ Added '%Y' here
                try:
                    return datetime.strptime(date_str.strip(), fmt).date()
                except:
                    continue
            return None

        def process_experience(row):
            start_date = parse_date_safe(row.get('Started On'))
            end_date = parse_date_safe(row.get('Finished On'))

            if not start_date:
                print(f"⚠️ Skipping experience (no start date): {row}")
                return

            title = row.get('Title', '').strip()
            company = row.get('Company Name', '').strip()
            location = row.get('Location', '').strip()
            description = row.get('Description', '').strip()

            role_type = ''
            if 'intern' in title.lower():
                role_type = 'Internship'
            elif start_date and start_date.month <= 4 and start_date.year == 2022:
                role_type = 'Internship'
            else:
                role_type = 'Full-time'

            Experience.objects.get_or_create(
                title=title,
                company_name=company,
                start_date=start_date,
                end_date=end_date,
                defaults=dict(
                    location=location,
                    description=description,
                    role_type=role_type
                )
            )

        def process_education(row):
            start_date = parse_date_safe(row.get('Start Date'))
            end_date = parse_date_safe(row.get('End Date'))

            if not start_date or not end_date:
                print(f"⚠️ Skipping education row with bad date: {row}")
                return

            institution = row.get('School Name', '').strip()
            degree = row.get('Degree Name', '').strip()
            notes = row.get('Notes', '').strip()
            activities = row.get('Activities and Societies', '').strip()

            obj, created = Education.objects.get_or_create(
                institution=institution,
                degree=degree,
                start_date=start_date,
                end_date=end_date,
                defaults={
                    'description': notes,
                    'activities': activities
                }
            )
            print(f"{'✅ Created' if created else '🔁 Exists'}: {degree} at {institution} ({start_date} – {end_date})")

        def process_certification(row):
            Certification.objects.update_or_create(
                title=row['Name'].strip(), 
                issuer=row['Authority'].strip(),
                defaults=dict(
                    issue_date=parse_date_safe(row['Started On']),  # ✅ fixed
                    certificate_url=row.get('Url', '').strip(),
                    license_number=row.get('License Number', '').strip()
                )
            )


        def process_recommendation(row):
            Recommendation.objects.update_or_create(
                full_name=(row['First Name'] + ' ' + row['Last Name']).strip(),
                job_title=row['Job Title'].strip(),
                current_company=row['Company'].strip(),
                defaults=dict(
                    text=row['Text'].strip(),
                    date=row['Creation Date']
                )
            )

        load_csv('Positions.csv', process_experience)
        load_csv('Education.csv', process_education)
        load_csv('Certifications.csv', process_certification)
        load_csv('Recommendations_Received.csv', process_recommendation)

        return redirect('home')

    return render(request, 'portfolio/upload_linkedin.html')
