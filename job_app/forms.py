from django import forms
from .models import Company, Vacancy, Specialty, Application, Resume
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button


class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary',
                  'specialty', 'grade', 'education', 'experience', 'portfolio')
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'status': 'Готовность к работе',
            'salary': 'Ожидаемое вознаграждение',
            'specialty': 'Специализация',
            'grade': 'Квалификация',
            'education': 'Образование',
            'experience': 'Опыт работы',
            'portfolio': 'Ссылка на портфолио',
        }

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('surname'),
            ),
            Row(
                Column('status'),
                Column('salary'),
            ),
            Row(
                Column('specialty'),
                Column('grade'),
            ),
            'education',
            'experience',
            'portfolio',
            Submit('submit', 'Отправить', css_class='btn btn-primary btn-block'),
        )


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        widgets = {
            'written_cover_letter': forms.Textarea(
                attrs={
                    'rows': '8',
                },
            ),
        }
        labels = {
            'written_username': 'Вас зовут',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'card mt-3 mb-3 card-body mx-3'
        self.helper.layout = Layout(
            'written_username',
            'written_phone',
            'written_cover_letter',
            Submit('submit', 'Отправить'),
        )


class CompanyVacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills',
                  'salary_min', 'salary_max', 'text',)
        widgets = {
            'specialty': forms.Select(
                choices=(specialty for specialty in Specialty.objects.all()),
                attrs={
                    'class': 'custom-select mr-sm-2',
                }
            ),
        }
        labels = {
            'title': 'Название вакансии',
            'specialty': 'Специализация',
            'salary_min': 'Зарплата от, Р',
            'salary_max': 'Зарплата до, Р',
            'skills': 'Требуемые навыки',
            'text': 'Описание вакансии',
        }

    def __init__(self, *args, **kwargs):
        super(CompanyVacancyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('specialty'),
            ),
            Row(
                Column('salary_min'),
                Column('salary_max'),
            ),
            'skills',
            'text',
            Submit('submit', 'Сохранить', css_class='btn btn-primary btn-block')
        )


class CompanyInfoForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')
        widgets = {
            'logo': forms.FileInput(),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4',
                }
            ),
        }

        labels = {
            'name': 'Название компании',
            'logo': 'Логотип',
            'employee_count': 'Количество человек в компании',
            'location': 'География',
            'description': ' Информация о компании',
        }
