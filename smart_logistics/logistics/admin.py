from django.contrib import admin
from .models import Employee, Goods, WorkAssignment, Ticket, EntryExitLog, WorkLog

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'department', 'phone', 'joined_date']

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'status', 'assigned_to', 'created_at']
    list_filter = ['status']

@admin.register(WorkAssignment)
class WorkAssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'status', 'due_date']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'priority', 'status', 'created_at']

@admin.register(EntryExitLog)
class EntryExitLogAdmin(admin.ModelAdmin):
    list_display = ['employee', 'log_type', 'timestamp']

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'hours']
