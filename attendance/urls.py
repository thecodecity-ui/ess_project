from django.urls import path
from . import views
from .views import ApprovePermissionHourView, EmployeeMonthlyAttendanceChartView, EmployeeMonthlyChartAPIView, EmployeeWeeklyAttendanceChartView, EmployeeYearlyAttendanceChartView, ManagePermissionHoursView, RequestPermissionHourView, calculate_total_present_days
from .views import employee_attendance_form_api
from .views import submit_employee_attendance_api

from .views import ManagerAttendanceFormAPI
from .views import EmployeeAttendanceHistoryAPIView

from .views import SubmitManagerAttendanceAPI
from .views import ManagerAttendanceHistory
from .views import ShowEmployeeAttendanceHistory
from .views import EmployeeRequestCheckOutReset
from .views import ManagerResetRequests
from .views import ApproveResetRequestAPI
from .views import ResetCheckoutTimeAPI
from .views import RejectResetRequestAPI
from .views import ManagerCheckOutResetRequestAPI
from .views import AdminManagerResetRequestsAPI
from .views import AdminApproveManagerResetRequestAPI
from .views import AdminRejectManagerResetRequestAPI
from .views import AdminResetManagerCheckoutTimeAPI

from .views import MdApproveManagerResetRequestAPIView
from .views import ShowEmployeeWeeklyChartAPIView

from .views import SupervisorAttendanceFormAPIView
from .views import SubmitSupervisorAttendanceAPIView
from .views import SupervisorAttendanceHistory
from .views import SupervisorRequestCheckOutReset
from .views import AdminSupervisorResetRequests
from .views import AdminApproveSupervisorResetRequest
from .views import AdminRejectSupervisorResetRequest
from .views import AdminResetSupervisorCheckoutTime
from .views import MdSupervisorResetRequests
from .views import MDApproveSupervisorResetRequest
from .views import MDRejectSupervisorResetRequest
from .views import MDResetSupervisorCheckoutTime
from .views import SupervisorWeeklyAttendanceChart
from .views import SupervisorMonthlyAttendanceChartAPIView

from .views import AdminManagerAttendanceHistoryAPIView
from .views import AdminSupervisorAttendanceHistoryAPIView
from .views import AdminEmployeeAttendanceHistoryAPIView
from .views import AdminManagerWeeklyChartAPIView
from .views import AdminSupervisorWeeklyChartAPI

from .views import AdminManagerMonthlyChartAPIView
from .views import AdminSupervisorMonthlyChartAPIView
from .views import AdminEmployeeWeeklyChartAPI
from .views import AdminEmployeeMonthlyChartAPI
from .views import EmployeeRequestCheckOutResetAPI
from .views import MdManagerAttendanceHistoryAPI
from .views import MdSupervisorAttendanceHistoryAPI
from .views import MdEmployeeAttendanceHistoryAPI
from .views import md_manager_weekly_chart_api
from .views import MdSupervisorWeeklyChartAPI
from .views import ManagerMonthlyChartAPI
from .views import SupervisorMonthlyChartAPI
from .views import MdEmployeeMonthlyChartAPIView
from .views import (
    ScheduleListCreateAPIView,
    ScheduleDetailAPIView,
    DepartmentActiveJobListCreateAPIView,
    DepartmentActiveJobDetailAPIView,
    CalendarEventListCreateAPIView,
    CalendarEventDetailAPIView,
    OfferListCreateAPIView,
    OfferDetailAPIView,
    ShiftAttendanceListCreateAPIView,
    ShiftAttendanceDetailAPIView,
)








urlpatterns = [
    path('api/calculate-total-present-days/<int:employee_id>/', calculate_total_present_days, name='calculate_total_present_days_api'),
    path('api/employee-attendance-form/', employee_attendance_form_api, name='employee_attendance_form_api'),
    path('api/submit-attendance/', submit_employee_attendance_api, name='submit_employee_attendance_api'),

    path('api/manager/attendance/', ManagerAttendanceFormAPI.as_view(), name='manager_attendance_form_api'),
    path('api/manager/attendance/submit/', SubmitManagerAttendanceAPI.as_view(), name='submit_manager_attendance_api'),
    path('api/manager/attendance-history/', ManagerAttendanceHistory.as_view(), name='manager_attendance_history_api'),
    path('api/employee-attendance-history/', EmployeeAttendanceHistoryAPIView.as_view(), name='employee_attendance_history_api'),

    path('api/employee/attendance-history/', ShowEmployeeAttendanceHistory.as_view(), name='show_employee_attendance_history_api'),
    path('api/employee/request-checkout-reset/', EmployeeRequestCheckOutReset.as_view(), name='employee_request_checkout_reset_api'),
    path('api/manager/reset-requests/', ManagerResetRequests.as_view(), name='manager_reset_requests_api'),
    path('api/manager/approve-reset-request/<int:request_id>/', ApproveResetRequestAPI.as_view(), name='approve_reset_request_api'),
    path('api/manager/reset-checkout-time/<int:employee_id>/<str:date>/', ResetCheckoutTimeAPI.as_view(), name='reset_checkout_time_api'),
    path('manager/reject-reset-request/<int:request_id>/', RejectResetRequestAPI.as_view(), name='reject_reset_request'),
    path('manager/request-checkout-reset/', ManagerCheckOutResetRequestAPI.as_view(), name='manager_request_check_out_reset'),
    path('admin/manager-reset-requests/', AdminManagerResetRequestsAPI.as_view(), name='admin_manager_reset_requests'),
    path('admin/approve-manager-reset-request/<int:request_id>/', AdminApproveManagerResetRequestAPI.as_view(), name='admin_approve_manager_reset_request'),
    path('admin/reject-manager-reset-request/<int:request_id>/', AdminRejectManagerResetRequestAPI.as_view(), name='admin_reject_manager_reset_request'),
    path('admin/reset-manager-checkout-time/<int:manager_id>/<str:date>/', AdminResetManagerCheckoutTimeAPI.as_view(), name='admin_reset_manager_checkout_time'),
    path('admin/employee/reset-requests/', views.AdminEmployeeResetRequestsAPIView.as_view(), name='admin_employee_reset_requests_api'),
    path('admin/employee/reset-request/approve/<int:request_id>/', views.AdminApproveEmployeeResetRequestAPIView.as_view(), name='admin_approve_employee_reset_request_api'),
    path('admin/employee/reset-request/reject/<int:request_id>/', views.AdminRejectEmployeeResetRequestAPIView.as_view(), name='admin_reject_employee_reset_request_api'),
    path('admin/employee/checkout-time/reset/<int:employee_id>/<str:date>/', views.AdminResetEmployeeCheckoutTimeAPIView.as_view(), name='admin_reset_employee_checkout_time_api'),
    path('md/employee/reset-requests/', views.MdEmployeeResetRequestsAPIView.as_view(), name='md_employee_reset_requests_api'),
    path('md/approve_employee_reset_request/<int:request_id>/', views.MdApproveEmployeeResetRequestAPIView.as_view(), name='md_approve_employee_reset_request'),
    path('md/reject_employee_reset_request/<int:request_id>/', views.MdRejectEmployeeResetRequestAPIView.as_view(), name='md_reject_employee_reset_request'),
    path('md/reset_employee_checkout_time/<int:employee_id>/<str:date>/', views.MdResetEmployeeCheckoutTimeAPIView.as_view(), name='md_reset_employee_checkout_time'),
    path('md/manager_reset_requests/', views.MdManagerResetRequestsAPIView.as_view(), name='md_manager_reset_requests'),
    path('approve-reset-request/<int:request_id>/', MdApproveManagerResetRequestAPIView.as_view(), name='approve_reset_request'),
    path('api/md/reject_manager_reset_request/<int:request_id>/', views.md_reject_manager_reset_request_api, name='md_reject_manager_reset_request_api'),
    path('api/md/reset_manager_checkout_time/<int:manager_id>/<str:date>/', views.md_reset_manager_checkout_time_api, name='md_reset_manager_checkout_time_api'),

    
    path('api/manager/weekly_attendance_chart/', views.manager_weekly_attendance_chart_api, name='manager_weekly_attendance_chart_api'),
    path('api/show_employee_weekly_chart/', ShowEmployeeWeeklyChartAPIView.as_view(), name='show_employee_weekly_chart_api'),
    
    path('api/manager/monthly-attendance-chart/', views.manager_monthly_attendance_chart_api, name='manager_monthly_attendance_chart_api'),
    path('api/employee-monthly-chart/', EmployeeMonthlyChartAPIView.as_view(), name='employee-monthly-chart'),
    path('api/supervisor-attendance-form/', SupervisorAttendanceFormAPIView.as_view(), name='supervisor-attendance-form'),
    path('api/supervisor-attendance/', SubmitSupervisorAttendanceAPIView.as_view(), name='submit-supervisor-attendance'),
    path('api/supervisor/attendance/history/', SupervisorAttendanceHistory.as_view(), name='supervisor_attendance_history_api'),
    path('api/supervisor/attendance/reset/', SupervisorRequestCheckOutReset.as_view(), name='supervisor_request_check_out_reset_api'),
    path('api/admin/supervisor/reset-requests/', AdminSupervisorResetRequests.as_view(), name='admin_supervisor_reset_requests_api'),
    path('api/admin/supervisor/reset-request/approve/<int:request_id>/', AdminApproveSupervisorResetRequest.as_view(), name='admin_approve_supervisor_reset_request_api'),
    path('api/admin/supervisor/reset-request/reject/<int:request_id>/', AdminRejectSupervisorResetRequest.as_view(), name='admin_reject_supervisor_reset_request_api'),
    path('api/admin/supervisor/reset-checkout-time/<int:supervisor_id>/<str:date>/', AdminResetSupervisorCheckoutTime.as_view(), name='admin_reset_supervisor_checkout_time_api'),
    path('api/md/supervisor/reset-requests/', MdSupervisorResetRequests.as_view(), name='md_supervisor_reset_requests_api'),
    path('api/md/approve-supervisor-reset-request/<int:request_id>/', MDApproveSupervisorResetRequest.as_view(), name='api_md_approve_supervisor_reset_request'),
    path('api/md/reject-supervisor-reset-request/<int:request_id>/', MDRejectSupervisorResetRequest.as_view(), name='api_md_reject_supervisor_reset_request'),
    path('api/md/reset-supervisor-checkout-time/<int:supervisor_id>/<str:date>/', MDResetSupervisorCheckoutTime.as_view(), name='api_md_reset_supervisor_checkout_time'),
    path('api/supervisor/weekly-attendance-chart/', SupervisorWeeklyAttendanceChart.as_view(), name='api_supervisor_weekly_attendance_chart'),
    path('api/supervisor-monthly-attendance-chart/', SupervisorMonthlyAttendanceChartAPIView.as_view(), name='supervisor_monthly_attendance_chart_api'),

    path('api/admin-manager-attendance-history/', AdminManagerAttendanceHistoryAPIView.as_view(), name='admin_manager_attendance_history_api'),
    path('api/admin-supervisor-attendance-history/', AdminSupervisorAttendanceHistoryAPIView.as_view(), name='admin_supervisor_attendance_history_api'),
    path('api/admin-employee-attendance-history/', AdminEmployeeAttendanceHistoryAPIView.as_view(), name='admin_employee_attendance_history_api'),
    path('api/admin_manager_weekly_chart/', AdminManagerWeeklyChartAPIView.as_view(), name='admin_manager_weekly_chart_api'),
    path('api/supervisor/weekly-chart/', AdminSupervisorWeeklyChartAPI.as_view(), name='admin_supervisor_weekly_chart_api'),
   
    path('api/admin/manager-monthly-chart/', AdminManagerMonthlyChartAPIView.as_view(), name='admin-manager-monthly-chart-api'),
    path('api/admin/supervisor/monthly_chart/', AdminSupervisorMonthlyChartAPIView.as_view(), name='admin-supervisor-monthly-chart'),
    path('admin/employee/weekly-chart/', AdminEmployeeWeeklyChartAPI.as_view(), name='admin_employee_weekly_chart_api'),
    path('api/admin/employee-monthly-chart/', AdminEmployeeMonthlyChartAPI.as_view(), name='admin_employee_monthly_chart_api'),
    path('api/employee/checkout-reset/', EmployeeRequestCheckOutResetAPI.as_view(), name='employee_request_checkout_reset_api'),
    path('api/md/manager-attendance-history/', MdManagerAttendanceHistoryAPI.as_view(), name='md_manager_attendance_history_api'),
    path('api/md/supervisor-attendance-history/', MdSupervisorAttendanceHistoryAPI.as_view(), name='md_supervisor_attendance_history_api'),
    path('api/md/employee-attendance-history/', MdEmployeeAttendanceHistoryAPI.as_view(), name='md_employee_attendance_history_api'),
    path('api/md_manager_weekly_chart/', md_manager_weekly_chart_api, name='md_manager_weekly_chart_api'),
    path('api/md_supervisor_weekly_chart/', MdSupervisorWeeklyChartAPI.as_view(), name='md_supervisor_weekly_chart_api'),
    path('api/manager-monthly-chart/', ManagerMonthlyChartAPI.as_view(), name='manager_monthly_chart_api'),
    path('api/supervisor-monthly-chart/', SupervisorMonthlyChartAPI.as_view(), name='supervisor_monthly_chart_api'),
    path('api/md_employee_weekly_chart/', views.md_employee_weekly_chart_api, name='md_employee_weekly_chart_api'),
    path('api/md_employee_monthly_chart/', MdEmployeeMonthlyChartAPIView.as_view(), name='md_employee_monthly_chart'),
    path('permission-hours/request/', RequestPermissionHourView.as_view(), name='request-permission-hour'),
    path('permission-hours/<int:permission_id>/approve/', ApprovePermissionHourView.as_view(), name='approve-permission-hour'),
    path('permission-hours/manage/', ManagePermissionHoursView.as_view(), name='manage-permission-hours'),
    path('employee/employee-weekly-attendance-chart/', EmployeeWeeklyAttendanceChartView.as_view(), name='employee_weekly_attendance_chart'),
     path('employee/employee-monthly-attendance-chart/', EmployeeMonthlyAttendanceChartView.as_view(), name='employee_monthly_attendance_chart'),
     path('employee/employee-yearly-attendance-chart/', EmployeeYearlyAttendanceChartView.as_view(), name='employee_yearly_attendance_chart'),

    path('schedules/', ScheduleListCreateAPIView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleDetailAPIView.as_view(), name='schedule-detail'),
    path('active-jobs/', DepartmentActiveJobListCreateAPIView.as_view(), name='active-job-list-create'),
    path('active-jobs/<int:pk>/', DepartmentActiveJobDetailAPIView.as_view(), name='active-job-detail'),
    path('calendar-events/', CalendarEventListCreateAPIView.as_view(), name='calendar-event-list-create'),
    path('calendar-events/<int:pk>/', CalendarEventDetailAPIView.as_view(), name='calendar-event-detail'),
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferDetailAPIView.as_view(), name='offer-detail'),
    path('shifts/', ShiftAttendanceListCreateAPIView.as_view(), name='shift-list-create'),
    path('shifts/<int:pk>/', ShiftAttendanceDetailAPIView.as_view(), name='shift-detail'),
]
