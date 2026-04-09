from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, ProfileView, HealthLogViewSet,
    TherapyPlanViewSet, AnalysisView, ForgotPasswordView, ResetPasswordView,
    ChatbotView
)

router = DefaultRouter()
router.register(r'health-logs', HealthLogViewSet, basename='healthlog')
router.register(r'therapy-plans', TherapyPlanViewSet, basename='therapyplan')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('analysis/', AnalysisView.as_view(), name='analysis'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('chat/', ChatbotView.as_view(), name='chatbot'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
