import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import TherapyCatalog

count = TherapyCatalog.objects.count()
print(f"Total Backup Therapy Plans: {count}")
for plan in TherapyCatalog.objects.all()[:3]:
    print(f"- {plan.name}: {plan.duration_days} days")
