import os
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

def count_plans():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM therapy_therapyplan")
        count = cursor.fetchone()[0]
        print(f"Number of plans in therapy_therapyplan: {count}")
        
        cursor.execute("SELECT id, name FROM therapy_therapyplan")
        plans = cursor.fetchall()
        for plan_id, name in plans:
            print(f"ID: {plan_id} | Name: {name}")

if __name__ == "__main__":
    count_plans()
