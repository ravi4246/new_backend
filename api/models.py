from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    reset_expiry = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    # Assessment Data
    initial_symptoms = models.TextField(blank=True, null=True)
    initial_sleep = models.CharField(max_length=100, blank=True, null=True)
    initial_digestion = models.CharField(max_length=100, blank=True, null=True)
    initial_activity = models.CharField(max_length=100, blank=True, null=True)
    habits = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class HealthLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_logs')
    symptoms = models.TextField()  # Comma-separated or JSON
    sleep_quality = models.IntegerField()  # 1-10
    digestion_status = models.CharField(max_length=255)
    activity_level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.user.username} on {self.created_at.date()}"

class TherapyPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_days = models.IntegerField()
    diet_plan = models.TextField()
    herbs_plan = models.TextField()
    lifestyle_plan = models.TextField()
    category = models.CharField(max_length=50)

    class Meta:
        db_table = 'therapy_therapyplan'

    def __str__(self):
        return self.name
