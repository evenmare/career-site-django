from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, CreateView

from job_app.forms import ApplicationForm
from job_app.models import Vacancy, Specialty, Company, Application, Resume
from jobs_project.settings import CARDS_ON_PAGE


def error404_view(request: HttpRequest, exception=None):
    return HttpResponseNotFound("""<h1>Error 404</h1><p>Page Not Found</p><a href="/">На главную</a>""")


def error500_view(request: HttpRequest, exception=None):
    return HttpResponseServerError("""<h1>Error 500</h1><a href="/">На главную</a><p>That's a crap</p>""")


class ProfileView(TemplateView):
    template_name = 'job_app/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User.objects.filter(username=self.kwargs['username']))
        context['resume'] = get_object_or_404(Resume.objects.filter(user=user))

        return context


class SearchView(ListView):
    template_name = 'job_app/search.html'
    paginate_by = CARDS_ON_PAGE
    model = Vacancy

    def get_queryset(self):
        search_field_text = self.request.GET.get('search_field')
        if not search_field_text:
            search_field_text = ''
        return (Vacancy.objects
                .filter(Q(title__icontains=search_field_text) |
                        Q(specialty__code__icontains=search_field_text) |
                        Q(specialty__title__icontains=search_field_text) |
                        Q(skills__icontains=search_field_text))
                .order_by('-published_at').all())


class VacancyView(SuccessMessageMixin, CreateView):
    success_message = 'Отклик отправлен!'
    template_name = 'job_app/vacancy.html'
    model = Application
    form_class = ApplicationForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy = get_object_or_404(Vacancy.objects.filter(id=self.kwargs['pk']))
        context['vacancy'] = vacancy

        return context

    def form_valid(self, form):
        input_application = form.save(commit=False)
        input_application.vacancy = Vacancy.objects.get(id=self.kwargs['pk'])
        input_application.user = self.request.user
        input_application.save()

        return super().form_valid(form)


class MainView(TemplateView):
    template_name = 'job_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = (
            Specialty.objects
                     .annotate(vacancies_count=Count('vacancies'))
                     .filter(vacancies_count__gt=0)
                     .order_by('-vacancies_count')
        )
        context['companies'] = (
            Company.objects
                   .annotate(vacancies_count=Count('vacancies'))
                   .filter(vacancies_count__gt=0)
                   .order_by('-vacancies_count')
        )

        return context


class VacanciesView(ListView):
    paginate_by = CARDS_ON_PAGE
    model = Vacancy
    template_name = 'job_app/vacancies.html'
    queryset = model.objects.order_by('-published_at')


class SpecializedVacanciesView(ListView):
    paginate_by = CARDS_ON_PAGE
    model = Vacancy
    template_name = 'job_app/vacancies.html'

    def get_queryset(self):
        category = get_object_or_404(
            Specialty.objects.filter(code=self.kwargs['category']))
        return (Vacancy.objects
                       .filter(specialty=category)
                       .order_by('-published_at'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecializedVacanciesView, self).get_context_data(**kwargs)
        context['title'] = Specialty.objects.get(code=self.kwargs['category']).title
        return context


class CompanyView(ListView):
    paginate_by = CARDS_ON_PAGE
    model = Vacancy
    template_name = 'job_app/company.html'

    def get_queryset(self):
        company = get_object_or_404(
            Company.objects.filter(id=self.kwargs['company_id']))
        return Vacancy.objects.filter(company=company).order_by('-published_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        company = Company.objects.get(id=self.kwargs['company_id'])
        context = super(CompanyView, self).get_context_data(**kwargs)
        context['company_location'] = company.location
        context['company_name'] = company.name
        context['company_logo'] = company.logo
        return context
