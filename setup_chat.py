import os, json

# 1. تعديل app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة imports
if 'import datetime' not in content:
    content = content.replace('import re, json, os', 'import re, json, os, datetime')
if 'from werkzeug.security import' not in content:
    content = content.replace('import re, json, os, datetime',
        'import re, json, os, datetime\nfrom werkzeug.security import generate_password_hash, check_password_hash')

# إضافة دوال المستخدمين والدردشة
helpers = '''

def load_users():
    if not os.path.exists('users.json'):
        return []
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_chats():
    if not os.path.exists('chat_messages.json'):
        return []
    try:
        with open('chat_messages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_chats(chats):
    with open('chat_messages.json', 'w', encoding='utf-8') as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)
'''
if 'def load_users' not in content:
    content = content.replace('def get_youtube_id(url):', helpers + '\n\ndef get_youtube_id(url):')

# تحديث context processor
old_ctx = '''@app.context_processor
def inject_globals():
    try:
        messages = load_messages()
        unread = sum(1 for m in messages if not m.get('read', False))
    except:
        unread = 0
    return {'unread_messages': unread}'''

new_ctx = '''@app.context_processor
def inject_globals():
    try:
        unread = sum(1 for m in load_messages() if not m.get('read', False))
    except:
        unread = 0
    try:
        unread_chats_admin = sum(1 for c in load_chats() if c.get('sender') == 'user' and not c.get('read_by_admin', False))
    except:
        unread_chats_admin = 0
    unread_chats_user = 0
    current_user = None
    if session.get('user_id'):
        try:
            unread_chats_user = sum(1 for c in load_chats() if c.get('user_id') == session['user_id'] and c.get('sender') == 'admin' and not c.get('read_by_user', False))
            current_user = next((u for u in load_users() if u['id'] == session['user_id']), None)
        except:
            pass
    return {
        'unread_messages': unread,
        'unread_chats_admin': unread_chats_admin,
        'unread_chats_user': unread_chats_user,
        'current_user': current_user
    }'''

if old_ctx in content:
    content = content.replace(old_ctx, new_ctx)

# إضافة كل مسارات الدردشة
chat_routes = '''
# ==================== نظام المستخدمين والدردشة ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'): return redirect(url_for('user_chat'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()
        if not username or not password or not name:
            flash('❌ يرجى ملء جميع الحقول', 'error'); return redirect(url_for('register'))
        if len(password) < 6:
            flash('❌ كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error'); return redirect(url_for('register'))
        users = load_users()
        if any(u['username'] == username for u in users):
            flash('❌ اسم المستخدم محجوز', 'error'); return redirect(url_for('register'))
        new_id = (max([u['id'] for u in users]) + 1) if users else 1
        users.append({'id': new_id, 'username': username, 'name': name,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
        save_users(users)
        session['user_id'] = new_id
        flash('✅ تم إنشاء حسابك!', 'success')
        return redirect(url_for('user_chat'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if session.get('user_id'): return redirect(url_for('user_chat'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        users = load_users()
        user = next((u for u in users if u['username'] == username), None)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('✅ مرحباً!', 'success'); return redirect(url_for('user_chat'))
        flash('❌ بيانات خاطئة', 'error')
    return render_template('user_login.html')

@app.route('/logout')
def user_logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/chat')
def user_chat():
    if not session.get('user_id'): return redirect(url_for('user_login'))
    chats = [c for c in load_chats() if c['user_id'] == session['user_id']]
    all_chats = load_chats()
    changed = False
    for c in all_chats:
        if c['user_id'] == session['user_id'] and c['sender'] == 'admin' and not c.get('read_by_user', False):
            c['read_by_user'] = True; changed = True
    if changed: save_chats(all_chats)
    return render_template('user_chat.html', chats=chats)

@app.route('/chat/send', methods=['POST'])
def user_send_message():
    if not session.get('user_id'): return redirect(url_for('user_login'))
    message = request.form.get('message', '').strip()
    if message:
        chats = load_chats()
        new_id = (max([c['id'] for c in chats]) + 1) if chats else 1
        chats.append({'id': new_id, 'user_id': session['user_id'], 'sender': 'user',
            'message': message, 'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'read_by_admin': False, 'read_by_user': True})
        save_chats(chats)
    return redirect(url_for('user_chat'))

@app.route('/admin/chats')
def admin_chats():
    if not session.get('admin'): return redirect(url_for('login'))
    users = load_users(); all_chats = load_chats(); conversations = []
    for u in users:
        user_msgs = [c for c in all_chats if c['user_id'] == u['id']]
        if user_msgs:
            last = user_msgs[-1]
            unread = sum(1 for c in user_msgs if c['sender'] == 'user' and not c.get('read_by_admin', False))
            conversations.append({'user': u, 'last_message': last['message'][:60],
                'last_time': last['created_at'], 'last_sender': last['sender'],
                'unread': unread, 'total': len(user_msgs)})
    conversations.sort(key=lambda x: x['last_time'], reverse=True)
    return render_template('admin_chats.html', conversations=conversations)

@app.route('/admin/chat/<int:user_id>')
def admin_chat_view(user_id):
    if not session.get('admin'): return redirect(url_for('login'))
    user = next((u for u in load_users() if u['id'] == user_id), None)
    if not user: abort(404)
    chats = [c for c in load_chats() if c['user_id'] == user_id]
    all_chats = load_chats(); changed = False
    for c in all_chats:
        if c['user_id'] == user_id and c['sender'] == 'user' and not c.get('read_by_admin', False):
            c['read_by_admin'] = True; changed = True
    if changed: save_chats(all_chats)
    return render_template('admin_chat_view.html', user=user, chats=chats)

@app.route('/admin/chat/<int:user_id>/send', methods=['POST'])
def admin_send_message(user_id):
    if not session.get('admin'): return redirect(url_for('login'))
    message = request.form.get('message', '').strip()
    if message:
        chats = load_chats()
        new_id = (max([c['id'] for c in chats]) + 1) if chats else 1
        chats.append({'id': new_id, 'user_id': user_id, 'sender': 'admin',
            'message': message, 'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'read_by_admin': True, 'read_by_user': False})
        save_chats(chats)
    return redirect(url_for('admin_chat_view', user_id=user_id))

'''

if '/register' not in content:
    content = content.replace("if __name__ == '__main__':", chat_routes + "if __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ تم تحديث app.py")

# 2. إنشاء ملفات البيانات
for fname, default in [('users.json', []), ('chat_messages.json', [])]:
    if not os.path.exists(fname):
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(default, f)
        print(f"✅ {fname}")

# 3. إنشاء قوالب الدردشة
templates = {
'register.html': '''{% extends "base.html" %}{% block title %}إنشاء حساب{% endblock %}{% block content %}
<div class="min-h-screen flex items-center justify-center px-6 pt-20 pb-10">
<div class="glass p-8 rounded-3xl w-full max-w-md border border-white/10">
<div class="text-center mb-8"><div class="w-16 h-16 mx-auto bg-gradient-to-br from-brand-green to-brand-blue rounded-2xl flex items-center justify-center text-3xl mb-4">👤</div>
<h1 class="text-2xl font-bold text-white">إنشاء حساب جديد</h1><p class="text-gray-400 text-sm mt-1">تواصل مع المدير مباشرة</p></div>
{% with messages = get_flashed_messages(with_categories=true) %}{% for cat, msg in messages %}<div class="mb-4 p-3 rounded-xl text-sm font-bold text-center {% if cat == 'error' %}bg-red-500/20 text-red-400{% else %}bg-green-500/20 text-green-400{% endif %}">{{ msg }}</div>{% endfor %}{% endwith %}
<form method="POST" class="space-y-4">
<div><label class="block text-sm text-gray-300 mb-2 font-bold">الاسم الكامل</label><input type="text" name="name" required class="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-brand-green outline-none"></div>
<div><label class="block text-sm text-gray-300 mb-2 font-bold">اسم المستخدم</label><input type="text" name="username" required class="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-brand-green outline-none"></div>
<div><label class="block text-sm text-gray-300 mb-2 font-bold">كلمة المرور (6+)</label><input type="password" name="password" required minlength="6" class="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-brand-green outline-none"></div>
<button type="submit" class="w-full btn-neon py-3 rounded-xl text-lg font-bold">إنشاء الحساب</button></form>
<p class="text-center text-sm text-gray-400 mt-6">لديك حساب؟ <a href="/login" class="text-brand-green font-bold hover:underline">سجل الدخول</a></p>
</div></div>{% endblock %}''',

'user_login.html': '''{% extends "base.html" %}{% block title %}تسجيل الدخول{% endblock %}{% block content %}
<div class="min-h-screen flex items-center justify-center px-6 pt-20 pb-10">
<div class="glass p-8 rounded-3xl w-full max-w-md border border-white/10">
<div class="text-center mb-8"><div class="w-16 h-16 mx-auto bg-gradient-to-br from-brand-green to-brand-blue rounded-2xl flex items-center justify-center text-3xl mb-4">🔐</div>
<h1 class="text-2xl font-bold text-white">تسجيل الدخول</h1></div>
{% with messages = get_flashed_messages(with_categories=true) %}{% for cat, msg in messages %}<div class="mb-4 p-3 rounded-xl text-sm font-bold text-center {% if cat == 'error' %}bg-red-500/20 text-red-400{% else %}bg-green-500/20 text-green-400{% endif %}">{{ msg }}</div>{% endfor %}{% endwith %}
<form method="POST" class="space-y-4">
<div><label class="block text-sm text-gray-300 mb-2 font-bold">اسم المستخدم</label><input type="text" name="username" required class="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-brand-green outline-none"></div>
<div><label class="block text-sm text-gray-300 mb-2 font-bold">كلمة المرور</label><input type="password" name="password" required class="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/10 text-white focus:border-brand-green outline-none"></div>
<button type="submit" class="w-full btn-neon py-3 rounded-xl text-lg font-bold">دخول</button></form>
<p class="text-center text-sm text-gray-400 mt-6">ليس لديك حساب؟ <a href="/register" class="text-brand-green font-bold hover:underline">أنشئ حسابك</a></p>
</div></div>{% endblock %}''',

'user_chat.html': '''{% extends "base.html" %}{% block title %}محادثتي{% endblock %}{% block content %}
<div class="pt-20 pb-6 px-3 md:px-6 max-w-3xl mx-auto">
<div class="glass rounded-3xl overflow-hidden border border-white/10 flex flex-col" style="height:calc(100vh - 120px);">
<div class="p-4 bg-gradient-to-r from-brand-green/20 to-brand-blue/20 border-b border-white/10 flex items-center gap-3">
<div class="w-12 h-12 rounded-full bg-gradient-to-br from-brand-green to-brand-blue flex items-center justify-center text-2xl">👨‍💼</div>
<div class="flex-1"><h2 class="font-bold text-white">المدير - واشمي محمد</h2><p class="text-xs text-gray-400"><span class="w-2 h-2 rounded-full bg-brand-green inline-block ml-1"></span> متصل</p></div>
</div>
<div id="chatBox" class="flex-1 overflow-y-auto p-4 space-y-3">
{% if not chats %}<div class="text-center py-12"><i class="fa-solid fa-comment-dots text-5xl text-gray-700 mb-3"></i><p class="text-gray-400">ابدأ المحادثة</p></div>{% endif %}
{% for c in chats %}{% if c.sender == 'user' %}
<div class="flex justify-end"><div class="max-w-[75%] bg-gradient-to-br from-brand-green to-brand-blue text-black rounded-2xl rounded-tr-sm px-4 py-2"><p class="text-sm font-medium whitespace-pre-wrap">{{ c.message }}</p><p class="text-[10px] opacity-70 mt-1 text-left">{{ c.created_at }}</p></div></div>
{% else %}
<div class="flex justify-start"><div class="max-w-[75%] bg-white/10 text-white rounded-2xl rounded-tl-sm px-4 py-2 border border-white/10"><p class="text-sm whitespace-pre-wrap">{{ c.message }}</p><p class="text-[10px] text-gray-500 mt-1">{{ c.created_at }}</p></div></div>
{% endif %}{% endfor %}</div>
<form method="POST" action="/chat/send" class="p-3 border-t border-white/10 bg-black/40 flex gap-2">
<input type="text" name="message" required autocomplete="off" placeholder="اكتب رسالتك..." class="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-brand-green outline-none">
<button type="submit" class="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-green to-brand-blue flex items-center justify-center text-black hover:scale-105 transition"><i class="fa-solid fa-paper-plane"></i></button>
</form></div></div>
<script>const cb=document.getElementById('chatBox');cb.scrollTop=cb.scrollHeight;let t=false;const i=document.querySelector('input[name="message"]');if(i){i.addEventListener('input',()=>t=true);i.addEventListener('blur',()=>t=false);}setInterval(()=>{if(!t)location.reload();},8000);</script>
{% endblock %}''',

'admin_chats.html': '''{% extends "base.html" %}{% block title %}المحادثات{% endblock %}{% block content %}
<div class="pt-32 pb-20 px-6 max-w-4xl mx-auto">
<div class="flex items-center justify-between mb-8 flex-wrap gap-4">
<div><h1 class="text-3xl font-black text-white">💬 المحادثات</h1><p class="text-gray-400 mt-1">{{ conversations|length }} محادثة · <span class="text-red-400 font-bold">{{ unread_chats_admin }} جديدة</span></p></div>
<a href="/admin" class="px-4 py-2 rounded-xl bg-white/5 text-gray-300 hover:bg-white/10 transition font-bold"><i class="fa-solid fa-arrow-right ml-1"></i> لوحة التحكم</a></div>
{% if not conversations %}<div class="glass rounded-3xl p-12 text-center"><i class="fa-solid fa-comments text-6xl text-gray-700 mb-4"></i><p class="text-gray-400 text-lg">لا توجد محادثات</p></div>
{% else %}<div class="space-y-3">
{% for conv in conversations %}
<a href="/admin/chat/{{ conv.user.id }}" class="glass glass-hover rounded-2xl p-5 flex items-center gap-4 group">
<div class="w-14 h-14 rounded-full bg-gradient-to-br from-brand-green to-brand-blue flex items-center justify-center text-black font-black text-xl shrink-0">{{ conv.user.name[0]|upper }}</div>
<div class="flex-1 min-w-0"><div class="flex items-center justify-between gap-2 mb-1"><h3 class="font-bold text-white group-hover:text-brand-green truncate">{{ conv.user.name }}</h3><span class="text-xs text-gray-500 shrink-0">{{ conv.last_time }}</span></div>
<p class="text-sm text-gray-400 truncate">{% if conv.last_sender == 'admin' %}<span class="text-brand-green">أنت:</span> {% endif %}{{ conv.last_message }}</p></div>
{% if conv.unread > 0 %}<div class="w-7 h-7 rounded-full bg-red-500 flex items-center justify-center text-white text-xs font-bold shrink-0">{{ conv.unread }}</div>{% endif %}
</a>{% endfor %}</div>{% endif %}</div>{% endblock %}''',

'admin_chat_view.html': '''{% extends "base.html" %}{% block title %}محادثة مع {{ user.name }}{% endblock %}{% block content %}
<div class="pt-20 pb-6 px-3 md:px-6 max-w-3xl mx-auto">
<div class="glass rounded-3xl overflow-hidden border border-white/10 flex flex-col" style="height:calc(100vh - 120px);">
<div class="p-4 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-b border-white/10 flex items-center gap-3">
<a href="/admin/chats" class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-white hover:bg-white/20 transition"><i class="fa-solid fa-arrow-right"></i></a>
<div class="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-black text-xl">{{ user.name[0]|upper }}</div>
<div class="flex-1"><h2 class="font-bold text-white">{{ user.name }}</h2><p class="text-xs text-gray-400">@{{ user.username }}</p></div></div>
<div id="chatBox" class="flex-1 overflow-y-auto p-4 space-y-3">
{% if not chats %}<div class="text-center py-12"><p class="text-gray-400">لا توجد رسائل بعد</p></div>{% endif %}
{% for c in chats %}{% if c.sender == 'user' %}
<div class="flex justify-start"><div class="max-w-[75%] bg-white/10 text-white rounded-2xl rounded-tl-sm px-4 py-2 border border-white/10"><p class="text-sm whitespace-pre-wrap">{{ c.message }}</p><p class="text-[10px] text-gray-500 mt-1">{{ c.created_at }}</p></div></div>
{% else %}
<div class="flex justify-end"><div class="max-w-[75%] bg-gradient-to-br from-purple-500 to-pink-500 text-white rounded-2xl rounded-tr-sm px-4 py-2"><p class="text-sm whitespace-pre-wrap">{{ c.message }}</p><p class="text-[10px] opacity-70 mt-1 text-left">{{ c.created_at }}</p></div></div>
{% endif %}{% endfor %}</div>
<form method="POST" action="/admin/chat/{{ user.id }}/send" class="p-3 border-t border-white/10 bg-black/40 flex gap-2">
<input type="text" name="message" required autocomplete="off" placeholder="اكتب ردك..." class="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-purple-400 outline-none">
<button type="submit" class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white hover:scale-105 transition"><i class="fa-solid fa-paper-plane"></i></button>
</form></div></div>
<script>const cb=document.getElementById('chatBox');cb.scrollTop=cb.scrollHeight;let t=false;const i=document.querySelector('input[name="message"]');if(i){i.addEventListener('input',()=>t=true);i.addEventListener('blur',()=>t=false);}setInterval(()=>{if(!t)location.reload();},8000);</script>
{% endblock %}'''
}

for name, html in templates.items():
    with open(f'templates/{name}', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ {name}")

# 4. تحديث base.html
with open('templates/base.html', 'r', encoding='utf-8') as f:
    base = f.read()

if 'href="/register"' not in base:
    # البحث عن رابط /admin واستبداله
    import re
    pattern = r'(<a href="/admin" class="px-3 py-1\.5[^"]*"[^>]*>.*?</a>)'
    match = re.search(pattern, base, re.DOTALL)
    if match:
        admin_link = match.group(1)
        new_nav = '''{% if current_user %}
                <a href="/chat" class="relative px-3 py-1.5 rounded-full bg-brand-green/10 text-brand-green hover:bg-brand-green/20 transition text-xs"><i class="fa-solid fa-comment-dots"></i><span class="hidden md:inline mr-1">{{ current_user.name.split(' ')[0] }}</span>{% if unread_chats_user > 0 %}<span class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center text-white font-bold">{{ unread_chats_user }}</span>{% endif %}</a>
                <a href="/logout" class="text-gray-400 hover:text-red-400 transition text-xs" title="خروج"><i class="fa-solid fa-sign-out-alt"></i></a>
                {% else %}
                <a href="/login" class="text-gray-300 hover:text-brand-green transition text-xs"><i class="fa-solid fa-sign-in-alt"></i><span class="hidden md:inline mr-1">دخول</span></a>
                <a href="/register" class="px-3 py-1.5 rounded-full bg-brand-green/10 text-brand-green hover:bg-brand-green/20 transition text-xs"><i class="fa-solid fa-user-plus"></i><span class="hidden md:inline mr-1">حساب جديد</span></a>
                {% endif %}
                ''' + admin_link
        base = base.replace(admin_link, new_nav)
        with open('templates/base.html', 'w', encoding='utf-8') as f:
            f.write(base)
        print("✅ تم تحديث base.html")
    else:
        print("⚠️ لم يتم العثور على رابط /admin. أضف الروابط يدوياً لاحقاً.")
else:
    print("ℹ️ base.html محدث مسبقاً")

# 5. تحديث admin.html
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

if '/admin/chats' not in admin:
    old_logout = '<a href="/admin/logout"'
    if old_logout in admin:
        new_chats = '''<a href="/admin/chats" class="px-4 py-2 rounded-xl bg-brand-green/20 text-brand-green font-bold hover:bg-brand-green/30 transition mr-2 relative">
            <i class="fa-solid fa-comments ml-1"></i> المحادثات
            {% if unread_chats_admin > 0 %}<span class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full text-xs flex items-center justify-center text-white font-bold">{{ unread_chats_admin }}</span>{% endif %}
        </a>
        ''' + old_logout
        admin = admin.replace(old_logout, new_chats, 1)
        with open('templates/admin.html', 'w', encoding='utf-8') as f:
            f.write(admin)
        print("✅ تم تحديث admin.html")

print("\n🎉 اكتمل نظام الدردشة!")
