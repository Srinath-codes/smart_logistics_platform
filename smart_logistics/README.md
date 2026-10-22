# 📦 SmartLogix — Smart Logistics Platform

A complete Django-based logistics management system with role-based dashboards for Admins and Employees.

---

## 🗂 Project Structure

```
smart_logistics/
├── manage.py
├── requirements.txt
├── setup.sh                    ← One-command setup
├── demo_data.py                ← Optional demo data loader
│
├── smart_logistics/            ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── logistics/                  ← Main app
│   ├── models.py               ← Employee, Goods, Ticket, WorkLog, etc.
│   ├── views.py                ← All views (admin + employee)
│   ├── forms.py                ← Django forms
│   ├── urls.py                 ← App URL routing
│   ├── admin.py                ← Django admin registration
│   ├── apps.py
│   ├── migrations/
│   └── templates/logistics/
│       ├── base.html           ← Sidebar layout
│       ├── login.html
│       ├── admin_dashboard.html
│       ├── employee_dashboard.html
│       ├── add_goods.html
│       ├── add_employee.html
│       ├── allocate_work.html
│       ├── admin_tickets.html
│       ├── employee_activity.html
│       ├── create_ticket.html
│       └── work_log.html
│
└── static/
    └── css/
        └── style.css           ← Full custom CSS (dark theme)
```

---

## ⚡ Quick Setup

### Option A — Automated (recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### Option B — Manual

**1. Create & activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run migrations**
```bash
python manage.py makemigrations logistics
python manage.py migrate
```

**4. Create superuser (Admin)**
```bash
python manage.py createsuperuser
```
Follow the prompts to set username and password.

**5. (Optional) Load demo data**
```bash
python manage.py shell < demo_data.py
```
Creates 3 employee accounts (`alice`, `bob`, `carol` — password: `pass1234`), sample goods, tickets, work logs, and assignments.

**6. Start the server**
```bash
python manage.py runserver
```
Visit → **http://127.0.0.1:8000**

---

## 🔐 Roles & Access

| Role | Login | Access |
|------|-------|--------|
| **Admin** | Superuser account | Full dashboard, manage goods, allocate work, view all tickets, monitor employees |
| **Employee** | Normal user with Employee profile | Personal dashboard, tasks, create tickets, work log, clock in/out |

Homepage (`/`) automatically redirects to the login page.  
After login, users are routed to the correct dashboard based on role.

---

## 📋 Features

### Admin
- 📊 Dashboard with stats + Chart.js analytics (donut + bar charts)
- 📦 Add / edit / delete goods (name, quantity, status, assignee)
- 👷 Create employee accounts
- 📋 Allocate tasks to employees with due dates
- 🎫 View & update all employee tickets (filter by status)
- 👁 Monitor individual employee activity (logs, hours, assignments)

### Employee
- 🏠 Personal dashboard with stats
- ⏱ Clock In / Clock Out with live status banner
- ✅ View assigned tasks, update task status
- 🎫 Create support tickets with priority levels
- 📅 Work hours log with calendar view (current month)
- 📋 Entry/exit timeline

---

## 🗄 Data Models

| Model | Key Fields |
|-------|-----------|
| `Employee` | user (OneToOne), department, phone, joined_date |
| `Goods` | name, quantity, status (pending/in_transit/delivered), assigned_to |
| `WorkAssignment` | employee, title, description, status, due_date |
| `Ticket` | employee, title, description, priority, status |
| `EntryExitLog` | employee, log_type (entry/exit), timestamp |
| `WorkLog` | employee, date, hours, notes (unique per employee+date) |

---

## 🗃 URLs

| URL | View | Access |
|-----|------|--------|
| `/` | Login | Public |
| `/login/` | Login | Public |
| `/logout/` | Logout | Auth |
| `/dashboard/` | Role router | Auth |
| `/admin-dashboard/` | Admin dashboard | Admin |
| `/goods/add/` | Add goods | Admin |
| `/goods/<pk>/edit/` | Edit goods | Admin |
| `/goods/<pk>/delete/` | Delete goods | Admin |
| `/allocate-work/` | Assign tasks | Admin |
| `/tickets/admin/` | All tickets | Admin |
| `/employees/add/` | Add employee | Admin |
| `/employees/<pk>/activity/` | Employee activity | Admin |
| `/employee-dashboard/` | Employee home | Employee |
| `/tickets/create/` | New ticket | Employee |
| `/work-log/` | Work log + calendar | Employee |
| `/entry-exit/` | Clock in/out | Employee |
| `/assignments/<pk>/update/` | Update task status | Employee |
| `/admin/` | Django admin panel | Superuser |

---

## 🎨 UI Design

- **Theme**: Dark industrial with amber accents
- **Fonts**: Syne (display) + DM Mono (data/labels)
- **Components**: Stat cards, data tables, badges, priority indicators, timeline, calendar grid
- **Charts**: Chart.js — donut (goods status) + bar (monthly hours)
- Custom CSS only — no Bootstrap/Tailwind dependency

---

## 🔄 Switch to MySQL

In `settings.py`, comment out SQLite and uncomment the MySQL block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smart_logistics_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

Then install the MySQL driver:
```bash
pip install mysqlclient
```

Create the database in MySQL first:
```sql
CREATE DATABASE smart_logistics_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then re-run migrations:
```bash
python manage.py migrate
```

---

## 🛡 Production Notes

Before deploying to production:
1. Set `DEBUG = False` in `settings.py`
2. Change `SECRET_KEY` to a strong random value
3. Set `ALLOWED_HOSTS` to your domain
4. Run `python manage.py collectstatic`
5. Use Gunicorn + Nginx for serving
6. Use environment variables for secrets (e.g., `python-decouple`)
