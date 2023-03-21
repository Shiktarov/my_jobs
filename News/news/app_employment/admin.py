from django.contrib import admin
from app_employment.models import Vacancy, Resume

class VacancyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

admin.site.register(Vacancy, VacancyAdmin)

class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

admin.site.register(Resume, ResumeAdmin)
