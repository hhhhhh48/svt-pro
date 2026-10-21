import json
import os

os.makedirs("data", exist_ok=True)

subjects = [
    {"id": "science", "name": "علوم الطبيعة والحياة",
     "streams": ["علوم تجريبية", "رياضيات"], "icon": "🧬", "order": 1}
]

units = [
    {"id": "science_protein", "subjectId": "science",
     "name": "تركيب البروتين", "order": 1, "questionCount": 1}
]

questions = [
    {
        "id": "q_sci_prot_001",
        "subjectId": "science",
        "unitId": "science_protein",
        "type": "qcm",
        "difficulty": 2,
        "source": "bac_2019",
        "status": "published",
        "question": "أي العضيات التالية مسؤولة عن ترجمة المعلومة الوراثية إلى بروتين؟",
        "options": [
            {"id": "a", "text": "الميتوكوندري"},
            {"id": "b", "text": "الريبوزوم"},
            {"id": "c", "text": "الشبكة الإندوبلازمية"},
            {"id": "d", "text": "جهاز غولجي"}
        ],
        "correctOptionId": "b",
        "explanation": "الريبوزوم هو مقر الترجمة، حيث يتم قراءة الـARNm وربط الأحماض الأمينية لتشكيل السلسلة الببتيدية.",
        "tags": ["ترجمة", "ريبوزوم"]
    }
]

for name, data in [("subjects", subjects), ("units", units), ("questions", questions)]:
    with open(f"data/{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ data/{name}.json ({len(data)} عنصر)")

print("🎉 تم تجهيز كل البيانات")
