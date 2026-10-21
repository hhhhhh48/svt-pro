import os, re

# 1. التأكد من وجود ملف index.html
if not os.path.exists('templates/index.html'):
    index_html = '''{% extends "base.html" %}
{% block content %}
<div class="pt-32 pb-20 px-6 text-center">
    <h1 class="text-6xl md:text-8xl font-black mb-6 text-white">مرحباً بك في <span class="text-glow">BAC 2026</span></h1>
    <p class="text-xl text-gray-400 mb-10">منصة البكالوريا الشاملة. جاهز للاختبارات؟</p>
    <div class="flex justify-center gap-4">
        <a href="/exams" class="btn-neon px-8 py-4 rounded-xl text-lg font-bold">ابدأ الاختبارات</a>
        <a href="/news" class="glass px-8 py-4 rounded-xl text-lg font-bold text-white hover:bg-white/10">آخر الأخبار</a>
    </div>
</div>
{% endblock %}'''
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✅ تم إنشاء ملف index.html")
else:
    print("ℹ️ ملف index.html موجود بالفعل")

# 2. إضافة مسار الصفحة الرئيسية في app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# حذف أي مسار قديم لـ / لتجنب التكرار
code = re.sub(r"@app\.route\('/'\).*?return.*?\n", "", code, flags=re.DOTALL)

home_route = '''
@app.route('/')
def index():
    try:
        data = load_data()
        return render_template('index.html', streams=data.get('streams', []), tips=data.get('tips', []))
    except Exception as e:
        return f"<h1>Error: {e}</h1>", 500
'''
if "if __name__ == '__main__':" in code:
    code = code.replace("if __name__ == '__main__':", home_route + "\nif __name__ == '__main__':")
else:
    code += home_route

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ تم إضافة مسار '/' (الصفحة الرئيسية) بنجاح!")
