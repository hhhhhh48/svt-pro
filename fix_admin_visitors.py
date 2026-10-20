import os, re

# 1. قراءة app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 2. حذف أي كود قديم يخص الزوار (لإزالة التعارض)
code = re.sub(r"from visitor_tracker import.*?\n", "", code)
code = re.sub(r"@app\.before_request.*?pass", "", code, flags=re.DOTALL)
code = re.sub(r"@app\.route\('/admin/visitors'\).*?return render_template\('admin_visitors\.html'.*?\)", "", code, flags=re.DOTALL)

# 3. إضافة نظام التتبع الجديد والمحمي (داخل app.py مباشرة)
new_code = '''
# ==================== نظام الزوار الجديد والمحمي ====================
import os as _os, json as _json, datetime as _dt

def get_visitors_path():
    return _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'visitors.json')

@app.before_request
def track_visitors_safe():
    # تجاهل الملفات الثابتة ولوحة التحكم
    if request.path.startswith('/static/') or request.path.startswith('/admin'):
        return
    try:
        ua = request.headers.get('User-Agent', '').lower()
        # حظر البوتات المعروفة
        if any(bot in ua for bot in ['bot', 'crawl', 'spider', 'curl', 'python', 'wget']):
            return
        
        path = get_visitors_path()
        visits = []
        if _os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    visits = _json.load(f)
            except Exception: pass
            
        visits.append({
            "ip": request.remote_addr or "Unknown",
            "ua": request.headers.get('User-Agent', 'Unknown'),
            "path": request.path,
            "time": _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # الاحتفاظ بآخر 500 زيارة فقط
        if len(visits) > 500: visits = visits[-500:]
        
        with open(path, 'w', encoding='utf-8') as f:
            _json.dump(visits, f, ensure_ascii=False, indent=2)
    except Exception:
        pass # إذا فشل أي شيء، الموقع يستمر بالعمل ولا ينهار

@app.route('/admin/visitors')
def admin_visitors():
    if not session.get('admin'): return redirect(url_for('login'))
    try:
        path = get_visitors_path()
        visits = []
        if _os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                visits = _json.load(f)
        visits.reverse() # الأحدث أولاً
        unique_ips = set(v.get('ip', 'Unknown') for v in visits)
        return render_template('admin_visitors.html', total=len(visits), unique=len(unique_ips), visits=visits)
    except Exception as e:
        return f"خطأ: {str(e)}", 500
# ======================================================================

if __name__ == '__main__':'''

code = code.replace("if __name__ == '__main__':", new_code)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

# 4. إنشاء قالب الصفحة بشكل بسيط جداً
html = '''{% extends "base.html" %}
{% block title %}الزوار{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-black text-white">👣 الزوار</h1>
        <a href="/admin" class="px-4 py-2 rounded-xl bg-white/5 text-gray-300 hover:bg-white/10 font-bold">عودة</a>
    </div>
    <div class="grid grid-cols-2 gap-4 mb-8">
        <div class="glass p-6 rounded-2xl border-t-4 border-t-brand-green text-center">
            <div class="text-4xl font-black text-brand-green mb-2">{{ total }}</div>
            <div class="text-sm text-gray-400">إجمالي الزيارات</div>
        </div>
        <div class="glass p-6 rounded-2xl border-t-4 border-t-brand-blue text-center">
            <div class="text-4xl font-black text-brand-blue mb-2">{{ unique }}</div>
            <div class="text-sm text-gray-400">زوار فريدون</div>
        </div>
    </div>
    <div class="glass rounded-3xl overflow-hidden border border-white/10">
        <div class="p-4 bg-white/5 border-b border-white/10 font-bold text-white">آخر الزيارات</div>
        <div class="divide-y divide-white/5">
            {% if visits %}
                {% for v in visits %}
                <div class="p-4 flex flex-col md:flex-row md:items-center gap-3">
                    <div class="md:w-1/3">
                        <p class="text-sm font-bold text-white">{{ v.ip }}</p>
                        <p class="text-xs text-gray-500">{{ v.time }}</p>
                    </div>
                    <div class="md:w-1/3">
                        <span class="bg-white/10 px-2 py-1 rounded text-xs text-gray-300">{{ v.path }}</span>
                    </div>
                    <div class="md:w-1/3 text-xs text-gray-500 truncate">
                        {{ v.ua }}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="p-8 text-center text-gray-500">لا توجد زيارات مسجلة.</div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}'''
with open('templates/admin_visitors.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم إصلاح الكود ودمجه في app.py بأمان تام!")
