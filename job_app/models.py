from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()

    def __str__(self):
        return f'{ self.id } { self.name }'


class Specialty(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return f'{ self.id } { self.code } { self.title }'


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=300)
    text = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{ self.id } { self.title } { self.company } { self.specialty }'
