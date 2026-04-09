import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
django.setup()

from api.models import TherapyPlan

def seed_data():
    plans = [
        {
            "name": "Stress & Sleep Reset",
            "description": "A comprehensive protocol focusing on nervous system relaxation, improved sleep hygiene, and mental clarity through Siddha principles.",
            "duration_days": 21,
            "diet_plan": "Satvic diet: include warm milk with nutmeg, almonds, and easily digestible cooked grains. Avoid caffeine and spicy foods.",
            "herbs_plan": "Brahmi Rasayana (5g twice daily) and Ashwagandha tablets (1 twice daily) for stress reduction.",
            "lifestyle_plan": "Daily 15-minute meditation (Pranayama) before bed. Oil massage (Abhyanga) twice a week.",
            "category": "stress"
        },
        {
            "name": "Holistic Digestive Balance",
            "description": "Balance your Agni (digestive fire) to eliminate toxins and restore metabolic harmony. Ideal for acidity and bloating.",
            "duration_days": 14,
            "diet_plan": "Light, warm meals. Ginger tea before meals. Avoid cold drinks, curd at night, and heavy oily foods.",
            "herbs_plan": "Triphala Churna (1 tsp with warm water at night) and Inji Morappa (ginger candy) after meals.",
            "lifestyle_plan": "Vajrasana for 5 mins after meals. Regular walking for 30 mins daily.",
            "category": "digestive"
        },
        {
            "name": "Natural Pain Relief Protocol",
            "description": "Manage inflammation and joint discomfort using traditional Vata-balancing methods.",
            "duration_days": 30,
            "diet_plan": "Anti-inflammatory diet: include turmeric, garlic, and fenugreek. Avoid gas-forming vegetables like cabbage and potato.",
            "herbs_plan": "Shallaki tablets (1 twice daily) and Pinda Thailam for external application on painful joints.",
            "lifestyle_plan": "Gentle stretching and joint movements. Avoid exposure to cold wind and excessive travel.",
            "category": "pain"
        },
        {
            "name": "Metabolic & Weight Regulation",
            "description": "Boost your metabolism and manage energy levels through Kapha-balancing lifestyle and diet.",
            "duration_days": 45,
            "diet_plan": "High fiber, whole grains, and protein. Use honey instead of sugar. Avoid dairy sweets and fried food.",
            "herbs_plan": "Trikatu Churna (pinch with honey twice daily) to boost metabolism.",
            "lifestyle_plan": "Vigorous exercise 1 hour daily. Avoid sleeping during the day.",
            "category": "metabolic"
        },
        {
            "name": "Immunity & Respiratory Support",
            "description": "Strengthen your natural defense system and improve lung health, especially good for frequent colds.",
            "duration_days": 28,
            "diet_plan": "Include Vitamin C rich fruits (Amla), ginger, and basil. Drink warm water throughout the day.",
            "herbs_plan": "Amrutarishta (20ml after meals) and Kabasura Kudineer (once daily for 3 days, then once a week).",
            "lifestyle_plan": "Steam inhalation daily. Kapalbhati Pranayama 10 mins daily.",
            "category": "immunity"
        },
        {
            "name": "Hormonal Harmony Program",
            "description": "Balance hormonal fluctuations and improve reproductive health through targeted nutrition and yoga.",
            "duration_days": 60,
            "diet_plan": "Hormone-balancing fats like Ghee and coconut. Include flax seeds and colorful vegetables. Avoid processed soy.",
            "herbs_plan": "Shatavari Ghrita (1 tsp with warm milk) and Aloe Vera juice (20ml) on empty stomach.",
            "lifestyle_plan": "Yoga asanas focusing on the pelvic area (Butterfly pose, Cobra pose). Regular cycles tracking.",
            "category": "hormonal"
        }
    ]

    print("Cleaning existing plans...")
    TherapyPlan.objects.all().delete()

    print("Seeding new plans...")
    for plan_data in plans:
        plan = TherapyPlan.objects.create(**plan_data)
        print(f"Created plan: {plan.name} (Category: {plan.category})")

    print("\nSeeding complete!")

if __name__ == "__main__":
    seed_data()
