import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. حذف أي مسار يحتوي على كود الـ JSON المزعج
routes = re.split(r'(?=@app\.route)', code)
new_routes = []
removed = 0

for r in routes:
    if 'attempts_file_exists' in r or 'supabase_enabled' in r:
        removed += 1
        continue # تجاهل هذا المسار بالكامل
    new_routes.append(r)

code = "".join(new_routes)
print(f"🗑️ تم حذف {removed} مسار يحتوي على كود الاختبار.")

# 2. حذف أي مسار رئيسي قديم '/'
routes = re.split(r'(?=@app\.route)', code)
new_routes = []
for r in routes:
    if r.strip().startswith("@app.route('/')") or r.strip().startswith('@app.route("/")'):
        continue # تجاهل المسار القديم
    new_routes.append(r)

code = "".join(new_routes)

# 3. تنظيف سطر التشغيل القديم
code = re.sub(r"if __name__ == .__main__.:.*", "", code, flags=re.DOTALL)

# 4. إضافة الصفحة الرئيسية الصحيحة وسطر التشغيل
final_code = '''
@app.route('/')
def index():
    try:
        data = load_data()
        return render_template('index.html', streams=data.get('streams', []), tips=data.get('tips', []))
    except Exception as e:
        return f"<h1>خطأ في الصفحة الرئيسية</h1><pre>{e}</pre>", 500

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)), debug=False)
'''

code = code + "\n" + final_code

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ تم تطهير الملف بالكامل وإضافة الصفحة الرئيسية الأصلية بنجاح!")
