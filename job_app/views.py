from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound, HttpResponseServerError, Http404
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from job_app.models import Company, Specialty, Vacancy, Application, Resume
from jobs_project.settings import CARDS_ON_PAGE
from .forms import CompanyInfoForm, CompanyVacancyForm, ApplicationForm, ResumeForm


def error404_view(request: HttpRequest, exception=None):
    return HttpResponseNotFound("""<h1>Error 404</h1><p>Page Not Found</p><a href="/">На главную</a>""")


def error500_view(request: HttpRequest, exception=None):
    return HttpResponseServerError("""<h1>Error 500</h1><a href="/">На главную</a><p>That's a crap</p>""")


class ResumeLetsStartView(TemplateView):
    template_name = 'job_app/resume-create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Resume.objects.get(user=self.request.user)
            return redirect('/myresume/')
        except Resume.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class ResumeEditView(SuccessMessageMixin, UpdateView):
    success_message = 'Резюме обновлено!'
    template_name = 'job_app/resume-edit.html'
    model = Resume
    form_class = ResumeForm
    success_url = '/myresume'

    def get_object(self, queryset=None):
        return Resume.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            Resume.objects.get(user=self.request.user)
        except Resume.DoesNotExist:
            return redirect('/myresume/letsstart')

        return super().dispatch(request, *args, **kwargs)


class ResumeCreateView(SuccessMessageMixin, CreateView):
    success_message = 'Резюме создано!'
    template_name = 'job_app/resume-edit.html'
    model = Resume
    form_class = ResumeForm
    success_url = '/myresume'

    def form_valid(self, form):
        input_resume = form.save(commit=False)
        input_resume.user = self.request.user
        input_resume.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            Resume.objects.get(user=self.request.user)
            return redirect('/myresume')
        except Resume.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


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


class CompanyVacancyEditView(SuccessMessageMixin, UpdateView):
    success_message = 'Вакансия обновлена'
    model = Vacancy
    form_class = CompanyVacancyForm
    template_name = 'job_app/vacancy-edit.html'

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(CompanyVacancyEditView, self).get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(
            vacancy=Vacancy.objects.get(id=self.kwargs['pk']))

        return context

    def form_valid(self, form):
        company_vacancy = form.save(commit=False)
        if company_vacancy.salary_min > company_vacancy.salary_max:
            form.add_error(field='salary_max', error='Максимальная зарплата должна быть больше минимальной!')
            return super().form_invalid(form)
        else:
            company_vacancy.save()
            return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            Vacancy.objects.filter(company=Company.objects.filter(owner=self.request.user))
        except (Company.DoesNotExist, Vacancy.DoesNotExist):
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class CompanyVacancyCreateView(SuccessMessageMixin, CreateView):
    success_message = 'Вакансия создана'
    model = Vacancy
    form_class = CompanyVacancyForm
    success_url = '/'
    template_name = 'job_app/vacancy-edit.html'

    def form_valid(self, form):
        company_vacancy = form.save(commit=False)
        company_vacancy.company = Company.objects.get(owner=self.request.user)
        if company_vacancy.salary_min > company_vacancy.salary_max:
            form.add_error(field='salary_max', error='Максимальная зарплата должна быть больше минимальной!')
            return super().form_invalid(form)
        else:
            company_vacancy.save()
            return super().form_valid(form)


class CompanyVacanciesView(ListView):
    paginate_by = CARDS_ON_PAGE
    model = Vacancy
    template_name = 'job_app/vacancy-list.html'

    def get_queryset(self):
        company_vacancies = (self.model.objects
                             .filter(company=self.request.user.company)
                             .order_by('-published_at'))

        return company_vacancies


class CompanyCreateView(SuccessMessageMixin, CreateView):
    success_message = 'Компания создана!'
    model = Company
    form_class = CompanyInfoForm
    success_url = '/mycompany'
    template_name = 'job_app/company-edit.html'

    def form_valid(self, form):
        user_company = form.save(commit=False)
        user_company.owner = self.request.user
        user_company.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=self.request.user)
            return redirect('/mycompany/')
        except Company.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class CompanyEditView(SuccessMessageMixin, UpdateView):
    success_message = 'Информация о компании обновлена'
    model = Company
    form_class = CompanyInfoForm
    success_url = '/mycompany'
    template_name = 'job_app/company-edit.html'

    def get_object(self, queryset=None):
        return Company.objects.get(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            return redirect('/mycompany/letsstart')

        return super().dispatch(request, *args, **kwargs)


class CompanyLetsStartView(TemplateView):
    template_name = 'job_app/company-create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=self.request.user)
            return redirect('/mycompany/')
        except Company.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class MainView(TemplateView):
    template_name = 'job_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = (
            Specialty.objects
                .annotate(vacancies_count=Count('vacancies'))
                .filter(vacancies_count__gt=0)
                .order_by('-vacancies_count')[:8]
        )
        context['companies'] = (
            Company.objects
                .annotate(vacancies_count=Count('vacancies'))
                .filter(vacancies_count__gt=0)
                .order_by('-vacancies_count')[:8]
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
        return Vacancy.objects \
            .filter(specialty=category) \
            .order_by('-published_at')

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
        return Vacancy.objects.filter(company=company)

    def get_context_data(self, *, object_list=None, **kwargs):
        company = Company.objects.get(id=self.kwargs['company_id'])
        context = super(CompanyView, self).get_context_data(**kwargs)
        context['company_location'] = company.location
        context['company_name'] = company.name
        context['company_logo'] = company.logo
        return context
