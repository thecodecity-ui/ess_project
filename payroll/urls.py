from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (ManagerPayrollHistoryAPIView, 
                    ManagerPayrollNotificationView, 
                    ManagerProcessPayrollAPIView, 
                    PayrollHistoryAPIView, 
                    PayrollNotificationView, 
                    ProcessPayrollAPIView, 
                    SupervisorPayrollHistoryAPIView, 
                    SupervisorPayrollNotificationView, 
                    SupervisorProcessPayrollAPIView, bonus_list_by_user)

urlpatterns = [
    # URL for processing payroll
    path('process-payroll/', ProcessPayrollAPIView.as_view(), name='process_payroll'),
    path('process-payroll/', ManagerProcessPayrollAPIView.as_view(), name='process_payroll'),
    path('payroll-history/', PayrollHistoryAPIView.as_view(), name='payroll_history'),
    path('manager-payroll-history/', ManagerPayrollHistoryAPIView.as_view(), name='manager_payroll_history'),
    path('payroll-notification/', PayrollNotificationView.as_view(), name='payroll-notification'),
    path('manager-payroll-notification/', ManagerPayrollNotificationView.as_view(), name='manager-payroll-notification'),
     path('process-payroll/', SupervisorProcessPayrollAPIView.as_view(), name='process_payroll'),
      path('supervisor-payroll-notification/', SupervisorPayrollNotificationView.as_view(), name='supervisor-payroll-notification'),
       path('supervisor-payroll-history/', SupervisorPayrollHistoryAPIView.as_view(), name='supervisor_payroll_history'),
       path('create_salary/', views.create_salary, name='create_salary'),
    path('create_bonus/', views.create_bonus, name='create_bonus'),
    path('mark_bonus_paid/<int:bonus_id>/', views.mark_bonus_paid, name='mark_bonus_paid'),
    path('bonus_list/', views.bonus_list, name='bonus_list'),
    path('salary_history/', views.salary_history, name='salary_history'),
     path('salary-history/all/', views.all_salary_history, name='all_salary_history'),
     path('salary-history/<str:user_id>/', views.salary_history_by_id, name='salary_history_by_id'),
     path('payroll-history/all/', views.all_payroll_history, name='all_payroll_history'),
     path('payroll-history/<str:user_id>/', views.payroll_history, name='payroll_history'),
      path('bonus-list/<int:user_id>/', bonus_list_by_user, name='bonus_list_by_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
