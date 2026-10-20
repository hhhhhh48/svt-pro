import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# إضافة استيراد ProxyFix إذا لم يكن موجوداً
if 'from werkzeug.middleware.proxy_fix import ProxyFix' not in code:
    code = code.replace('from flask import', 'from werkzeug.middleware.proxy_fix import ProxyFix\nfrom flask import')

# تفعيل ProxyFix بعد إنشاء التطبيق مباشرة
if 'app.wsgi_app = ProxyFix' not in code:
    code = code.replace('app = Flask(__name__)', 'app = Flask(__name__)\napp.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)')

# تحديث سطر تسجيل الزيارة لضمان قراءة الـ IP الحقيقي
code = code.replace('"ip": request.remote_addr or "Unknown",', '"ip": request.headers.get(\'X-Forwarded-For\', request.remote_addr).split(\',\')[0].strip(),')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ تم تفعيل ProxyFix لالتقاط الـ IP الحقيقي للزوار!")
