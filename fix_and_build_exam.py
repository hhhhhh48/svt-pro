import os, re

# 1. إنشاء مجلد templates إذا لم يكن موجوداً
os.makedirs('templates', exist_ok=True)

# 2. إنشاء ملف exam_take.html بالكامل (مع كود Supabase)
html_content = '''{% extends "base.html" %}
{% block title %}{{ exam.subject }} | امتحان{% endblock %}
{% block content %}
<div class="pt-24 pb-20 px-4 max-w-4xl mx-auto">
    <!-- شريط المؤقت -->
    <div class="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 glass px-8 py-4 rounded-full border-2 border-brand-green shadow-[0_0_30px_rgba(0,255,136,0.3)] flex items-center gap-4">
        <i class="fa-solid fa-stopwatch text-2xl text-yellow-400 animate-pulse"></i>
        <div id="timer" class="text-3xl font-black font-mono text-white tracking-widest">...</div>
    </div>

    <div class="text-center mb-10">
        <h1 class="text-3xl md:text-4xl font-black text-white mb-2">{{ exam.subject }}</h1>
        <p class="text-brand-green font-bold">{{ exam.stream }}</p>
    </div>

    <form id="examForm">
        {% for section in exam.sections %}
        <div class="mb-10">
            <div class="bg-brand-green/10 border-r-4 border-brand-green p-4 mb-6 rounded-l-xl">
                <h2 class="text-xl font-bold text-brand-green">{{ section.title }}</h2>
            </div>

            {% if section.type == 'qcm' %}
                {% for q in section.questions %}
                <div class="glass p-6 rounded-2xl mb-4">
                    <p class="text-white font-bold mb-4">{{ loop.index }}. {{ q.q }}</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {% for opt in q.options %}
                        <label class="flex items-center gap-3 p-3 rounded-xl border border-white/10 hover:border-brand-green/50 hover:bg-white/5 cursor-pointer">
                            <input type="radio" name="qcm_{{ section.loop.index }}_{{ loop.index }}" value="{{ loop.index0 }}" class="w-5 h-5 accent-brand-green">
                            <span class="text-gray-300">{{ opt }}</span>
                        </label>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            {% elif section.type == 'text' %}
                {% for ex in section.exercises %}
                <div class="glass p-6 rounded-2xl mb-6">
                    <h3 class="text-lg font-bold text-white mb-4">{{ ex.title }}</h3>
                    <div class="text-gray-300 whitespace-pre-wrap leading-relaxed mb-6">{{ ex.text }}</div>
                    <textarea rows="6" class="w-full bg-black/50 border border-white/10 rounded-xl p-4 text-white focus:border-brand-green outline-none" placeholder="اكتب إجابتك هنا بالتفصيل..."></textarea>
                    <div class="hidden correction-box mt-4 p-4 bg-green-500/10 border border-green-500/20 rounded-xl text-sm">
                        <strong class="text-green-400 block mb-2"><i class="fa-solid fa-check-circle"></i> التصحيح النموذجي:</strong>
                        <div class="text-green-100 whitespace-pre-wrap">{{ ex.correction }}</div>
                    </div>
                </div>
                {% endfor %}
            {% endif %}
        </div>
        {% endfor %}

        <button type="submit" id="submitBtn" class="w-full btn-neon py-5 rounded-2xl text-xl font-black mb-10">تسليم الامتحان وعرض التصحيح</button>
    </form>
</div>

<script>
    // المؤقت
    let time = {{ exam.duration_mins }} * 60;
    const timerEl = document.getElementById('timer');
    const interval = setInterval(() => {
        if(time <= 0) { clearInterval(interval); timerEl.textContent = '00:00:00'; return; }
        time--;
        const h = String(Math.floor(time / 3600)).padStart(2, '0');
        const m = String(Math.floor((time % 3600) / 60)).padStart(2, '0');
        const s = String(time % 60).padStart(2, '0');
        timerEl.textContent = `${h}:${m}:${s}`;
        if(time < 300) timerEl.classList.add('text-red-500');
    }, 1000);

    // عرض التصحيح
    document.getElementById('examForm').addEventListener('submit', function(e) {
        e.preventDefault();
        if(!confirm('هل أنت متأكد من تسليم الامتحان؟')) return;
        clearInterval(interval);
        document.getElementById('timer').style.display = 'none';
        document.querySelectorAll('.correction-box').forEach(box => box.classList.remove('hidden'));
        document.getElementById('submitBtn').style.display = 'none';
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // حفظ النتيجة في Supabase
        const studentName = prompt("أدخل اسمك لحفظ نتيجتك في السجل:", "تلميذ بكالوريا");
        if (studentName) {
            fetch('/api/save-result', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: studentName,
                    exam_id: "{{ exam.id }}",
                    score: 15, // سيتم تعديلها لاحقاً للحساب الفعلي
                    total: 20
                })
            }).then(res => res.json()).then(data => {
                if(data.status === 'success') console.log('✅ تم حفظ النتيجة بنجاح!');
                else console.error('❌ خطأ:', data.message);
            });
        }
    });
</script>
{% endblock %}'''

with open('templates/exam_take.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("✅ تم إنشاء ملف exam_take.html")

# 3. تحديث app.py (تأمين الإعدادات)
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# إزالة الكود القديم لـ Supabase إذا كان موجوداً لتجنب التكرار
if 'from supabase import create_client' in code:
    code = re.sub(r'import os\nfrom dotenv.*?supabase = create_client.*?\n\n', '', code, flags=re.DOTALL)

# إضافة كود Supabase الجديد
supabase_setup = '''import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key) if url and key else None

'''
code = supabase_setup + code

# إضافة المسار إذا لم يكن موجوداً
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
print("✅ تم تحديث app.py وإضافة مسار حفظ النتائج")
