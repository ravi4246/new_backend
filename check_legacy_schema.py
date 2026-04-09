import os
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

def check_schema():
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE therapy_therapyplan")
        columns = cursor.fetchall()
        print("Columns in therapy_therapyplan:")
        for col in columns:
            print(col)

if __name__ == "__main__":
    check_schema()
