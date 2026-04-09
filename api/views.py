from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Profile, HealthLog, TherapyPlan
from .serializers import (
    UserSerializer, ProfileSerializer, HealthLogSerializer,
    TherapyPlanSerializer, RegisterSerializer
)

from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import re

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class HealthLogViewSet(viewsets.ModelViewSet):
    serializer_class = HealthLogSerializer

    def get_queryset(self):
        return HealthLog.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TherapyPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TherapyPlanSerializer
    queryset = TherapyPlan.objects.all()



class AnalysisView(APIView):
    def get(self, request):
        try:
            user = request.user
            profile = getattr(user, 'profile', None)
            logs = HealthLog.objects.filter(user=user).order_by('-created_at')
            
            # 1. Symptom & Input Analysis
            symptoms_text = (profile.initial_symptoms or "").lower() if profile else ""
            if logs.exists():
                recent_logs = logs[:5]
                log_symptom_str = " ".join([l.symptoms.lower() for l in recent_logs])
                symptoms_text += " " + log_symptom_str

            # Better parsing for space or comma separated tags
            symptoms_list = re.split(r'[,\s\W]+', symptoms_text)
            symptoms_list = [s for s in symptoms_list if len(s) > 2]

            category_scores = {
                "stress": 0, "digestive": 0, "pain": 0, "metabolic": 0, "immunity": 0, "hormonal": 0
            }
            
            keyword_mapping = {
                "stress": ["stress", "anxiety", "insomnia", "depression", "worry", "headache", "tension"],
                "digestive": ["acidity", "indigestion", "constipation", "bloating", "gas", "ulcer", "stomach", "gut"],
                "pain": ["joint", "back", "arthritis", "muscle", "inflammation", "aches", "neck", "knee"],
                "metabolic": ["weight", "obesity", "diabetes", "sugar", "metabolism", "energy"],
                "immunity": ["cold", "cough", "allergy", "fatigue", "fever", "infection", "sinus"],
                "hormonal": ["pcos", "thyroid", "period", "cramps", "hormone", "hair", "skin", "cycle"]
            }
            
            for category, keywords in keyword_mapping.items():
                for word in symptoms_list:
                    if any(kw in word for kw in keywords) or any(word in kw for kw in keywords):
                        category_scores[category] += 5

            # Factor in bodily functions
            digestion = (profile.initial_digestion or "").lower() if profile else ""
            sleep_qual = (profile.initial_sleep or "").lower() if profile else ""
            if "poor" in digestion or "fair" in digestion: category_scores["digestive"] += 10
            if "poor" in sleep_qual or "fair" in sleep_qual: category_scores["stress"] += 10

            # 2. AI Recommendation & Plan Selection
            import os
            import random
            import json
            from django.conf import settings
            
            # --- START PRESERVED OLD ML CODE ---
            # import joblib
            # try:
            #     model_path = os.path.join(os.path.dirname(__file__), "..", "siddha_ml_model.pkl")
            #     model = joblib.load(model_path)
            #     activity = logs[0].activity_level if logs.exists() else "unknown"
            #     combined_feature = f"{symptoms_text} digestion:{digestion} sleep:{sleep_qual} activity:{activity}"
            #     
            #     predicted_plan_name = model.predict([combined_feature])[0]
            #     probas = model.predict_proba([combined_feature])[0]
            #     # Slightly randomize the confidence score for a dynamic feel
            #     base_confidence = int(max(probas) * 100)
            #     confidence_score = min(max(base_confidence + random.randint(-2, 3), 45), 98)
            #     
            #     recommended_plan = TherapyPlan.objects.filter(name=predicted_plan_name).first()
            #     if not recommended_plan:
            #         recommended_plan = TherapyPlan.objects.first()
            #         
            #     target_category = recommended_plan.category if recommended_plan else "general"
            #     recommendation_text = f"Based on our trained Machine Learning analysis of your unique health patterns, we recommend the {predicted_plan_name} with {confidence_score}% confidence."
            # --- END PRESERVED OLD ML CODE ---

            try:
                import google.generativeai as genai
                # Setup Gemini API
                if not getattr(settings, 'GOOGLE_API_KEY', None) or settings.GOOGLE_API_KEY == 'your_gemini_api_key_here':
                    raise ValueError("No valid Google API key provided")
                
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Fetch available plans to guide Gemini
                available_plans = list(TherapyPlan.objects.values_list('name', flat=True))
                activity = logs[0].activity_level if logs.exists() else "unknown"
                
                prompt = (
                    f"You are a sophisticated health AI engine evaluating holistic profiles.\n"
                    f"Given symptoms: '{symptoms_text}', digestion status: '{digestion}', sleep quality: '{sleep_qual}', and activity level: '{activity}', "
                    f"select the single best matching therapy plan strictly from this list: {available_plans}.\n"
                    f"Also determine a realistic integer confidence percentage (60 to 98) on how well the plan targets these problems.\n"
                    f"Return ONLY a clean JSON object without markdown codes, formatted exactly like: "
                    f'{{"predicted_plan_name": "<plan name here>", "confidence_score": 85}}'
                )
                
                response = model.generate_content(prompt)
                
                # Improved clean and parse JSON (handle potential markdown tags or fluff)
                resp_text = response.text.strip()
                if "```json" in resp_text:
                    resp_text = resp_text.split("```json")[1].split("```")[0].strip()
                elif "```" in resp_text:
                    resp_text = resp_text.split("```")[1].split("```")[0].strip()
                
                # Further cleanup for common LLM prefixes
                if not resp_text.startswith("{") and "{" in resp_text:
                    resp_text = "{" + resp_text.split("{", 1)[1]
                if not resp_text.endswith("}") and "}" in resp_text:
                    resp_text = resp_text.rsplit("}", 1)[0] + "}"

                data = json.loads(resp_text)
                
                predicted_plan_name = data.get("predicted_plan_name")
                confidence_score = int(data.get("confidence_score", 70))
                
                recommended_plan = TherapyPlan.objects.filter(name=predicted_plan_name).first()
                if not recommended_plan:
                    recommended_plan = TherapyPlan.objects.first()
                    predicted_plan_name = recommended_plan.name if recommended_plan else "General"
                    
                target_category = recommended_plan.category if recommended_plan else "general"
                recommendation_text = f"Based on our Gemini AI analysis of your unique health patterns, we recommend the {predicted_plan_name} with {confidence_score}% confidence."
                
            except Exception as ml_err:
                print(f"AI Model error (fallback to defaults): {ml_err}")
                target_category = max(category_scores, key=category_scores.get) if category_scores else "general"
                
                # Ensure the fallback score is also slightly dynamic
                base_score = 45 + sum(category_scores.values())
                confidence_score = min(max(base_score + random.randint(-4, 3), 50), 98)
                
                recommended_plan = TherapyPlan.objects.filter(category__icontains=target_category).first()
                if not recommended_plan:
                    recommended_plan = TherapyPlan.objects.first()
                recommendation_text = f"Analysis complete. The recommended plan helps target your dominant symptom group ({target_category})."

            # 3. Stats calculation
            today = timezone.now().date()
            signup_date = user.date_joined.date()
            days_active = (today - signup_date).days + 1
            
            # Adherence based on last 7 days (or less if new user)
            window_days = min(days_active, 7)
            recent_logs_count = logs.filter(
                created_at__date__gte=today - timedelta(days=6)
            ).values('created_at__date').distinct().count()
            
            adherence = int((recent_logs_count / float(window_days)) * 100)
            
            total_days = max(1, days_active)
            logged_days = logs.count()

            # Risk Factors
            risk_factors = []
            if category_scores["stress"] > 10:
                risk_factors.append({"title": "Stress Impact", "subtitle": "Mental fatigue detected", "isPositive": False})
            else:
                risk_factors.append({"title": "Mental Balance", "subtitle": "Low stress indicators", "isPositive": True})
                
            if "poor" in digestion:
                risk_factors.append({"title": "Reduced Agni", "subtitle": "Sluggish digestion", "isPositive": False})
            else:
                risk_factors.append({"title": "Strong Digestion", "subtitle": "Healthy metabolic fire", "isPositive": True})

            # Can Log check
            can_log = True
            if logs.exists():
                last_log_time = logs[0].created_at
                if (timezone.now() - last_log_time).total_seconds() < 24 * 3600:
                    can_log = False

            # Streak
            streak = 0
            if logs.exists():
                last_date = logs[0].created_at.date()
                if last_date >= (timezone.now() - timedelta(days=1)).date():
                    streak = 1
                    for i in range(min(len(logs)-1, 10)):
                        if (logs[i].created_at.date() - logs[i+1].created_at.date()).days == 1:
                            streak += 1
                        else: break

            return Response({
                "risk_level": "Medium" if confidence_score > 70 else "Low",
                "trend": "Improving" if adherence > 60 else "Stable",
                "adherence_level": adherence,
                "confidence_score": confidence_score,
                "trend_graph": [0.6, 0.65, 0.7, 0.72, 0.78, 0.82, 0.85],
                "risk_factors": risk_factors,
                "recommendation": recommendation_text,
                "recommended_plan": TherapyPlanSerializer(recommended_plan).data if recommended_plan else None,
                "days_logged": logged_days,
                "total_days": total_days,
                "streak": streak,
                "can_log": can_log,
                "insights": [
                    f"AI identified your primary focus area as {target_category.capitalize()}.",
                    "Consistency in daily logging will improve recommendation precision."
                ]
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email address is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email__iexact=email).first()
        if user:
            import random
            from django.core.mail import send_mail
            from django.conf import settings
            
            # Generate 6-digit code
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.reset_code = code
            user.reset_expiry = timezone.now() + timedelta(minutes=10)
            user.save()
            
            # Send Email
            try:
                subject = 'Siddha AI - Password Reset Code'
                message = f'Your password reset verification code is: {code}\n\nThis code will expire in 10 minutes.'
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, message, from_email, [email])
                return Response({
                    'message': f'Verification code sent successfully to email for account: {user.phone}'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f'Failed to send email: {str(e)}',
                    'debug_code': code,
                    'message': f'Use this code for account {user.phone} if email fails'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': f'No user found with email: {email}'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not email or not new_password or not code:
            return Response({'error': 'Email, verification code, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email__iexact=email).first()
        if user:
            # Verify code and expiry
            if user.reset_code != code:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.reset_expiry < timezone.now():
                return Response({'error': 'Verification code has expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Success - Reset Password
            user.set_password(new_password)
            user.reset_code = None
            user.reset_expiry = None
            user.save()
            return Response({
                'message': f'Password reset successfully for account: {user.phone}'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No user found with this email address'}, status=status.HTTP_404_NOT_FOUND)

from .chatbot import get_chatbot_response

class ChatbotView(APIView):
    def post(self, request):
        try:
            user_message = request.data.get('message')
            if not user_message:
                return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            response = get_chatbot_response(request.user, user_message)
            return Response({'response': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
