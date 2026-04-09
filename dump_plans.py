import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import TherapyPlan

def check_data():
    plans = TherapyPlan.objects.all()
    print("--- THERAPY PLANS ---")
    for plan in plans:
        print(f"Plan ID: {plan.id} | Name: {plan.name} | Category: {plan.category}")

if __name__ == "__main__":
    check_data()
