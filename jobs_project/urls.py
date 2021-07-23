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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from job_app.views import MainView, VacanciesView, CompanyView, SpecializedVacanciesView, \
    VacancyView, CompanyLetsStart, CompanyEdit, CompanyCreate, CompanyVacancies, \
    CompanyVacancyCreate, error404_view, error500_view, CompanyVacancyEdit
from authentifiaction_app.views import SignupView, UserLoginView

handler404 = error404_view
handler500 = error500_view

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', SignupView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mycompany/letsstart/', CompanyLetsStart.as_view(), name='company_letsstart'),
    path('mycompany/create/', CompanyCreate.as_view(), name='company_create'),
    path('mycompany/', CompanyEdit.as_view(), name='company_edit'),
    path('mycompany/vacancies', CompanyVacancies.as_view(), name='company_vacancies'),
    path('mycompany/vacancies/create', CompanyVacancyCreate.as_view(), name='company_vacancy_create'),
    path('mycompany/vacancies/<int:pk>', CompanyVacancyEdit.as_view(), name='company_vacancy_edit'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', SpecializedVacanciesView.as_view(), name='categorized_vacancies'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)