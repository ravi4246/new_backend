import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from django.conf import settings
print("=== DATABASE CONFIG ===")
print("ENGINE:", settings.DATABASES['default']['ENGINE'])
print("NAME:", settings.DATABASES['default']['NAME'])

from api.models import TherapyPlan, User
print("\n=== DJANGO MODEL COUNTS ===")
print("Users:", User.objects.count())
print("TherapyPlans:", TherapyPlan.objects.count())

from django.db import connection
print("\n=== RAW TABLES IN DB ===")
try:
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print([t[0] for t in tables])
        
        # Check if there is a 'therapy_plans' table that is not 'api_therapyplan'
        # Check schemas
        for tbl in ['api_therapyplan', 'therapy_therapyplan']:
            if tbl in [t[0] for t in tables]:
                cursor.execute(f"DESCRIBE {tbl}")
                print(f"\nSchema for '{tbl}':")
                for row in cursor.fetchall():
                    print(row)
            
except Exception as e:
    print("Could not fetch raw tables:", e)
