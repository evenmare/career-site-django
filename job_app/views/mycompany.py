from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import UpdateView, CreateView, TemplateView, ListView, DeleteView

from job_app.forms import CompanyVacancyForm, CompanyInfoForm
from job_app.models import Vacancy, Application, Company
from jobs_project.settings import CARDS_ON_PAGE


class CompanyVacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'job_app/model-delete.html'
    success_url = '/mycompany/vacancies'

    def dispatch(self, request, *args, **kwargs):
        try:
            Vacancy.objects.filter(company=Company.objects.filter(owner=self.request.user))
        except (Company.DoesNotExist, Vacancy.DoesNotExist):
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class CompanyVacancyEditView(SuccessMessageMixin, UpdateView):
    success_message = 'Вакансия обновлена'
    model = Vacancy
    form_class = CompanyVacancyForm
    template_name = 'job_app/mycompany/vacancy-edit.html'

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
        elif company_vacancy.salary_min < 0 or company_vacancy.salary_max < 0:
            form.add_error(field='salary_min', error='Зарплата не может быть отрицательной!')
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
    template_name = 'job_app/mycompany/vacancy-edit.html'

    def form_valid(self, form):
        company_vacancy = form.save(commit=False)
        company_vacancy.company = Company.objects.get(owner=self.request.user)
        if company_vacancy.salary_min > company_vacancy.salary_max:
            form.add_error(field='salary_max', error='Максимальная зарплата должна быть больше минимальной!')
            return super().form_invalid(form)
        elif company_vacancy.salary_min < 0 or company_vacancy.salary_max < 0:
            form.add_error(field='salary_min', error='Зарплата не может быть отрицательной!')
            return super().form_invalid(form)
        else:
            company_vacancy.save()
            return super().form_valid(form)

    def get_success_url(self):
        output_vacancy = (Vacancy.objects
                          .filter(company=Company.objects.get(owner=self.request.user))
                          .order_by('-id').first())

        return f'/mycompany/vacancies/{output_vacancy.id}'


class CompanyVacanciesView(ListView):
    paginate_by = CARDS_ON_PAGE
    model = Vacancy
    template_name = 'job_app/mycompany/vacancy-list.html'

    def get_queryset(self):
        company_vacancies = (self.model.objects
                             .filter(company=self.request.user.company)
                             .order_by('-published_at'))

        return company_vacancies

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            return redirect('/mycompany/letsstart')

        return super().dispatch(request, *args, **kwargs)


class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'job_app/model-delete.html'
    success_url = '/mycompany/letsstart'

    def get_object(self, queryset=None):
        return Company.objects.get(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Company.DoesNotExist:
            return redirect('/mycompany/letsstart')

        return super().dispatch(request, *args, **kwargs)


class CompanyCreateView(SuccessMessageMixin, CreateView):
    success_message = 'Компания создана!'
    model = Company
    form_class = CompanyInfoForm
    success_url = '/mycompany'
    template_name = 'job_app/mycompany/company-edit.html'

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
    template_name = 'job_app/mycompany/company-edit.html'

    def get_object(self, queryset=None):
        return Company.objects.get(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            return redirect('/mycompany/letsstart')

        return super().dispatch(request, *args, **kwargs)


class CompanyLetsStartView(TemplateView):
    template_name = 'job_app/mycompany/company-create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=self.request.user)
            return redirect('/mycompany/')
        except Company.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)
