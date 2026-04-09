import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import User
from api.chatbot import get_chatbot_response

def run_test():
    import google.generativeai as genai
    from django.conf import settings
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print("Available models:")
        for m in models:
            print(f"- {m}")
    except Exception as e:
        print(f"Failed to list models: {e}")

if __name__ == "__main__":
    run_test()
