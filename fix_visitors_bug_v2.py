import os, re

# 1. تحديث visitor_tracker.py ليكون محصناً ضد الأخطاء
tracker_code = '''import json, os, datetime

BOT_KEYWORDS = ['bot', 'crawl', 'spider', 'slurp', 'baidu', 'yandex', 'bing', 'googlebot', 'ahrefs', 'semrush', 'python-requests', 'curl', 'wget', 'scrapy', 'httpclient', 'java', 'headlesschrome', 'phantomjs', 'selenium', 'puppeteer']

def is_human(user_agent):
    if not user_agent: return False
    try:
        ua_lower = user_agent.lower()
        return not any(k in ua_lower for k in BOT_KEYWORDS)
    except Exception:
        return False

def load_visits():
    if not os.path.exists('visitors.json'): return []
    try:
        with open('visitors.json', 'r', encoding='utf-8') as f: return json.load(f)
    except Exception: return []

def save_visits(visits):
    try:
        with open('visitors.json', 'w', encoding='utf-8') as f:
            json.dump(visits, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def log_visit(ip, ua, path):
    try:
        visits = load_visits()
        visits.append({
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ip": ip, "ua": ua, "path": path
        })
        if len(visits) > 500: visits = visits[-500:]
        save_visits(visits)
    except Exception:
        pass

def get_stats():
    try:
        visits = load_visits()
        unique_ips = set(v.get('ip', 'Unknown') for v in visits if isinstance(v, dict))
        return len(visits), len(unique_ips), visits
    except Exception:
        return 0, 0, []
'''
with open('visitor_tracker.py', 'w', encoding='utf-8') as f:
    f.write(tracker_code)

# 2. تصحيح دالة التتبع في app.py لتكون آمنة
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# البحث عن الدالة القديمة واستبدالها بالنسخة الآمنة
old_hook_pattern = r"@app\.before_request\s*def track_visitors\(\):.*?log_visit\(request\.remote_addr, ua, request\.path\)"
new_hook = '''@app.before_request
def track_visitors():
    if request.path.startswith('/static/') or request.path.startswith('/admin'):
        return
    try:
        ua = request.headers.get('User-Agent', '')
        if is_human(ua):
            log_visit(request.remote_addr, ua, request.path)
    except Exception:
        pass'''
app_code = re.sub(old_hook_pattern, new_hook, app_code, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("✅ تم إصلاح الكود! الموقع لن يتعطل أبداً حتى لو فشل تسجيل الزوار.")
