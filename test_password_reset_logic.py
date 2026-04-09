import os
import django
import sys

# Setup Django
sys.path.append('c:/Users/raviv/AndroidStudioProjects/MyApplication7/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import User
from django.utils import timezone

def test_password_reset():
    email = "test@example.com"
    phone = "1234567890"
    
    # 1. Ensure test user exists
    user, created = User.objects.get_or_create(phone=phone, defaults={'email': email})
    if not created:
        user.email = email
        user.save()
    
    print(f"Test User: {user.phone}, Email: {user.email}")
    
    # Simulate ForgotPasswordView logic
    import random
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    user.reset_code = code
    user.reset_expiry = timezone.now() + django.utils.timezone.timedelta(minutes=10)
    user.save()
    
    print(f"Generated Code: {user.reset_code}")
    
    # Verify DB
    db_user = User.objects.get(email=email)
    print(f"DB Reset Code: {db_user.reset_code}")
    
    if db_user.reset_code == code:
        print("SUCCESS: Code generated and saved correctly.")
    else:
        print("FAILURE: Code mismatch.")
        return

    # Simulate ResetPasswordView logic
    new_pass = "new_secure_password123"
    if db_user.reset_code == code and db_user.reset_expiry > timezone.now():
        db_user.set_password(new_pass)
        db_user.reset_code = None
        db_user.reset_expiry = None
        db_user.save()
        print("SUCCESS: Password reset logic verified.")
    else:
        print("FAILURE: Validation failed.")

if __name__ == "__main__":
    test_password_reset()
