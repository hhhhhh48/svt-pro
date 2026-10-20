import os, re

# 1. تحديث فلتر البوتات في app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# إضافة كلمات مفتاحية جديدة لطرد روبوتات جوجل وأمازون
old_bots = "bot_keywords = ['bot', 'crawl', 'spider', 'slurp', 'baidu', 'yandex', 'bing', 'googlebot', 'ahrefs', 'semrush', 'python-requests', 'curl', 'wget', 'scrapy', 'httpclient', 'java', 'headlesschrome', 'phantomjs', 'selenium', 'puppeteer']"
new_bots = "bot_keywords = ['bot', 'crawl', 'spider', 'slurp', 'baidu', 'yandex', 'bing', 'googlebot', 'ahrefs', 'semrush', 'python-requests', 'curl', 'wget', 'scrapy', 'httpclient', 'java', 'headlesschrome', 'phantomjs', 'selenium', 'puppeteer', 'googleother', 'adsbot', 'mediapartners', 'lighthouse', 'pingdom', 'uptimerobot']"

if old_bots in code:
    code = code.replace(old_bots, new_bots)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ تم تحديث فلتر البوتات (طرد روبوتات جوجل وأدوات الفحص).")
else:
    print("ℹ️ الفلتر محدث مسبقاً أو لم يتم العثور على النص الأصلي.")

# 2. إصلاح اسم الموقع في التذييل (SVT PRO -> BAC 2026)
with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'SVT PRO' in html or 'SVT <span' in html:
    html = html.replace('SVT PRO', 'BAC 2026')
    html = html.replace('SVT <span class="text-glow">PRO</span>', 'BAC <span class="text-glow">2026</span>')
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ تم إصلاح اسم الموقع في التذييل ليصبح BAC 2026.")
else:
    print("ℹ️ اسم الموقع في التذييل صحيح مسبقاً.")
