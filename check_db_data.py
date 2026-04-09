import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import User, Profile, HealthLog, TherapyPlan

def check_data():
    print("="*40)
    print("--- 1. USERS & PROFILES ---")
    users = User.objects.all()
    if not users:
        print("No users found.")
    for user in users:
        print(f"User ID: {user.id} | Phone: {user.phone} | Email: {user.email}")
        if hasattr(user, 'profile'):
            p = user.profile
            print(f"  -> Profile: {p.full_name}, Age: {p.age}, Gender: {p.gender}, Blood: {p.blood_group}")
        else:
            print("  -> No Profile attached.")

    print("\n--- 2. HEALTH LOGS ---")
    logs = HealthLog.objects.all()
    if not logs:
        print("No health logs found.")
    for log in logs:
        print(f"Log ID: {log.id} | User: {log.user.phone} | Symptoms: {log.symptoms} | Sleep: {log.sleep_quality}/10 | Digestion: {log.digestion_status} | Activity: {log.activity_level} | Date: {log.created_at.date()}")

    print("\n--- 3. THERAPY PLANS ---")
    plans = TherapyPlan.objects.all()
    if not plans:
        print("No therapy plans found.")
    for plan in plans:
        print(f"Plan ID: {plan.id} | User: {plan.user.phone} | Name: {plan.plan_name} | Status: {plan.status} | Started: {plan.start_date.date()}")
    
    print("="*40)

if __name__ == "__main__":
    check_data()
