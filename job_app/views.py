from django.http import HttpRequest, HttpResponseNotFound, HttpResponseServerError
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import get_object_or_404
from job_app.models import Company, Specialty, Vacancy
from job_app.data import cards_on_page


def error404_view(request: HttpRequest, exception=None):
    return HttpResponseNotFound("""<h1>Error 404</h1><p>Page Not Found</p><a href="/">На главную</a>""")


def error500_view(request: HttpRequest, exception=None):
    return HttpResponseServerError("""<h1>Error 500</h1><a href="/">На главную</a><p>That's a crap</p>""")


class MainView(TemplateView):
    template_name = 'job_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects \
            .annotate(vacancies_count=Count('vacancies')) \
            .filter(vacancies_count__gt=0) \
            .order_by('-vacancies_count')[:8]
        context['companies'] = Company.objects \
            .annotate(vacancies_count=Count('vacancies')) \
            .filter(vacancies_count__gt=0) \
            .order_by('-vacancies_count')[:8]
        return context


class VacanciesView(ListView):
    paginate_by = cards_on_page
    model = Vacancy
    template_name = 'job_app/vacancies.html'
    queryset = model.objects.order_by('-published_at')


class SpecializedVacanciesView(ListView):
    paginate_by = cards_on_page
    model = Vacancy
    template_name = 'job_app/vacancies.html'

    def get_queryset(self):
        category = get_object_or_404(
            Specialty.objects.filter(code=self.kwargs['category']))
        return Vacancy.objects\
            .filter(specialty=category)\
            .order_by('-published_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecializedVacanciesView, self).get_context_data(**kwargs)
        context['title'] = Specialty.objects.get(code=self.kwargs['category']).title
        return context


class VacancyView(DetailView):
    template_name = 'job_app/vacancy.html'
    model = Vacancy


class CompanyView(ListView):
    paginate_by = cards_on_page
    model = Vacancy
    template_name = 'job_app/company.html'

    def get_queryset(self):
        company = get_object_or_404(
            Company.objects.filter(id=self.kwargs['company_id']))
        return Vacancy.objects.filter(company=company)

    def get_context_data(self, *, object_list=None, **kwargs):
        company = Company.objects.get(id=self.kwargs['company_id'])
        context = super(CompanyView, self).get_context_data(**kwargs)
        context['company_location'] = company.location
        context['company_name'] = company.name
        context['company_logo'] = company.logo
        return context
