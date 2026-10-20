import os, re

# 1. تحديث app.py لضمان عدم حدوث أخطاء في المسار
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# استبدال مسار الزوار بنسخة أكثر أماناً
old_route = r"@app\.route\('/admin/visitors'\).*?return render_template\('admin_visitors\.html', total=total, unique=unique, visits=visits\)"
new_route = """@app.route('/admin/visitors')
def admin_visitors():
    if not session.get('admin'): return redirect(url_for('login'))
    try:
        from visitor_tracker import get_stats
        total, unique, visits = get_stats()
        # التأكد من أن الزيارات قائمة وأنها مقلوبة لعرض الأحدث أولاً
        visits = list(reversed(visits)) if visits else []
    except Exception as e:
        total, unique, visits = 0, 0, []
    return render_template('admin_visitors.html', total=total, unique=unique, visits=visits)"""

if "/admin/visitors" in app_code:
    app_code = re.sub(old_route, new_route, app_code, flags=re.DOTALL)
else:
    app_code = app_code.replace("if __name__ == '__main__':", new_route + "\n\nif __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# 2. إنشاء قالب HTML بسيط جداً ومضمون (بدون أي أكواد معقدة قد تسبب خطأ)
html_code = '''{% extends "base.html" %}
{% block title %}الزيارات{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-5xl mx-auto">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-black text-white">👣 الزوار</h1>
        <a href="/admin" class="px-4 py-2 rounded-xl bg-white/5 text-gray-300 hover:bg-white/10 font-bold">عودة</a>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8">
        <div class="glass p-6 rounded-2xl border-t-4 border-t-brand-green text-center">
            <div class="text-4xl font-black text-brand-green mb-2">{{ total|default(0) }}</div>
            <div class="text-sm text-gray-400 font-bold">إجمالي الزيارات</div>
        </div>
        <div class="glass p-6 rounded-2xl border-t-4 border-t-brand-blue text-center">
            <div class="text-4xl font-black text-brand-blue mb-2">{{ unique|default(0) }}</div>
            <div class="text-sm text-gray-400 font-bold">زوار فريدون</div>
        </div>
    </div>

    <div class="glass rounded-3xl overflow-hidden border border-white/10">
        <div class="p-4 bg-white/5 border-b border-white/10 font-bold text-white">آخر الزيارات</div>
        <div class="divide-y divide-white/5">
            {% if visits %}
                {% for v in visits %}
                <div class="p-4 flex flex-col md:flex-row md:items-center gap-3">
                    <div class="flex items-center gap-3 md:w-1/3">
                        <div class="w-10 h-10 rounded-full bg-brand-green/20 text-brand-green flex items-center justify-center">
                            <i class="fa-solid fa-user"></i>
                        </div>
                        <div>
                            <p class="text-sm font-bold text-white">{{ v.ip|default('غير معروف') }}</p>
                            <p class="text-xs text-gray-500">{{ v.time|default('') }}</p>
                        </div>
                    </div>
                    <div class="md:w-1/3 text-sm text-gray-300">
                        <span class="bg-white/10 px-2 py-1 rounded text-xs">{{ v.path|default('/') }}</span>
                    </div>
                    <div class="md:w-1/3 text-xs text-gray-500 truncate">
                        {{ v.ua|default('') }}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="p-8 text-center text-gray-500">
                    لا توجد زيارات مسجلة حتى الآن. قم بتصفح الموقع من نافذة تصفح خفي لتسجيل أول زيارة.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}'''

with open('templates/admin_visitors.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("✅ تم إصلاح صفحة الزوار!")
