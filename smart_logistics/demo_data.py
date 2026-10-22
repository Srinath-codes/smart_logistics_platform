"""
Demo data loader — run via: python manage.py shell < demo_data.py
Or called automatically by setup.sh
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_logistics.settings')
django.setup()

from django.contrib.auth.models import User
from logistics.models import Employee, Goods, WorkAssignment, Ticket, EntryExitLog, WorkLog
from django.utils import timezone
from datetime import date, timedelta
import random

print("Loading demo data...")

# Create employees
emp_data = [
    ("alice", "Alice Johnson", "Warehouse", "555-0101"),
    ("bob", "Bob Martinez", "Transport", "555-0102"),
    ("carol", "Carol Smith", "Operations", "555-0103"),
]

employees = []
for uname, fullname, dept, phone in emp_data:
    if not User.objects.filter(username=uname).exists():
        first, last = fullname.split(" ", 1)
        user = User.objects.create_user(username=uname, password="pass1234", first_name=first, last_name=last)
        emp = Employee.objects.create(user=user, department=dept, phone=phone)
        employees.append(emp)
        print(f"  Created employee: {uname} / pass1234")
    else:
        employees.append(Employee.objects.get(user__username=uname))

# Create goods
goods_data = [
    ("Industrial Motors x10", 10, "pending"),
    ("Steel Pipes Bundle", 50, "in_transit"),
    ("Electronic Components Kit", 200, "pending"),
    ("Safety Equipment Set", 30, "delivered"),
    ("Conveyor Belts", 5, "in_transit"),
    ("Hydraulic Pumps", 8, "delivered"),
]
for name, qty, status in goods_data:
    g, created = Goods.objects.get_or_create(name=name, defaults={
        "quantity": qty, "status": status,
        "assigned_to": random.choice(employees) if random.random() > 0.4 else None
    })
    if created:
        print(f"  Created goods: {name}")

# Create assignments
task_data = [
    (employees[0], "Inspect Warehouse Section A", "Full inspection of storage zone A including safety checks.", "assigned"),
    (employees[1], "Deliver Batch #2024-11 to Zone 3", "Transport goods from loading bay to zone 3.", "in_progress"),
    (employees[2], "Update Inventory Records", "Reconcile physical count with system records.", "completed"),
    (employees[0], "Prepare Shipping Documents", "Process outgoing shipment documentation.", "assigned"),
]
for emp, title, desc, status in task_data:
    WorkAssignment.objects.get_or_create(employee=emp, title=title, defaults={
        "description": desc, "status": status,
        "due_date": date.today() + timedelta(days=random.randint(1, 14))
    })

# Create tickets
ticket_data = [
    (employees[0], "Forklift battery low", "The forklift in bay 2 has a degraded battery.", "medium", "open"),
    (employees[1], "Missing PPE in Zone 3", "Safety helmets are not available.", "high", "in_review"),
    (employees[2], "System access issue", "Cannot log into inventory module.", "low", "resolved"),
]
for emp, title, desc, priority, status in ticket_data:
    Ticket.objects.get_or_create(employee=emp, title=title, defaults={
        "description": desc, "priority": priority, "status": status
    })

# Create work logs
today = date.today()
for emp in employees:
    for i in range(7):
        d = today - timedelta(days=i)
        WorkLog.objects.get_or_create(employee=emp, date=d, defaults={
            "hours": random.choice([6, 7, 7.5, 8, 8.5, 9]),
            "notes": random.choice(["Regular shift", "Overtime", "Early finish", ""])
        })

# Entry/exit logs
for emp in employees:
    EntryExitLog.objects.get_or_create(employee=emp, log_type="entry",
                                        timestamp=timezone.now() - timedelta(hours=8))

print("\n✓ Demo data loaded successfully!")
print("\nEmployee logins (password: pass1234):")
for uname, fullname, dept, _ in emp_data:
    print(f"  {uname} — {fullname} ({dept})")
