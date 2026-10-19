import os, json, subprocess

# 1. التأكد من وجود data.json
if not os.path.exists('data.json'):
    try:
        from data import STREAMS, TIPS
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({'streams': STREAMS, 'tips': TIPS}, f, ensure_ascii=False, indent=2)
        print("✅ تم إنشاء data.json")
    except Exception as e:
        print("❌ خطأ:", e)

# 2. التأكد من وجود exams.json
if not os.path.exists('exams.json') and os.path.exists('fix_exams.py'):
    os.system('python3 fix_exams.py')

# 3. إصلاح المسارات في app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'def get_base_path' not in code:
    helper = '''
def get_base_path(filename):
    import os
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
'''
    code = code.replace('def load_data():', helper + '\ndef load_data():')

for fname in ['data.json', 'exams.json', 'users.json', 'chat_messages.json', 'messages.json']:
    code = code.replace(f"open('{fname}'", f"open(get_base_path('{fname}')")
    code = code.replace(f'open("{fname}"', f'open(get_base_path("{fname}")')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ تم إصلاح مسارات الملفات في app.py")

# 4. إزالة JSON من .gitignore إن وجدت
if os.path.exists('.gitignore'):
    with open('.gitignore', 'r') as f:
        gi = f.read()
    for name in ['data.json', 'exams.json', 'users.json', 'chat_messages.json', 'messages.json']:
        gi = gi.replace(name + '\n', '')
    with open('.gitignore', 'w') as f:
        f.write(gi)
print("✅ تم تحديث .gitignore")

# 5. رفع الكل إلى GitHub
os.system('git add -f data.json exams.json users.json chat_messages.json messages.json')
os.system('git add .')
os.system('git commit -m "Fix: absolute paths and force add json files"')
print("✅ تم تجهيز الرفع. جاري الرفع...")
