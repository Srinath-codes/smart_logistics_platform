#!/bin/bash
# ─────────────────────────────────────────────────
#  SmartLogix — Smart Logistics Platform
#  Quick Setup Script
# ─────────────────────────────────────────────────

set -e
echo ""
echo "  ██████╗ ███╗   ███╗ █████╗ ██████╗ ████████╗"
echo "  ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝"
echo "  ███████╗██╔████╔██║███████║██████╔╝   ██║   "
echo "  ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   "
echo "  ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   "
echo "  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   "
echo "  LOGIX — Smart Logistics Platform"
echo ""

# 1. Create virtual environment
echo "→ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install Django
echo "→ Installing dependencies..."
pip install -r requirements.txt --quiet

# 3. Run migrations
echo "→ Running migrations..."
python manage.py makemigrations logistics
python manage.py migrate

# 4. Create superuser
echo ""
echo "→ Create Admin (Superuser) Account"
python manage.py createsuperuser

# 5. Optional: load demo data
echo ""
read -p "→ Load demo data? (y/n): " load_demo
if [ "$load_demo" = "y" ]; then
  python manage.py shell < demo_data.py
  echo "✓ Demo data loaded."
fi

# 6. Start server
echo ""
echo "✓ Setup complete!"
echo "→ Starting development server at http://127.0.0.1:8000"
echo ""
python manage.py runserver
