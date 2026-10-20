import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

seo_code = '''
# ==================== إعدادات SEO لجوجل ====================
from flask import send_from_directory

@app.route('/robots.txt')
def robots():
    return """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://svt-pro.onrender.com/sitemap.xml""", 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    data = load_data()
    base_url = "https://svt-pro.onrender.com"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n'
    
    # الصفحة الرئيسية
    xml += f'  <url><loc>{base_url}/</loc><priority>1.0</priority></url>\\n'
    
    # الشعب والمواد والدروس
    for stream in data['streams']:
        xml += f'  <url><loc>{base_url}/stream/{stream["slug"]}</loc></url>\\n'
        for subject in stream['subjects']:
            xml += f'  <url><loc>{base_url}/stream/{stream["slug"]}/{subject["slug"]}</loc></url>\\n'
            for unit in subject['units']:
                xml += f'  <url><loc>{base_url}/stream/{stream["slug"]}/{subject["slug"]}/{unit["slug"]}</loc></url>\\n'
                
    xml += '</urlset>'
    return xml, 200, {'Content-Type': 'application/xml'}
# =========================================================

if __name__ == '__main__':'''

if '/sitemap.xml' not in code:
    code = code.replace("if __name__ == '__main__':", seo_code)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ تمت إضافة مسارات robots.txt و sitemap.xml")
