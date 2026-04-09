from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, HealthLog, TherapyPlan

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['full_name', 'age', 'gender', 'blood_group', 'phone', 'email',
                  'initial_symptoms', 'initial_sleep', 'initial_digestion', 
                  'initial_activity', 'habits']

class HealthLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthLog
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class TherapyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapyPlan
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['phone', 'password', 'email', 'profile']

    def validate_phone(self, value):
        if len(value) < 3 or not value.isdigit():
            raise serializers.ValidationError("Phone number must be at least 3 digits.")
        return value

    def validate_password(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Password must be at least 4 characters long.")
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        email = validated_data.get('email')
        
        if not email:
            raise serializers.ValidationError({"email": "Email address is required."})
            
        user = User.objects.create_user(
            phone=validated_data['phone'],
            email=email,
            password=validated_data['password']
        )
        Profile.objects.create(user=user, **profile_data)
        return user
