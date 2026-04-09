import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import User, Profile, HealthLog, TherapyPlan
from api.views import AnalysisView
from django.test import RequestFactory
from django.utils import timezone

def test_analysis():
    print("--- Database Check ---")
    plan_count = TherapyPlan.objects.count()
    print(f"Therapy Plans in DB: {plan_count}")
    if plan_count > 0:
        for p in TherapyPlan.objects.all()[:3]:
            print(f" - {p.name} (Cat: {p.category})")

    user_count = User.objects.count()
    print(f"\nUsers in DB: {user_count}")
    
    if user_count == 0:
        print("No users found to test.")
        return

    # Use the first user with a profile
    user = User.objects.filter(profile__isnull=False).first()
    if not user:
        user = User.objects.first()
        print(f"Using user without profile: {user.phone}")
    else:
        print(f"Using user: {user.phone} ({user.profile.full_name})")
        print(f"Symptoms: {user.profile.initial_symptoms}")

    factory = RequestFactory()
    request = factory.get('/api/analysis/')
    request.user = user
    
    view = AnalysisView()
    response = view.get(request)
    
    print("\n--- AI Analysis API Response ---")
    import json
    print(json.dumps(response.data, indent=2))

if __name__ == "__main__":
    test_analysis()
