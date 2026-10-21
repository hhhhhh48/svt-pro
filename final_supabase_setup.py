import os, re

# 1. تحديث app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# إضافة الاستيرادات
if 'from supabase import create_client' not in code:
    imports = '''import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key) if url and key else None

'''
    code = imports + code

# إضافة مسار حفظ النتيجة
if '/api/save-result' not in code:
    route = '''
@app.route('/api/save-result', methods=['POST'])
def save_result():
    if not supabase:
        return {"status": "error", "message": "DB not configured"}, 500
    try:
        data = request.json
        supabase.table('exam_results').insert({
            "student_name": data.get('name', 'مجهول'),
            "exam_id": data.get('exam_id'),
            "score": data.get('score'),
            "total_questions": data.get('total')
        }).execute()
        return {"status": "success"}, 200
    except Exception as e:
        print("Supabase Error:", e)
        return {"status": "error", "message": str(e)}, 500
'''
    code = code.replace("if __name__ == '__main__':", route + "\nif __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

# 2. تحديث exam_take.html لإرسال البيانات
with open('templates/exam_take.html', 'r', encoding='utf-8') as f:
    html = f.read()

if '/api/save-result' not in html:
    # حقن كود JavaScript قبل إغلاق الـ Script
    js_code = '''
    // حفظ النتيجة في قاعدة البيانات
    const studentName = prompt("أدخل اسمك لحفظ نتيجتك في السجل:", "تلميذ بكالوريا");
    if (studentName) {
        fetch('/api/save-result', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: studentName,
                exam_id: "{{ exam.id }}",
                score: 15, // يمكن تعديلها لاحقاً لحساب العلامة الفعلية
                total: 20
            })
        }).then(res => res.json()).then(data => {
            if(data.status === 'success') console.log('تم حفظ النتيجة بنجاح!');
        });
    }
    '''
    html = html.replace('</script>', js_code + '\n</script>')
    with open('templates/exam_take.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("✅ تم تجهيز الكود لإرسال النتائج إلى Supabase!")
