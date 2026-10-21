import re, os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. حذف كل تعريفات @app.route('/') بأي شكل كانت
# سنستخدم طريقة التقسيم (split) بدلاً من regex للموثوقية
lines = code.split('\n')
result = []
i = 0
removed = 0
while i < len(lines):
    line = lines[i]
    # إذا وجدنا بداية route('/')
    if re.match(r"^\s*@app\.route\(['\"]\/['\"]\)", line):
        removed += 1
        i += 1
        # تخطي حتى نهاية الدالة (نبحث عن أول سطر غير متباعد بعد def)
        # أولاً: تجاوز سطر def
        if i < len(lines) and lines[i].strip().startswith('def '):
            i += 1
            # الآن تخطي جسم الدالة (كل الأسطر المتباعدة أو الفارغة)
            while i < len(lines):
                if lines[i] and not lines[i].startswith('    ') and not lines[i].startswith('\t'):
                    if lines[i].strip():
                        break
                i += 1
        continue
    result.append(line)
    i += 1

code = '\n'.join(result)
print(f"🗑️ تم حذف {removed} تعريف قديم لـ /")

# 2. تنظيف المسافات الزائدة
code = re.sub(r'\n{3,}', '\n\n', code)

# 3. إضافة مسار /test و / (بطريقة بسيطة جداً لا تتعارض)
home_routes = '''
@app.route('/test')
def healthcheck():
    return "OK - Server Working", 200

@app.route('/')
def homepage():
    try:
        data = load_data()
        return render_template('index.html',
                               streams=data.get('streams', []) if data else [],
                               tips=data.get('tips', []) if data else [])
    except Exception as e:
        return "<h1>خطأ في الصفحة الرئيسية</h1><pre>" + str(e) + "</pre>", 500

if __name__ == '__main__':'''

code = code.replace("if __name__ == '__main__':", home_routes, 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

# 4. التحقق النهائي
print("\n" + "="*50)
print("🔍 فحص المسارات الآن:")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_app", "app.py")
    test_app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_app)
    for rule in test_app.app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"  ✅ {rule.rule}")
    print("="*50)
    print("✅ التطبيق يحمل بنجاح! المسارات أعلاه تعمل.")
except Exception as e:
    print(f"❌ خطأ: {e}")
