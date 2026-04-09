import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from api.views import AnalysisView
from django.contrib.auth import get_user_model
import traceback

User = get_user_model()
users = User.objects.all()

if not users:
    print("No users found")
    sys.exit(1)

factory = APIRequestFactory()

for user in users:
    print(f"--- Testing user {user.phone} ---")
    request = factory.get('/api/analysis/')
    force_authenticate(request, user=user)

    try:
        response = AnalysisView.as_view()(request)
        print("STATUS:", response.status_code)
        if hasattr(response, 'data'):
             print("PLAN:", response.data.get('recommended_plan'))
             print("CONF:", response.data.get('confidence_score'))
        else:
             print("DATA:", response.content)
    except Exception as e:
        traceback.print_exc()

