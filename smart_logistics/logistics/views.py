from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import Employee, Goods, WorkAssignment, Ticket, EntryExitLog, WorkLog
from .forms import (GoodsForm, WorkAssignmentForm, TicketForm,
                    WorkLogForm, EmployeeCreateForm, UpdateAssignmentStatusForm)


# ─── Auth ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'logistics/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Dashboard Router ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    try:
        request.user.employee
        return redirect('employee_dashboard')
    except Employee.DoesNotExist:
        messages.warning(request, 'Your employee profile is not set up yet. Contact admin.')
        return render(request, 'logistics/login.html')


# ─── Admin Views ──────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')

    employees = Employee.objects.select_related('user').all()
    goods = Goods.objects.all()
    tickets = Ticket.objects.select_related('employee__user').order_by('-created_at')[:5]
    assignments = WorkAssignment.objects.select_related('employee__user').all()

    goods_pending = goods.filter(status='pending').count()
    goods_transit = goods.filter(status='in_transit').count()
    goods_delivered = goods.filter(status='delivered').count()
    open_tickets = Ticket.objects.filter(status='open').count()

    # Chart data
    status_data = {
        'labels': ['Pending', 'In Transit', 'Delivered'],
        'values': [goods_pending, goods_transit, goods_delivered],
    }

    # Monthly work hours for chart (last 6 months)
    today = date.today()
    monthly_hours = []
    monthly_labels = []
    for i in range(5, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year - ((today.month - i - 1) // 12)
        total = WorkLog.objects.filter(date__year=y, date__month=m).aggregate(t=Sum('hours'))['t'] or 0
        monthly_labels.append(date(y, m, 1).strftime('%b'))
        monthly_hours.append(float(total))

    context = {
        'employees': employees,
        'goods': goods,
        'tickets': tickets,
        'assignments': assignments,
        'goods_pending': goods_pending,
        'goods_transit': goods_transit,
        'goods_delivered': goods_delivered,
        'open_tickets': open_tickets,
        'total_employees': employees.count(),
        'total_goods': goods.count(),
        'status_data': json.dumps(status_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_hours': json.dumps(monthly_hours),
    }
    return render(request, 'logistics/admin_dashboard.html', context)


@login_required
def add_goods(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    form = GoodsForm()
    if request.method == 'POST':
        form = GoodsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goods added successfully.')
            return redirect('admin_dashboard')
    return render(request, 'logistics/add_goods.html', {'form': form, 'title': 'Add Goods'})


@login_required
def edit_goods(request, pk):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    goods = get_object_or_404(Goods, pk=pk)
    form = GoodsForm(instance=goods)
    if request.method == 'POST':
        form = GoodsForm(request.POST, instance=goods)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goods updated successfully.')
            return redirect('admin_dashboard')
    return render(request, 'logistics/add_goods.html', {'form': form, 'title': 'Edit Goods', 'goods': goods})


@login_required
def delete_goods(request, pk):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    goods = get_object_or_404(Goods, pk=pk)
    if request.method == 'POST':
        goods.delete()
        messages.success(request, 'Goods deleted.')
    return redirect('admin_dashboard')


@login_required
def allocate_work(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    form = WorkAssignmentForm()
    if request.method == 'POST':
        form = WorkAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work allocated successfully.')
            return redirect('admin_dashboard')
    return render(request, 'logistics/allocate_work.html', {'form': form})


@login_required
def admin_tickets(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    tickets = Ticket.objects.select_related('employee__user').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    return render(request, 'logistics/admin_tickets.html', {'tickets': tickets, 'status_filter': status_filter})


@login_required
def update_ticket_status(request, pk):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Ticket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()
            messages.success(request, 'Ticket status updated.')
    return redirect('admin_tickets')


@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    form = EmployeeCreateForm()
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('admin_dashboard')
    return render(request, 'logistics/add_employee.html', {'form': form})


@login_required
def employee_activity(request, pk):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    employee = get_object_or_404(Employee, pk=pk)
    logs = EntryExitLog.objects.filter(employee=employee).order_by('-timestamp')[:20]
    work_logs = WorkLog.objects.filter(employee=employee).order_by('-date')[:30]
    assignments = WorkAssignment.objects.filter(employee=employee)
    tickets = Ticket.objects.filter(employee=employee)
    total_hours = work_logs.aggregate(t=Sum('hours'))['t'] or 0
    return render(request, 'logistics/employee_activity.html', {
        'employee': employee, 'logs': logs, 'work_logs': work_logs,
        'assignments': assignments, 'tickets': tickets, 'total_hours': total_hours,
    })


# ─── Employee Views ───────────────────────────────────────────────────────────

@login_required
def employee_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('login')

    assignments = WorkAssignment.objects.filter(employee=employee)
    pending_tasks = assignments.exclude(status='completed')
    tickets = Ticket.objects.filter(employee=employee)
    work_logs = WorkLog.objects.filter(employee=employee).order_by('-date')[:7]
    entry_logs = EntryExitLog.objects.filter(employee=employee).order_by('-timestamp')[:5]

    week_hours = WorkLog.objects.filter(
        employee=employee,
        date__gte=date.today() - timedelta(days=7)
    ).aggregate(t=Sum('hours'))['t'] or 0

    # Check if already clocked in today
    today_logs = EntryExitLog.objects.filter(employee=employee, timestamp__date=date.today()).order_by('-timestamp')
    last_log = today_logs.first()
    clocked_in = last_log and last_log.log_type == 'entry'

    context = {
        'employee': employee,
        'assignments': assignments,
        'pending_tasks': pending_tasks,
        'tickets': tickets,
        'work_logs': work_logs,
        'entry_logs': entry_logs,
        'week_hours': week_hours,
        'clocked_in': clocked_in,
        'total_assignments': assignments.count(),
        'completed_tasks': assignments.filter(status='completed').count(),
        'open_tickets': tickets.filter(status='open').count(),
    }
    return render(request, 'logistics/employee_dashboard.html', context)


@login_required
def create_ticket(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return redirect('login')
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.employee = employee
            ticket.save()
            messages.success(request, 'Ticket submitted successfully.')
            return redirect('employee_dashboard')
    return render(request, 'logistics/create_ticket.html', {'form': form})


@login_required
def work_log(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return redirect('login')
    form = WorkLogForm(initial={'date': date.today()})
    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.employee = employee
            try:
                log.save()
                messages.success(request, 'Work log saved.')
            except Exception:
                messages.error(request, 'A log for this date already exists.')
            return redirect('work_log')

    logs = WorkLog.objects.filter(employee=employee).order_by('-date')
    total_hours = logs.aggregate(t=Sum('hours'))['t'] or 0

    # Build calendar data for current month
    today = date.today()
    first_day = today.replace(day=1)
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

    month_logs = {log.date: log.hours for log in logs.filter(date__year=today.year, date__month=today.month)}

    # Build calendar grid
    calendar_weeks = []
    day = first_day - timedelta(days=first_day.weekday())
    while day <= last_day:
        week = []
        for _ in range(7):
            if first_day <= day <= last_day:
                week.append({'date': day, 'hours': month_logs.get(day, None), 'today': day == today})
            else:
                week.append({'date': None, 'hours': None, 'today': False})
            day += timedelta(days=1)
        calendar_weeks.append(week)

    context = {
        'form': form, 'logs': logs, 'total_hours': total_hours,
        'calendar_weeks': calendar_weeks, 'current_month': today.strftime('%B %Y'),
    }
    return render(request, 'logistics/work_log.html', context)


@login_required
def entry_exit_log(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return redirect('login')
    if request.method == 'POST':
        log_type = request.POST.get('log_type')
        if log_type in ('entry', 'exit'):
            EntryExitLog.objects.create(employee=employee, log_type=log_type)
            messages.success(request, f'{"Clocked in" if log_type == "entry" else "Clocked out"} successfully.')
    return redirect('employee_dashboard')


@login_required
def update_assignment_status(request, pk):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return redirect('login')
    assignment = get_object_or_404(WorkAssignment, pk=pk, employee=employee)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(WorkAssignment.STATUS_CHOICES):
            assignment.status = new_status
            assignment.save()
            messages.success(request, 'Assignment updated.')
    return redirect('employee_dashboard')
