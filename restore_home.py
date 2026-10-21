import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# نتحقق أولاً إذا كان المسار '/' موجوداً
if "@app.route('/')" not in code:
    # دالة الصفحة الرئيسية
    home_route = '''
@app.route('/')
def index():
    try:
        data = load_data()
        return render_template('index.html', streams=data['streams'], tips=data.get('tips', []))
    except Exception as e:
        return f"Error loading home: {e}", 500
'''
    # نضيفها قبل أول مسار آخر أو قبل التشغيل
    if "if __name__ == '__main__':" in code:
        code = code.replace("if __name__ == '__main__':", home_route + "\nif __name__ == '__main__':")
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ تمت إعادة مسار الصفحة الرئيسية '/' بنجاح!")
else:
    print("ℹ️ مسار الرئيسية موجود مسبقاً.")
