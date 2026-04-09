import csv
import random
import os

def generate_dataset(filename="siddha_ai_training_data.csv", num_rows=45231):
    symptoms_list = [
        "headache, fatigue", "joint pain, back pain", "acidity, bloating", 
        "cold, cough, low immunity", "skin rash, itching", "sleeplessness, anxiety",
        "stomach pain, indigestion", "weight gain, sluggishness", "fever, body ache",
        "hair fall, dandruff", "breathing difficulty, asthma", "muscle cramps"
    ]
    
    digestion_list = ["excellent", "good", "average", "poor"]
    sleep_list = ["excellent", "good", "disturbed", "poor"]
    activity_list = ["high", "moderate", "low", "sedentary"]
    
    therapy_plans = [
        "Vata Dosha Regimen", "Pitta Dosha Regimen", "Kapha Dosha Regimen",
        "General Immunity Booster Regimen", "Digestive Health Regimen",
        "Skin & Hair Radiance Regimen", "Stress Relief Regimen",
        "Joint & Bone Health Regimen", "Respiratory Health Regimen",
        "Weight Management Regimen"
    ]

    print(f"Generating {num_rows} rows of fake training data...")
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'age', 'gender', 'symptoms', 'digestion', 'sleep_quality', 'activity_level', 'target_therapy_plan'])
            
            for i in range(1, num_rows + 1):
                age = random.randint(18, 75)
                gender = random.choice(['Male', 'Female', 'Other'])
                symptoms = random.choice(symptoms_list)
                digestion = random.choice(digestion_list)
                sleep = random.choice(sleep_list)
                activity = random.choice(activity_list)
                plan = random.choice(therapy_plans)
                
                writer.writerow([f"USR{i:05d}", age, gender, symptoms, digestion, sleep, activity, plan])
                
        print(f"Successfully created {filename} ({os.path.getsize(filename)/(1024*1024):.2f} MB)")
    except Exception as e:
        print("Error saving:", str(e))

if __name__ == "__main__":
    generate_dataset()
