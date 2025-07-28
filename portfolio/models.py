from django.db import models
from datetime import datetime, date


class Experience(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    role_type = models.CharField(max_length=50, blank=True)
    responsibilities = models.TextField(blank=True, help_text="Enter bullet points separated by newline")


    def __str__(self):
        return f"{self.title} @ {self.company_name}"

    def formatted_dates(self):
        def to_date(value):
            if isinstance(value, str):
                for fmt in ("%b %Y", "%b-%Y", "%Y-%m-%d"):
                    try:
                        return datetime.strptime(value.strip(), fmt).date()
                    except:
                        continue
            return value

        start = to_date(self.start_date)
        end = to_date(self.end_date)

        if isinstance(start, (datetime, date)) and isinstance(end, (datetime, date)):
            return f"{start.strftime('%b %Y')} – {end.strftime('%b %Y')}"
        elif isinstance(start, (datetime, date)):
            return f"{start.strftime('%b %Y')} – Present"
        else:
            return f"{self.start_date} – {self.end_date}"


class Education(models.Model):
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    activities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

    def formatted_dates(self):
        def to_date(value):
            if isinstance(value, str):
                for fmt in ("%b %Y", "%b-%Y", "%Y-%m-%d"):
                    try:
                        return datetime.strptime(value.strip(), fmt).date()
                    except:
                        continue
            return value

        start = to_date(self.start_date)
        end = to_date(self.end_date)

        if isinstance(start, (datetime, date)) and isinstance(end, (datetime, date)):
            return f"{start.strftime('%b %Y')} – {end.strftime('%b %Y')}"
        else:
            return f"{self.start_date} – {self.end_date}"




class Certification(models.Model):
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField(blank=True, null=True)  # ✅ Now optional  # Use actual DateField instead of CharField
    expiration_date = models.DateField(blank=True, null=True)  # Optional
    certificate_url = models.URLField(blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of skills")
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)  # for media

    def __str__(self):
        return f"{self.title} by {self.issuer}"



class Recommendation(models.Model):
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    current_company = models.CharField(max_length=255)
    
    
    relationship = models.CharField(max_length=100, blank=True)

    text = models.TextField()
    date = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='recommendations/', blank=True, null=True)

    def __str__(self):
        return f"Recommendation by {self.full_name}"


class About(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    birthday = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    degree = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField()
    freelance = models.CharField(max_length=50,blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/')

    def __str__(self):
        return self.name

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )



class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(help_text="Enter a number between 0 to 100")

    def __str__(self):
        return f"{self.name} - {self.level}%"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/')
    link = models.URLField()

    def __str__(self):
        return self.title
