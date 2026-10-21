import re, os

# اقرأ الكود
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. احذف كل أسطر الاستيراد المسببة للمشاكل
remove_patterns = [
    r'^from supabase import.*$',
    r'^from dotenv import.*$',
    r'^import supabase.*$',
    r'^load_dotenv\(\).*$',
    r'^try:\s*$',
    r'^\s*from dotenv import load_dotenv\s*$',
    r'^\s*load_dotenv\(\)\s*$',
    r'^\s*except ImportError:\s*$',
    r'^\s*pass\s*$',
    r'^supabase\s*=.*$',
]
lines = code.split('\n')
cleaned = []
skip_next = False
for line in lines:
    skip = False
    for pat in remove_patterns:
        if re.match(pat, line):
            skip = True
            break
    if not skip:
        cleaned.append(line)
code = '\n'.join(cleaned)

# 2. احذف أي مسار save-result قديم
code = re.sub(
    r"@app\.route\('/api/save-result'.*?(?=@app\.route|if __name__)",
    "",
    code,
    flags=re.DOTALL
)

# 3. أضف import urllib
if 'import urllib.request' not in code:
    code = 'import urllib.request\n' + code

# 4. أضف دالة الحفظ الجديدة قبل التشغيل
new_route = '''@app.route('/api/save-result', methods=['POST'])
def save_result():
    data = request.json or {}
    url = os.environ.get('SUPABASE_URL', '')
    key = os.environ.get('SUPABASE_KEY', '')
    if not url or not key:
        return {'status': 'error', 'msg': 'Not configured'}, 500
    try:
        payload = json.dumps({
            'student_name': data.get('name', 'مجهول'),
            'exam_id': data.get('exam_id', ''),
            'score': int(data.get('score', 0)),
            'total_questions': int(data.get('total', 20))
        }).encode('utf-8')
        req = urllib.request.Request(
            url + '/rest/v1/exam_results',
            data=payload,
            headers={
                'apikey': key,
                'Authorization': 'Bearer ' + key,
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {'status': 'success' if resp.status in (200, 201) else 'error'}, 200
    except Exception as e:
        print('Save error:', e)
        return {'status': 'error', 'msg': str(e)}, 500

if __name__ == '__main__':'''

code = code.replace("if __name__ == '__main__':", new_route)

# 5. نظف requirements
with open('requirements.txt', 'w') as f:
    f.write("Flask==3.0.0\nWerkzeug==3.0.1\ngunicorn==21.2.0\n")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

# تحقق نهائي
print("=" * 50)
print("🔍 فحص أول 15 سطر من app.py:")
with open('app.py', encoding='utf-8') as f:
    for i, line in enumerate(f.readlines()[:15], 1):
        print(f"{i:2}. {line.rstrip()}")
print("=" * 50)
print("🔍 البحث عن أي أثر لـ supabase أو dotenv:")
bad = os.popen("grep -nE 'supabase|dotenv' app.py | grep -vE 'SUPABASE_|save_result|save_to'").read()
print(bad if bad.strip() else "  ✅ لا يوجد أي أثر — الكود نظيف تماماً!")
print("=" * 50)
print("✅ تم كل شيء!")
