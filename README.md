# Smart Logistics Platform

A small Django app for keeping day-to-day logistics work in one place. Admins can track goods, assign work, review employee tickets, and see activity at a glance. Employees get a focused dashboard for their tasks, work hours, and support requests.

## What you can do

- Manage goods and follow their progress from pending to delivered.
- Create employee accounts and assign work with due dates.
- Let employees update task progress, log work hours, and clock in or out.
- Handle support tickets with priority and status tracking.
- Review activity summaries and dashboard charts.

## Tech stack

- Python 3
- Django 4.2
- SQLite by default
- HTML templates and custom CSS

## Get it running

From the `smart_logistics` directory:

```bash
python -m venv .venv
```

Activate the environment, then install Django:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and sign in with the superuser account you created. The optional `setup.sh` script automates these steps on macOS/Linux.

## Optional sample data

To populate the app with sample employees, goods, tasks, tickets, and work logs:

```bash
python manage.py shell < demo_data.py
```

This creates demo employee accounts named `alice`, `bob`, and `carol`, each with the password `pass1234`. Use these only in a local demo database; change or remove them before exposing an instance to other users.

## Project layout

```
smart_logistics/
├── logistics/          # Models, views, forms, templates, and migrations
├── smart_logistics/    # Django settings and URL configuration
├── static/css/         # Application styles
├── demo_data.py        # Optional sample data loader
├── manage.py
├── requirements.txt
└── setup.sh
```

## Before deploying

This project is set up for local development. Review the Django settings before hosting it: use a private secret key, turn off debug mode, restrict allowed hosts, and configure a production database and static-file serving.

## License

No license has been specified yet. Contact the project owner before reusing or redistributing the code.
