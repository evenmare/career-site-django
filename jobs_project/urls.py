"""jobs_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from job_app.views import MainView, VacanciesView, CompanyView, SpecializedVacanciesView, \
    VacancyView, CompanyLetsStartView, CompanyEditView, CompanyCreateView, CompanyVacanciesView, \
    CompanyVacancyCreateView, error404_view, error500_view, CompanyVacancyEditView, ResumeCreateView, ResumeEditView
from authentifiaction_app.views import SignupView, UserLoginView

handler404 = error404_view
handler500 = error500_view

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', SignupView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mycompany/letsstart/', login_required(CompanyLetsStartView.as_view()), name='company_letsstart'),
    path('mycompany/create/', login_required(CompanyCreateView.as_view()), name='company_create'),
    path('mycompany/', login_required(CompanyEditView.as_view()), name='company_edit'),
    path('mycompany/vacancies', login_required(CompanyVacanciesView.as_view()), name='company_vacancies'),
    path('mycompany/vacancies/create', login_required(CompanyVacancyCreateView.as_view()), name='company_vacancy_create'),
    path('mycompany/vacancies/<int:pk>', login_required(CompanyVacancyEditView.as_view()), name='company_vacancy_edit'),
    path('myresume/create', login_required(ResumeCreateView.as_view()), name='resume_create'),
    path('myresume/', login_required(ResumeEditView.as_view()), name='resume_edit'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', SpecializedVacanciesView.as_view(), name='categorized_vacancies'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)