import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import User, Profile, TherapyPlan
from django.test import RequestFactory
from rest_framework.test import force_authenticate
from api.views import AnalysisView

def test_symptoms(symptoms_str, digestion, sleep_qual):
    print(f"\nTesting with symptoms: '{symptoms_str}', digestion: '{digestion}', sleep: '{sleep_qual}'")
    profile = Profile.objects.exclude(user=None).first()
    if not profile:
        print("No valid profile found")
        return
    user = profile.user
    old_sym = profile.initial_symptoms
    old_dig = profile.initial_digestion
    old_slp = profile.initial_sleep
    
    profile.initial_symptoms = symptoms_str
    profile.initial_digestion = digestion
    profile.initial_sleep = sleep_qual
    profile.save()
    
    factory = RequestFactory()
    request = factory.get('/api/analysis/')
    force_authenticate(request, user=user)
    
    response = AnalysisView.as_view()(request)
    data = response.data
    
    print(f"Confidence Score: {data.get('confidence_score')}")
    print(f"Risk Level: {data.get('risk_level')}")
    print(f"Recommendation: {data.get('recommendation')}")
    plan = data.get('recommended_plan', {})
    print(f"Plan: {plan.get('name')} | Category: {plan.get('description', '')[:50]}")
    
    # Restore
    profile.initial_symptoms = old_sym
    profile.initial_digestion = old_dig
    profile.initial_sleep = old_slp
    profile.save()

test_symptoms("headache, acidity, skin problems", "poor", "good")
test_symptoms("joint pain, back pain", "good", "poor")
test_symptoms("fatigue, cold/cough", "good", "good")
test_symptoms("", "good", "good")

