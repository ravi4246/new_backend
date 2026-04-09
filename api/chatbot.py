import google.generativeai as genai
from django.conf import settings
from .models import Profile, HealthLog, TherapyPlan
import logging

logger = logging.getLogger(__name__)

def get_chatbot_response(user, user_message):
    """
    Generates a RAG-based response for the user's message.
    """
    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == 'your_gemini_api_key_here':
        return "I'm sorry, but the AI service is not configured yet. Please add a valid GOOGLE_API_KEY to the backend environment."

    try:
        # 1. Retrieve Context
        profile = getattr(user, 'profile', None)
        logs = HealthLog.objects.filter(user=user).order_by('-created_at')[:5]
        plans = TherapyPlan.objects.all()

        # 2. Build Context String
        context = "### User Profile\n"
        if profile:
            context += f"- Name: {profile.full_name}\n"
            context += f"- Age: {profile.age}\n"
            context += f"- Gender: {profile.gender}\n"
            context += f"- Initial Symptoms: {profile.initial_symptoms}\n"
            context += f"- Habits: {profile.habits}\n"
        else:
            context += "No profile found.\n"

        context += "\n### Recent Health Logs\n"
        for log in logs:
            context += f"- {log.created_at.date()}: Symptoms: {log.symptoms}, Sleep: {log.sleep_quality}/10, Digestion: {log.digestion_status}, Activity: {log.activity_level}\n"

        context += "\n### Available Siddha Therapy Plans (Knowledge Base)\n"
        for plan in plans:
            context += f"- {plan.name}: {plan.description}\n"
            context += f"  - Diet: {plan.diet_plan}\n"
            context += f"  - Herbs: {plan.herbs_plan}\n"
            context += f"  - Lifestyle: {plan.lifestyle_plan}\n"

        # 3. Configure Gemini
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')

        system_prompt = (
            "You are a Siddha AI Health Assistant. Use the provided user context and the therapy plan knowledge base "
            "to answer the user's questions. Always provide advice based on Siddha principles as described in the "
            "knowledge base. If the user's symptoms match a specific plan, recommend it. "
            "Be empathetic, professional, and clear. Keep responses concise and formatted with markdown."
        )

        full_prompt = (
            f"{system_prompt}\n\n"
            f"--- CONTEXT ---\n{context}\n\n"
            f"--- USER QUESTION ---\n{user_message}"
        )

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        logger.error(f"Error in get_chatbot_response: {str(e)}")
        return f"I encountered an error while processing your request: {str(e)}"
