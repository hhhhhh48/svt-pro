# -*- coding: utf-8 -*-
"""يملأ attempts.json ببيانات وهمية لاختبار لوحة الصدارة"""
import json, os
from datetime import datetime

ATTEMPTS_FILE = 'data/attempts.json'
week_key = f"{datetime.now().year}-W{datetime.now().isocalendar()[1]:02d}"

fake_users = [
    {"user_name": "ياسمين ب.", "subject_id": "science", "score": 38, "total": 40},
    {"user_name": "ياسمين ب.", "subject_id": "physics", "score": 35, "total": 40},
    {"user_name": "أمين ك.", "subject_id": "math", "score": 37, "total": 40},
    {"user_name": "أمين ك.", "subject_id": "science", "score": 33, "total": 40},
    {"user_name": "سارة م.", "subject_id": "physics", "score": 40, "total": 40},
    {"user_name": "سارة م.", "subject_id": "math", "score": 36, "total": 40},
    {"user_name": "محمد ع.", "subject_id": "science", "score": 30, "total": 40},
    {"user_name": "ليلى ح.", "subject_id": "math", "score": 39, "total": 40},
    {"user_name": "ليلى ح.", "subject_id": "physics", "score": 32, "total": 40},
    {"user_name": "كمال ر.", "subject_id": "science", "score": 28, "total": 40},
]

attempts = []
if os.path.exists(ATTEMPTS_FILE):
    with open(ATTEMPTS_FILE, 'r', encoding='utf-8') as f:
        attempts = json.load(f)
    # احذف البيانات الوهمية القديمة إن وجدت
    attempts = [a for a in attempts if not a.get('_test')]

for i, u in enumerate(fake_users):
    attempts.append({
        'id': f'test_{i}',
        'user_name': u['user_name'],
        'subject_id': u['subject_id'],
        'unit_id': 'all',
        'score': u['score'],
        'total': u['total'],
        'duration_sec': 1500 + i * 30,
        'week_key': week_key,
        'created_at': datetime.now().isoformat(),
        'answers': [],
        '_test': True
    })

with open(ATTEMPTS_FILE, 'w', encoding='utf-8') as f:
    json.dump(attempts, f, ensure_ascii=False, indent=2)

print(f"✅ أضفنا {len(fake_users)} محاولة تجريبية لـ {week_key}")
print(f"📊 المجموع الكلي في الملف: {len(attempts)} محاولة")
