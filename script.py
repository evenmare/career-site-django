import os
import django
import random
import job_app.data as data
from job_app.models import Vacancy, Company, Specialty

os.environ['DJANGO_SETTINGS_MODULE'] = 'jobs_project.settings'
django.setup()

if __name__ == '__main__':

    for company in data.companies:
        Company.objects.create(
            name=company['title'],
            location=company['location'],
            description=company['description'],
            employee_count=int(company['employee_count']),
        )

    for specialty in data.specialties:
        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )

    for i in range(105):
        Vacancy.objects.create(
            title=random.choice(data.jobs),
            specialty=Specialty.objects.get(code=random.choice(data.specialties)['code']),
            company=Company.objects.get(id=random.choice(data.companies)['id']),
            skills=', '.join([str(elem) for elem in random.sample(data.skills, 3)]),
            text=random.choice(data.descriptions),
            salary_min=random.randint(20, 60) * 1000,
            salary_max=random.randint(65, 300) * 1000,
        )
