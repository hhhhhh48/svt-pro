import json, os, datetime

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
    if len(visits) > 500: visits = visits[-500:]
    save_visits(visits)

def get_stats():
    visits = load_visits()
    # استخدام .get لتجنب الأخطاء إذا كان هناك سجل قديم ناقص
    unique_ips = set(v.get('ip', 'Unknown') for v in visits)
    return len(visits), len(unique_ips), visits
