from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #urls for Admin
    path('', views.index, name='index'),
    path('admin/logout/', views.user_logout, name='user_logout'),
    path('admin/forgot_password/', views.forgot_password, name='forgot_password'),
    path('admin/reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('admin_home/', views.custom_admin_home, name='custom_admin_home'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    # #CRUD Operations for Admin
   path('admin/managers/', views.add_manager, name='add_manager'),
    path('admin/managers/<str:id>/', views.update_manager, name='update_manager'),
    path('admin/managers/delete/<str:id>/', views.delete_manager, name='delete_manager'),
    
    path('admin/supervisor/', views.add_supervisor, name='add_supervisor'),
    path('admin/supervisor/<str:id>/', views.update_supervisor, name='update_supervisor'),
    path('admin/supervisor/delete/<str:id>/', views.delete_supervisor, name='delete_supervisor'),

    path('admin/employees/', views.add_employee, name='add_employee'),
    path('admin/employees/<int:id>/', views.update_employee, name='update_employee'),
    path('admin/employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    path('admin/departments/', views.add_department, name='add_department'),
    path('admin/departments/<int:id>/', views.update_department, name='update_department'),
    path('admin/departments/delete/<int:id>/', views.delete_department, name='delete_department'),

    path('admin/shifts/', views.add_shift, name='add_shift'),
    path('admin/shifts/<int:id>/', views.update_shift, name='update_shift'),
    path('admin/shifts/delete/<int:id>/', views.delete_shift, name='delete_shift'),

    path('admin/locations/', views.add_location, name='add_location'),
    path('admin/locations/<int:id>/', views.update_location, name='update_location'),
    path('admin/locations/delete/<int:id>/', views.delete_location, name='delete_location'),

    # urls for Managers & Employees 
    path('common_login/', views.common_user_login, name='common_user_login'),
   
    path('manager/forgot_password/', views.forgot_password_manager, name='forgot_password_manager'),
    path('manager/reset_password/<str:token>/', views.reset_password_manager, name='reset_password_manager'),
    path('supervisor/forgot_password/', views.forgot_password_supervisor, name='forgot_password_supervisor'),
    path('supervisor/reset_password/<str:token>/', views.reset_password_supervisor, name='reset_password_supervisor'),
    path('employee/forgot_password/', views.forgot_password_employee, name='forgot_password_employee'),
    path('employee/reset_password/<str:token>/', views.reset_password_employee, name='reset_password_employee'),
    path('api/employees/<str:id>/', views.view_employee_profile, name='view_employee_profile'),
    path('api/employees/<str:id>/update/', views.update_employee_profile, name='update_employee_profile'),
    path('api/managers/<str:id>/', views.view_manager_profile, name='view_manager_profile'),
    path('api/managers/<int:id>/update/', views.update_manager_profile, name='update_manager_profile'),
    path('api/manager/view_employee/', views.manager_view_employee_profile, name='manager_view_employee_profile'),

    path('api/supervisor/<str:id>/', views.view_supervisor_profile, name='view_supervisor_profile'),
    path('api/supervisor/<str:id>/update/', views.update_supervisor_profile, name='update_supervisor_profile'),
    #  # Attendance History
    # path('admin/admin_manager_attendance_history/', views.admin_manager_attendance_history, name='admin_manager_attendance_history'),
    # path('admin/admin_employee_attendance_history/', views.admin_employee_attendance_history, name='admin_employee_attendance_history'),
    # #Weekly & Monthly chart for Manager from Admin
    # path('admin/admin_manager_weekly_chart/', views.admin_manager_weekly_chart, name='admin_manager_weekly_chart'),
    # path('admin/admin_manager_monthly_chart/', views.admin_manager_monthly_chart, name='admin_manager_monthly_chart'),
    # #Weekly & Monthly chart for Employee from Admin
    # path('admin/admin_employee_weekly_chart/', views.admin_employee_weekly_chart, name='admin_employee_weekly_chart'),
    # path('admin/admin_employee_monthly_chart/', views.admin_employee_monthly_chart, name='admin_employee_monthly_chart'),
   
    # # urls for MD
    # # path('md/login/', views.md_login, name='md_login'),
    # path('md/logout/', views.user_logout, name='user_logout'),
    path('md/home/', views.md_home, name='md_home'),
    path('md/add_manager/', views.md_add_manager, name='md_add_manager'),
    path('md/add_supervisor/', views.md_add_supervisor, name='md_add_supervisor'),
    path('md/add_employee/', views.md_add_employee, name='md_add_employee'),
    path('md/add_department/', views.md_add_department, name='md_add_department'),
    path('md/add_shift/', views.md_add_shift, name='md_add_shift'),
    path('md/add_location/', views.md_add_location, name='md_add_location'),
    path('md/delete_manager/<str:manager_id>/', views.md_delete_manager, name='md_delete_manager'),
    path('md/delete_employee/<str:employee_id>/', views.md_delete_employee, name='md_delete_employee'),
    path('md/delete_department/<str:department_id>/', views.md_delete_department, name='md_delete_department'),
    path('md/delete_shift/<str:shift_number>/', views.md_delete_shift, name='md_delete_shift'),
    path('md/delete_location/<str:location_id>/', views.md_delete_location, name='md_delete_location'),
    path('md/update_manager/<int:id>/', views.md_update_manager, name='md_update_manager'),
    path('md/update_employee/<int:id>/', views.md_update_employee, name='md_update_employee'),
    path('md/update_department/<int:id>/', views.md_update_department, name='md_update_department'),
    path('md/update_shift/<int:id>/', views.md_update_shift, name='md_update_shift'),
    path('md/update_location/<int:id>/', views.md_update_location, name='md_update_location'),
    path('md/forgot_password_md/', views.forgot_password_md, name='forgot_password_md'),
    path('md/reset_password_md/<token>/', views.reset_password_md, name='reset_password_md'),

    # #forgot/reset password for md
    path('requests/add/', views.add_request, name='add_request'),
    path('requests/supervisor/', views.supervisor_view_allrequest, name='supervisor_view_allrequest'),
    path('requests/admin/', views.admin_view_request, name='admin_view_request'),
    
    path('todos/', views.todo_list, name='todo_list'),              # GET: List all Todos
    path('todos/create/', views.todo_create, name='todo_create'),   # POST: Create a new Todo
    path('todos/<int:id>/toggle/', views.todo_toggle, name='todo_toggle'),  # PATCH: Toggle Todo
    path('todos/<int:id>/delete/', views.todo_delete, name='todo_delete'),  # DELETE: Delete Todo
    path('news/send/', views.send_news, name='send_news'),
    path('news/view/', views.view_news, name='view_news'),
    path('tickets/', views.self_service, name='self_service'),
    path('tickets/add/', views.add_ticket, name='add_ticket'),
    path('requests/', views.self_request, name='self_request'),
    
    # #Attendance history for md, emp, man.
    # path('md/md_manager_attendance_history/', views.md_manager_attendance_history, name='md_manager_attendance_history'),
    # path('md/md_employee_attendance_history/', views.md_employee_attendance_history, name='md_employee_attendance_history'),
    # #Weekly & Monthly chart for Manager from MD
    # path('md/md_manager_weekly_chart/', views.md_manager_weekly_chart, name='md_manager_weekly_chart'),
    # path('md/md_manager_monthly_chart/', views.md_manager_monthly_chart, name='md_manager_monthly_chart'),
    # #Weekly & Monthly chart for Employee from MD
    # path('md/md_employee_weekly_chart/', views.md_employee_weekly_chart, name='md_employee_weekly_chart'),
    # path('md/md_employee_monthly_chart/', views.md_employee_monthly_chart, name='md_employee_monthly_chart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)