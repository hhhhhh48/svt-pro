import os, re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# إزالة أي كود قديم للتتبع لتجنب التعارض
code = re.sub(r"# ==================== نظام الزوار.*?# ======================================================================", "", code, flags=re.DOTALL)

new_tracker = '''
# ==================== نظام الزوار المتقدم ====================
import os as _os, json as _json, datetime as _dt, uuid

def get_visitors_path():
    return _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'visitors.json')

def load_visits():
    path = get_visitors_path()
    if _os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return _json.load(f)
        except Exception:
            return []
    return []

def save_visits(visits):
    try:
        with open(get_visitors_path(), 'w', encoding='utf-8') as f:
            _json.dump(visits, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

@app.before_request
def track_visitors_advanced():
    # تجاهل المسارات الإدارية والملفات الثابتة والملفات الحساسة
    if request.path.startswith('/admin') or request.path.startswith('/static') or request.path == '/favicon.ico':
        return

    try:
        ua = request.headers.get('User-Agent', '').lower()

        # 🚫 الفلتر 1: حظر البوتات المعروفة
        bot_keywords = ['bot', 'crawl', 'spider', 'slurp', 'baidu', 'yandex', 'bing', 'googlebot', 'ahrefs', 'semrush', 'python-requests', 'curl', 'wget', 'scrapy', 'httpclient', 'java', 'headlesschrome', 'phantomjs', 'selenium', 'puppeteer']
        if any(keyword in ua for keyword in bot_keywords):
            return

        # 🚫 الفلتر 2: التحقق من وجود User-Agent حقيقي
        if not ua or len(ua) < 20:
            return

        # 🚫 الفلتر 3: منع التكرار في نفس الجلسة (Session)
        if 'visitor_logged' in session:
            return

        # ✅ إذا اجتاز الفلاتر، نعتبره زائراً بشرياً
        visits = load_visits()
        visits.append({
            "id": str(uuid.uuid4())[:8],
            "ip": request.remote_addr or "Unknown",
            "ua": request.headers.get('User-Agent', 'Unknown'),
            "path": request.path,
            "time": _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        if len(visits) > 1000: visits = visits[-1000:]
        save_visits(visits)

        # تعليم الجلسة لمنع التسجيل المتكرر
        session['visitor_logged'] = True

    except Exception:
        pass

@app.route('/admin/visitors')
def admin_visitors():
    if not session.get('admin'): return redirect(url_for('login'))
    try:
        visits = load_visits()
        visits.reverse()
        unique_ips = set(v.get('ip', 'Unknown') for v in visits)
        return render_template('admin_visitors.html', total=len(visits), unique=len(unique_ips), visits=visits)
    except Exception as e:
        return f"خطأ في تحميل الزوار: {str(e)}", 500
# ======================================================================

if __name__ == '__main__':'''

code = code.replace("if __name__ == '__main__':", new_tracker)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ تم تحديث كود التتبع بثلاثة فلاتر متقدمة!")
