from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Experience, Education, Certification, Recommendation, About, Skill, Project

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Recommendation)
admin.site.register(About)
admin.site.register(Skill)
admin.site.register(Project)

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date']
    search_fields = ['title', 'issuer', 'skills']