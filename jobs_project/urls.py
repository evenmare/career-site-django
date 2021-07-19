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
from django.urls import path
from job_app.views import MainView, VacanciesView, CompanyView, SpecializedVacanciesView, \
    VacancyView, error404_view, error500_view

handler404 = error404_view
handler500 = error500_view

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', SpecializedVacanciesView.as_view(), name='categorized_vacancies'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
]
