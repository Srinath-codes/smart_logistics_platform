from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('goods/add/', views.add_goods, name='add_goods'),
    path('goods/<int:pk>/edit/', views.edit_goods, name='edit_goods'),
    path('goods/<int:pk>/delete/', views.delete_goods, name='delete_goods'),
    path('allocate-work/', views.allocate_work, name='allocate_work'),
    path('tickets/admin/', views.admin_tickets, name='admin_tickets'),
    path('tickets/<int:pk>/update/', views.update_ticket_status, name='update_ticket_status'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<int:pk>/activity/', views.employee_activity, name='employee_activity'),

    # Employee
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('work-log/', views.work_log, name='work_log'),
    path('entry-exit/', views.entry_exit_log, name='entry_exit_log'),
    path('assignments/<int:pk>/update/', views.update_assignment_status, name='update_assignment_status'),
]
