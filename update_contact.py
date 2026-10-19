import json, os

# 1. إضافة المسارات إلى app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '/contact' not in content:
    routes = '''
# ==================== نظام التواصل والرسائل ====================
def load_messages():
    if not os.path.exists('messages.json'):
        return []
    try:
        with open('messages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_messages(messages):
    with open('messages.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.context_processor
def inject_globals():
    try:
        messages = load_messages()
        unread = sum(1 for m in messages if not m.get('read', False))
    except:
        unread = 0
    return {'unread_messages': unread}

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    import datetime
    if request.method == 'POST':
        messages = load_messages()
        new_id = (max([m['id'] for m in messages]) + 1) if messages else 1
        new_msg = {
            "id": new_id,
            "name": request.form.get('name', '').strip(),
            "email": request.form.get('email', '').strip(),
            "subject": request.form.get('subject', 'استفسار عام'),
            "message": request.form.get('message', '').strip(),
            "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            "read": False
        }
        if new_msg['name'] and new_msg['message']:
            messages.append(new_msg)
            save_messages(messages)
            flash('✅ تم إرسال رسالتك بنجاح! سيتم الرد عليك قريباً.', 'success')
            return redirect(url_for('contact'))
        flash('❌ يرجى ملء الاسم والرسالة على الأقل.', 'error')
    return render_template('contact.html')

@app.route('/admin/messages')
def admin_messages():
    if not session.get('admin'): return redirect(url_for('login'))
    messages = load_messages()[::-1]
    unread = sum(1 for m in messages if not m.get('read', False))
    return render_template('admin_messages.html', messages=messages, unread=unread)

@app.route('/admin/messages/read/<int:msg_id>', methods=['POST'])
def mark_msg_read(msg_id):
    if not session.get('admin'): return redirect(url_for('login'))
    messages = load_messages()
    for m in messages:
        if m['id'] == msg_id: m['read'] = True
    save_messages(messages)
    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/delete/<int:msg_id>', methods=['POST'])
def delete_msg(msg_id):
    if not session.get('admin'): return redirect(url_for('login'))
    messages = [m for m in load_messages() if m['id'] != msg_id]
    save_messages(messages)
    flash('✅ تم حذف الرسالة', 'success')
    return redirect(url_for('admin_messages'))

'''
    content = content.replace("if __name__ == '__main__':", routes + "if __name__ == '__main__':")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ تمت إضافة المسارات")

# 2. إنشاء messages.json فارغ
if not os.path.exists('messages.json'):
    with open('messages.json', 'w', encoding='utf-8') as f:
        json.dump([], f)
    print("✅ تم إنشاء messages.json")

# 3. تحديث base.html: زر التواصل في الشريط + زر عائم
with open('templates/base.html', 'r', encoding='utf-8') as f:
    b = f.read()

if '/contact' not in b:
    # إضافة رابط "تواصل معنا" في الشريط
    old = '<a href="/admin" class="px-3 py-1.5 rounded-full bg-yellow-500/10'
    new = '<a href="/contact" class="text-gray-300 hover:text-brand-green transition"><i class="fa-solid fa-envelope md:hidden"></i><span class="hidden md:inline">تواصل معنا</span></a>\n                ' + old
    b = b.replace(old, new, 1)
    
    # إضافة زر عائم (Floating Button)
    fab = '''<a href="/contact" class="fixed bottom-6 left-6 w-14 h-14 rounded-full bg-gradient-to-br from-brand-green to-brand-blue flex items-center justify-center text-black text-2xl shadow-[0_0_25px_rgba(0,255,136,0.6)] hover:scale-110 transition z-40" title="تواصل معنا">
        <i class="fa-solid fa-comment-dots"></i>
    </a>
</body>'''
    b = b.replace('</body>', fab, 1)
    
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(b)
    print("✅ تم تحديث base.html (رابط + زر عائم)")
else:
    print("ℹ️ التواصل موجود مسبقاً في base.html")

# 4. إضافة رابط الرسائل في لوحة التحكم admin.html
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

if '/admin/messages' not in admin:
    old_link = '<a href="/admin/logout"'
    new_link = '''<a href="/admin/messages" class="px-4 py-2 rounded-xl bg-brand-blue/20 text-brand-blue font-bold hover:bg-brand-blue/30 transition mr-2 relative">
            <i class="fa-solid fa-envelope ml-1"></i> الرسائل
            {% if unread_messages > 0 %}<span class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full text-xs flex items-center justify-center text-white font-bold">{{ unread_messages }}</span>{% endif %}
        </a>
        ''' + old_link
    admin = admin.replace(old_link, new_link, 1)
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write(admin)
    print("✅ تمت إضافة رابط الرسائل في admin.html")

print("\n🎉 كل شيء جاهز!")
