import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# تقسيم الكود بناءً على بداية كل مسار @app.route
parts = re.split(r'(?=@app\.route)', code)

header = parts[0]
routes = parts[1:]

seen_routes = set()
new_routes = []

for route in routes:
    # استخراج اسم المسار (مثلاً '/exam-center')
    match = re.search(r'@app\.route\([\'"](.*?)[\'"]', route)
    if match:
        route_path = match.group(1)
        if route_path not in seen_routes:
            seen_routes.add(route_path)
            new_routes.append(route)
        else:
            print(f"🗑️ تم حذف نسخة مكررة من المسار: {route_path}")
    else:
        new_routes.append(route)

# إعادة تجميع الكود
new_code = header + "".join(new_routes)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("✅ تم تنظيف الكود وإزالة جميع التكرارات بنجاح!")
