import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. تقسيم الكود بناءً على بداية كل مسار @app.route
routes = re.split(r'(?=@app\.route)', code)
new_routes = []

for r in routes:
    # البحث عن المسار الذي يعرض هذا الـ JSON المزعج أو المسار الرئيسي القديم
    if 'attempts_file_exists' in r or 'supabase_enabled' in r:
        print("🗑️ تم حذف كود الاختبار (JSON) المزعج.")
        continue
    if r.strip().startswith("@app.route('/')") or r.strip().startswith('@app.route("/")'):
        print("🗑️ تم حذف الصفحة الرئيسية القديمة.")
        continue
    new_routes.append(r)

code = "".join(new_routes)

# 2. إضافة الصفحة الرئيسية الصحيحة (التي تعرض index.html)
home_route = '''
@app.route('/')
def index():
    try:
        data = load_data()
        return render_template('index.html', streams=data.get('streams', []), tips=data.get('tips', []))
    except Exception as e:
        return f"<h1>خطأ في الصفحة الرئيسية</h1><pre>{e}</pre>", 500

if __name__ == '__main__':'''

code = code.replace("if __name__ == '__main__':", home_route)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ تمت الجراحة بنجاح! تم حذف الـ JSON وإعادة الصفحة الرئيسية.")
