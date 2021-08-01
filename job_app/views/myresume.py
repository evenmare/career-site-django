from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DeleteView, TemplateView, UpdateView, CreateView

from job_app.forms import ResumeForm
from job_app.models import Vacancy, Company, Resume


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


class ResumeDeleteView(DeleteView):
    model = Resume
    template_name = 'job_app/model-delete.html'
    success_url = '/myresume/letsstart'

    def get_object(self, queryset=None):
        return Resume.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            Resume.objects.get(user=self.request.user)
        except Resume.DoesNotExist:
            return redirect('/myresume/letsstart')

        return super().dispatch(request, *args, **kwargs)


class ResumeLetsStartView(TemplateView):
    template_name = 'job_app/myresume/resume-create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Resume.objects.get(user=self.request.user)
            return redirect('/myresume')
        except Resume.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)


class ResumeEditView(SuccessMessageMixin, UpdateView):
    success_message = 'Резюме обновлено!'
    template_name = 'job_app/myresume/resume-edit.html'
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
    template_name = 'job_app/myresume/resume-edit.html'
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
