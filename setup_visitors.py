import os, re

# 1. إنشاء ملف التتبع
tracker_code = '''import json, os, datetime

BOT_KEYWORDS = ['bot', 'crawl', 'spider', 'slurp', 'baidu', 'yandex', 'bing', 'googlebot', 'ahrefs', 'semrush', 'python-requests', 'curl', 'wget', 'scrapy', 'httpclient', 'java', 'headlesschrome', 'phantomjs', 'selenium', 'puppeteer']

def is_human(user_agent):
    if not user_agent: return False
    ua_lower = user_agent.lower()
    return not any(k in ua_lower for k in BOT_KEYWORDS)

def load_visits():
    if not os.path.exists('visitors.json'): return []
    try:
        with open('visitors.json', 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

def save_visits(visits):
    with open('visitors.json', 'w', encoding='utf-8') as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)

def log_visit(ip, ua, path):
    visits = load_visits()
    visits.append({
        "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ip": ip, "ua": ua, "path": path
    })
    # الاحتفاظ بآخر 500 زيارة فقط
    if len(visits) > 500: visits = visits[-500:]
    save_visits(visits)

def get_stats():
    visits = load_visits()
    return len(visits), len(set(v['ip'] for v in visits)), visits
'''
with open('visitor_tracker.py', 'w', encoding='utf-8') as f:
    f.write(tracker_code)

# 2. تعديل app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

if 'from visitor_tracker import' not in app_code:
    app_code = app_code.replace('from data import', 'from visitor_tracker import is_human, log_visit, get_stats\nfrom data import')

if '@app.before_request' not in app_code:
    hook = '''
@app.before_request
def track_visitors():
    if request.path.startswith('/static/') or request.path.startswith('/admin'):
        return
    ua = request.headers.get('User-Agent', '')
    if is_human(ua):
        log_visit(request.remote_addr, ua, request.path)
'''
    app_code = app_code.replace("app.jinja_env.filters['youtube_id'] = get_youtube_id", "app.jinja_env.filters['youtube_id'] = get_youtube_id\n" + hook)

if '/admin/visitors' not in app_code:
    route = '''
@app.route('/admin/visitors')
def admin_visitors():
    if not session.get('admin'): return redirect(url_for('login'))
    total, unique, visits = get_stats()
    visits.reverse() # الأحدث أولاً
    return render_template('admin_visitors.html', total=total, unique=unique, visits=visits)
'''
    app_code = app_code.replace("if __name__ == '__main__':", route + "\nif __name__ == '__main__':")

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_code)

# 3. إنشاء صفحة العرض admin_visitors.html
html_code = '''{% extends "base.html" %}
{% block title %}الزيارات | لوحة التحكم{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-5xl mx-auto">
    <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
            <h1 class="text-3xl font-black text-white">👣 الزوار الحقيقيون</h1>
            <p class="text-gray-400 mt-1">تتبع التلاميذ الذين دخلوا الموقع</p>
        </div>
        <a href="/admin" class="px-4 py-2 rounded-xl bg-white/5 text-gray-300 hover:bg-white/10 transition font-bold">
            <i class="fa-solid fa-arrow-right ml-1"></i> عودة للوحة
        </a>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8">
        <div class="glass p-6 rounded-2xl border-t-4 border-t-brand-green text-center">
            <div class="text-4xl font-black text-brand-green mb-2">{{ total }}</div>
            <div class="text-sm text-gray-400 font-bold">إجمالي الزيارات</div>
        </div>
        <div class="glass p-6 rounded-2xl border-t-4 border-t-brand-blue text-center">
            <div class="text-4xl font-black text-brand-blue mb-2">{{ unique }}</div>
            <div class="text-sm text-gray-400 font-bold">زوار فريدون (IP)</div>
        </div>
    </div>

    <div class="glass rounded-3xl overflow-hidden border border-white/10">
        <div class="p-4 bg-white/5 border-b border-white/10 font-bold text-white">آخر الزيارات</div>
        <div class="divide-y divide-white/5">
            {% for v in visits %}
            <div class="p-4 hover:bg-white/5 transition flex flex-col md:flex-row md:items-center gap-3">
                <div class="flex items-center gap-3 md:w-1/3">
                    <div class="w-10 h-10 rounded-full bg-brand-green/20 text-brand-green flex items-center justify-center text-sm">
                        <i class="fa-solid fa-user"></i>
                    </div>
                    <div>
                        <p class="text-sm font-bold text-white">{{ v.ip }}</p>
                        <p class="text-xs text-gray-500">{{ v.time }}</p>
                    </div>
                </div>
                <div class="md:w-1/3 text-sm text-gray-300">
                    <span class="bg-white/10 px-2 py-1 rounded text-xs">{{ v.path }}</span>
                </div>
                <div class="md:w-1/3 text-xs text-gray-500 truncate" title="{{ v.ua }}">
                    {{ v.ua[:50] }}...
                </div>
            </div>
            {% endfor %}
            {% if not visits %}
            <div class="p-8 text-center text-gray-500">لا توجد زيارات مسجلة بعد.</div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}'''
with open('templates/admin_visitors.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

# 4. تعديل admin.html لإضافة زر الزوار
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

if '/admin/visitors' not in admin_html:
    old_btn = '<a href="/admin/logout"'
    new_btn = '''<a href="/admin/visitors" class="px-4 py-2 rounded-xl bg-brand-green/20 text-brand-green font-bold hover:bg-brand-green/30 transition mr-2">
        <i class="fa-solid fa-users ml-1"></i> الزوار
    </a>
    ''' + old_btn
    admin_html = admin_html.replace(old_btn, new_btn)
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_html)

print("✅ تم إعداد نظام تتبع الزوار بنجاح!")
