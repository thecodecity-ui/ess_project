from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
# Import the views from the same directory

urlpatterns = [
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('leave-history/', views.leave_history, name='leave_history'),
    path('employee-leave-status/', views.employee_leave_status, name='employee_leave_status'),
    path('employee-leave-calendar/', views.employee_leave_calendar_view, name='employee_leave_calendar'),
    path('manager-apply-leave/', views.manager_apply_leave, name='manager_apply_leave'),
    path('manager-leave-history/', views.manager_leave_history, name='manager_leave_history'),
    path('manager-leave-calendar/', views.manager_leave_calendar_view, name='manager_leave_calendar'),
    path('manager-leave-status/', views.manager_leave_status, name='manager_leave_status'),
    # Leave policies endpoints
    path('leave-policies/', views.leave_policies, name='leave_policies'),
    path('leave-balance/update/<str:user>/', views.update_leave_balance, name='update_leave_balance'),

    # Manager leave policies endpoints
    path('manager-leave-policies/', views.manager_leave_policies, name='manager_leave_policies'),
    path('manager-leave-balance/update/<str:user>/', views.update_manager_leave_balance, name='update_manager_leave_balance'),

    # Notification endpoints
    path('notification/cancel/<int:notification_id>/', views.cancel_notification, name='cancel_notification'),
    path('admin-notification/cancel/<int:notification_id>/', views.admin_cancel_notification, name='admin_cancel_notification'),
    path('manager-notification/cancel/<int:notification_id>/', views.manager_cancel_notification, name='manager_cancel_notification'),
    path('apply-leave/', views.supervisor_apply_leave, name='supervisor_apply_leave'),
    path('leave-history/', views.supervisor_leave_history, name='supervisor_leave_history'),
    path('leave-calendar/', views.supervisor_leave_calendar_view, name='supervisor_leave_calendar_view'),
    path('leave-status/', views.supervisor_leave_status, name='supervisor_leave_status'),
    path('supervisor-leave-policies/', views.supervisor_leave_policies, name='supervisor_leave_policies'),
    path('update-supervisor-leave-balance/<str:user>/', views.update_supervisor_leave_balance, name='update_supervisor_leave_balance'),
    path('cancel-supervisor-notification/<int:notification_id>/', views.supervisor_cancel_notification, name='supervisor_cancel_notification'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
