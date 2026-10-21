import re, os

# 1. قراءة الكود وحذف أي أثر لـ supabase أو dotenv
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'from supabase' in line or 'import supabase' in line or 'supabase =' in line:
        continue
    if 'dotenv' in line or 'load_dotenv' in line:
        continue
    new_lines.append(line)

code = "".join(new_lines)

# 2. إضافة import requests إذا لم يكن موجوداً
if 'import requests' not in code:
    code = "import requests\n" + code

# 3. حذف مسار الحفظ القديم إذا كان موجوداً
code = re.sub(r"@app\.route\('/api/save-result'\).*?(?=@app\.route|if __name__)", "", code, flags=re.DOTALL)

# 4. كتابة دالة الحفظ الجديدة والآمنة
new_route = '''
def save_to_supabase(name, exam_id, score, total):
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    if not url or not key:
        return False
    headers = {'apikey': key, 'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    payload = {'student_name': name, 'exam_id': exam_id, 'score': score, 'total_questions': total}
    try:
        res = requests.post(f'{url}/rest/v1/exam_results', json=payload, headers=headers, timeout=10)
        return res.status_code in [200, 201]
    except:
        return False

@app.route('/api/save-result', methods=['POST'])
def save_result():
    data = request.json
    success = save_to_supabase(
        name=data.get('name', 'مجهول'),
        exam_id=data.get('exam_id'),
        score=data.get('score'),
        total=data.get('total')
    )
    return {'status': 'success' if success else 'error'}, 200 if success else 500

if __name__ == '__main__':'''

# إضافة المسار قبل التشغيل
if '/api/save-result' not in code:
    code = code.replace("if __name__ == '__main__':", new_route)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

# 5. كتابة ملف requirements بشكل نظيف
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write("Flask==3.0.0\nWerkzeug==3.0.1\ngunicorn==21.2.0\nrequests\n")

print("✅ تم تنظيف الكود بالكامل وحذف supabase القديمة!")
print("⬇️ أول 5 أسطر من الكود الآن:")
for i, line in enumerate(open('app.py', encoding='utf-8').readlines()[:5]):
    print(f"{i+1}: {line.strip()}")
