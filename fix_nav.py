import os, re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# البحث عن قسم الروابط في شريط التنقل واستبداله بالقائمة الكاملة
new_nav_links = '''<div class="hidden md:flex items-center gap-6 text-sm font-bold">
                <a href="/" class="text-gray-300 hover:text-brand-green transition">الرئيسية</a>
                <a href="/exams" class="text-gray-300 hover:text-brand-green transition">الاختبارات</a>
                <a href="/news" class="text-gray-300 hover:text-brand-green transition">الأخبار</a>
                <a href="/exams" class="text-gray-300 hover:text-brand-green transition">الأرشيف</a>
            </div>'''

# استخدام Regex لاستبدال أي قائمة تنقل موجودة حالياً
# نبحث عن <div class="hidden md:flex ...> ونستبدله
pattern = r'<div class="hidden md:flex items-center gap-.*?</div>'
if re.search(pattern, html, flags=re.DOTALL):
    html = re.sub(pattern, new_nav_links, html, count=1, flags=re.DOTALL)
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ تم تحديث شريط التنقل وإضافة (الاختبارات) و (الأخبار) و (الأرشيف).")
else:
    print("⚠️ لم يتم العثور على شريط التنقل القياسي. سنحاول البحث بطريقة أخرى...")
    # محاولة أخرى إذا كان التصميم مختلفاً
    html = html.replace('<a href="/exams" class="text-gray-300 hover:text-brand-green transition">الأرشيف</a>', 
                        '<a href="/exams" class="text-gray-300 hover:text-brand-green transition">الاختبارات</a>\n<a href="/news" class="text-gray-300 hover:text-brand-green transition">الأخبار</a>')
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ تمت محاولة الإضافة.")

# تأكيد وجود مسار /news في app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

if '/news' not in app_code:
    print("⚠️ مسار الأخبار غير موجود في app.py، جاري إضافته...")
    news_route = '''
@app.route('/news')
def news_page():
    try:
        with open('news_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template('news.html', news=data['news'])
    except Exception as e:
        return f"خطأ في تحميل الأخبار: {str(e)}", 500
'''
    app_code = app_code.replace("if __name__ == '__main__':", news_route + "\nif __name__ == '__main__':")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("✅ تم إضافة مسار الأخبار إلى app.py")
else:
    print("ℹ️ مسار الأخبار موجود بالفعل في app.py")

