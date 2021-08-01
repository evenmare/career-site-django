from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LogoutView

from authentifiaction_app.views import SignupView, UserLoginView
from job_app.views import public, myresume, mycompany

handler404 = public.error404_view
handler500 = public.error500_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', SignupView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', public.MainView.as_view(), name='home'),
    path('vacancies/', public.VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', public.SpecializedVacanciesView.as_view(), name='categorized_vacancies'),
    path('vacancies/<int:pk>/', public.VacancyView.as_view(), name='vacancy'),
    path('companies/<int:company_id>/', public.CompanyView.as_view(), name='company'),
    path('search/', public.SearchView.as_view(), name='search'),
    path('profile/<str:username>/', public.ProfileView.as_view(), name='profile'),

    path('mycompany/letsstart/', login_required(mycompany.CompanyLetsStartView.as_view()), name='company_letsstart'),
    path('mycompany/create/', login_required(mycompany.CompanyCreateView.as_view()), name='company_create'),
    path('mycompany/', login_required(mycompany.CompanyEditView.as_view()), name='company_edit'),
    path('mycompany/delete/', login_required(mycompany.CompanyDeleteView.as_view()), name='company_delete'),
    path('mycompany/vacancies/', login_required(mycompany.CompanyVacanciesView.as_view()), name='company_vacancies'),
    path('mycompany/vacancies/create', login_required(mycompany.CompanyVacancyCreateView.as_view()),
         name='company_vacancy_create'),
    path('mycompany/vacancies/<int:pk>/', login_required(mycompany.CompanyVacancyEditView.as_view()),
         name='company_vacancy_edit'),
    path('mycompany/vacancies/<int:pk>/delete/', login_required(mycompany.CompanyVacancyDeleteView.as_view()),
         name='company_vacancy_delete'),

    path('myresume/letsstart/', login_required(myresume.ResumeLetsStartView.as_view()), name='resume_letsstart'),
    path('myresume/create/', login_required(myresume.ResumeCreateView.as_view()), name='resume_create'),
    path('myresume/', login_required(myresume.ResumeEditView.as_view()), name='resume_edit'),
    path('myresume/delete/', login_required(myresume.ResumeDeleteView.as_view()), name='resume_delete'),
]
