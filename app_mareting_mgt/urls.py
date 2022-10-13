from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from .import views


urlpatterns=[
    path('clientcompany/', views.Client_Company_view.as_view()),
    path('clientcompany/<int:id>/', views.Client_Company_view.as_view()),
    path('user/register/',views.new_register_user.as_view()),
    path('view_RegisteredUser/',views.view_RegisteredUser.as_view()),
    path('api/token/',views.MyTokenObtainPairView.as_view()),
    path('forgotpassword/',views.forgotpasswordview.as_view()),
    path('user/edit/<int:id>/',views.user_edit.as_view()), 
    path('viewcompanies/', views.view_companies.as_view()),
    path('employee/details/',views.empl_details_view.as_view()),
    path('employee/details/<int:id>/',views.empl_details_view.as_view()),
    path('employee/address/',views.employee_address_view.as_view()),
    path('employee/address/<int:id>/',views.employee_address_view.as_view()),
    # path('employee/job/details/',views.employee_job_details.as_view()),
    path('salesprogress/',views.view_salesprogress.as_view()),
    path('salesprogress/<int:id>/',views.view_salesprogress.as_view()),
    path('addtags/', views.tag_view.as_view()),
    path('employee/marketing/meet/',views.view_meeting.as_view()),
    path('employee/marketing/meet/<int:id>/',views.view_meeting.as_view()),
    path('user/logout/',views.Logout.as_view()),
    # path('meeting/<int:id>/',views.meeting_data.as_view()),
]

