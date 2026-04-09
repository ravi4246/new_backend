import os
import django
import sys

# Setup Django
sys.path.append('c:/Users/raviv/AndroidStudioProjects/MyApplication7/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import User

def list_user_emails():
    print("--- REGISTERED USERS ---")
    users = User.objects.all()
    if not users.exists():
        print("No users found in database.")
        return
    
    for user in users:
        print(f"Phone: {user.phone} | Email: {user.email}")

if __name__ == "__main__":
    list_user_emails()
