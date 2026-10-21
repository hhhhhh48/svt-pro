import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key) if url and key else None

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, abort, request, redirect, url_for, session, flash
import re, json, os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
app.secret_key = 'super_secret_key_bac_2026'


def get_base_path(filename):
    import os
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def load_data():
    with open(get_base_path('data.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(get_base_path('data.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_exams():
    with open(get_base_path('exams.json'), 'r', encoding='utf-8') as f:
        return json.load(f)



def load_users():
    if not os.path.exists('users.json'):
        return []
    try:
        with open(get_base_path('users.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(get_base_path('users.json'), 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_chats():
    if not os.path.exists('chat_messages.json'):
        return []
    try:
        with open(get_base_path('chat_messages.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_chats(chats):
    with open(get_base_path('chat_messages.json'), 'w', encoding='utf-8') as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)


def get_youtube_id(url):
    match = re.search(r'(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([^&\n?#]+)', url)
    return match.group(1) if match else None

app.jinja_env.filters['youtube_id'] = get_youtube_id




# ==================== المسارات الرئيسية ====================
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', streams=data['streams'], tips=data['tips'])

@app.route('/stream/<stream_slug>')
def stream_page(stream_slug):
    data = load_data()
    stream = next((s for s in data['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    return render_template('stream.html', stream=stream)

@app.route('/stream/<stream_slug>/<subject_slug>')
def subject_page(stream_slug, subject_slug):
    data = load_data()
    stream = next((s for s in data['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject: abort(404)
    return render_template('subject.html', stream=stream, subject=subject)

@app.route('/stream/<stream_slug>/<subject_slug>/<unit_slug>')
def unit_page(stream_slug, subject_slug, unit_slug):
    data = load_data()
    stream = next((s for s in data['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject: abort(404)
    unit = next((u for u in subject['units'] if u['slug'] == unit_slug), None)
    if not unit: abort(404)
    return render_template('unit.html', stream=stream, subject=subject, unit=unit)

# ==================== الأرشيف ====================
# ==================== لوحة التحكم ====================
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == 'Mohamed jsk':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('كلمة المرور خاطئة!', 'error')
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'): return redirect(url_for('login'))
    return render_template('admin.html', streams=load_data()['streams'])

@app.route('/admin/add_video', methods=['POST'])
def add_video():
    if not session.get('admin'): return redirect(url_for('login'))
    data = load_data()
    for stream in data['streams']:
        for subject in stream['subjects']:
            for unit in subject['units']:
                if unit['slug'] == request.form['unit'] and subject['slug'] == request.form['subject']:
                    unit['videos'].append({
                        "title": request.form['title'], "url": request.form['url'],
                        "source": "YouTube", "duration": request.form.get('duration', 'متاح')
                    })
                    save_data(data)
                    flash('✅ تمت إضافة الفيديو!', 'success')
                    return redirect(url_for('admin_dashboard'))
    flash('❌ خطأ.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_unit', methods=['POST'])
def add_unit():
    if not session.get('admin'): return redirect(url_for('login'))
    data = load_data()
    for stream in data['streams']:
        for subject in stream['subjects']:
            if subject['slug'] == request.form['subject']:
                subject['units'].append({
                    "id": len(subject['units']) + 1,
                    "slug": request.form['title'].lower().replace(' ', '-'),
                    "title": request.form['title'], "icon": request.form['icon'],
                    "summary": request.form['summary'],
                    "videos": [], "pdfs": [], "exams": [], "quiz": []
                })
                save_data(data)
                flash('✅ تمت إضافة الوحدة!', 'success')
                return redirect(url_for('admin_dashboard'))
    flash('❌ خطأ.', 'error')
    return redirect(url_for('admin_dashboard'))


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = {'units': [], 'videos': [], 'exams': []}
    
    if query and len(query) >= 2:
        data = load_data()
        q_lower = query.lower()
        
        for stream in data['streams']:
            for subject in stream['subjects']:
                for unit in subject['units']:
                    if q_lower in unit['title'].lower() or q_lower in unit['summary'].lower():
                        results['units'].append({'stream': stream, 'subject': subject, 'unit': unit})
                    for video in unit.get('videos', []):
                        if q_lower in video['title'].lower():
                            results['videos'].append({'stream': stream, 'subject': subject, 'unit': unit, 'video': video})
        
        try:
            exams_data = load_exams()
            for stream in exams_data['streams']:
                for subject in stream['subjects']:
                    if q_lower in subject['name'].lower() or q_lower in stream['name'].lower():
                        results['exams'].append({'stream': stream, 'subject': subject})
        except:
            pass
    
    total = len(results['units']) + len(results['videos']) + len(results['exams'])
    return render_template('search.html', query=query, results=results, total=total)


# ==================== نظام التواصل والرسائل ====================
def load_messages():
    if not os.path.exists('messages.json'):
        return []
    try:
        with open(get_base_path('messages.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_messages(messages):
    with open(get_base_path('messages.json'), 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.context_processor
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
    }

@app.route('/contact', methods=['GET', 'POST'])
def contact():
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








# ==================== إعدادات SEO لجوجل ====================
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import send_from_directory

@app.route('/robots.txt')
def robots():
    return """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://svt-pro.onrender.com/sitemap.xml""", 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    data = load_data()
    base_url = "https://svt-pro.onrender.com"
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # الصفحة الرئيسية
    xml += f'  <url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
    
    # الشعب والمواد والدروس
    for stream in data['streams']:
        xml += f'  <url><loc>{base_url}/stream/{stream["slug"]}</loc></url>\n'
        for subject in stream['subjects']:
            xml += f'  <url><loc>{base_url}/stream/{stream["slug"]}/{subject["slug"]}</loc></url>\n'
            for unit in subject['units']:
                xml += f'  <url><loc>{base_url}/stream/{stream["slug"]}/{subject["slug"]}/{unit["slug"]}</loc></url>\n'
                
    xml += '</urlset>'
    return xml, 200, {'Content-Type': 'application/xml'}
# =========================================================


# ==================== نظام الزوار المتقدم ====================
import os as _os, json as _json, datetime as _dt, uuid

def get_visitors_path():
    return _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'visitors.json')

def load_visits():
    path = get_visitors_path()
    if _os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return _json.load(f)
        except Exception:
            return []
    return []

def save_visits(visits):
    try:
        with open(get_visitors_path(), 'w', encoding='utf-8') as f:
            _json.dump(visits, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

@app.before_request
def track_visitors_advanced():
    # تجاهل المسارات الإدارية والملفات الثابتة والملفات الحساسة
    if request.path.startswith('/admin') or request.path.startswith('/static') or request.path == '/favicon.ico':
        return

    try:
        ua = request.headers.get('User-Agent', '').lower()

        # 🚫 الفلتر 1: حظر البوتات المعروفة
        bot_keywords = ['bot', 'crawl', 'spider', 'slurp', 'baidu', 'yandex', 'bing', 'googlebot', 'ahrefs', 'semrush', 'python-requests', 'curl', 'wget', 'scrapy', 'httpclient', 'java', 'headlesschrome', 'phantomjs', 'selenium', 'puppeteer', 'googleother', 'adsbot', 'mediapartners', 'lighthouse', 'pingdom', 'uptimerobot']
        if any(keyword in ua for keyword in bot_keywords):
            return

        # 🚫 الفلتر 2: التحقق من وجود User-Agent حقيقي
        if not ua or len(ua) < 20:
            return

        # 🚫 الفلتر 3: منع التكرار في نفس الجلسة (Session)
        if 'visitor_logged' in session:
            return

        # ✅ إذا اجتاز الفلاتر، نعتبره زائراً بشرياً
        visits = load_visits()
        visits.append({
            "id": str(uuid.uuid4())[:8],
            "ip": request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip(),
            "ua": request.headers.get('User-Agent', 'Unknown'),
            "path": request.path,
            "time": _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        if len(visits) > 1000: visits = visits[-1000:]
        save_visits(visits)

        # تعليم الجلسة لمنع التسجيل المتكرر
        session['visitor_logged'] = True

    except Exception:
        pass

@app.route('/admin/visitors')
def admin_visitors():
    if not session.get('admin'): return redirect(url_for('login'))
    try:
        visits = load_visits()
        visits.reverse()
        unique_ips = set(v.get('ip', 'Unknown') for v in visits)
        return render_template('admin_visitors.html', total=len(visits), unique=len(unique_ips), visits=visits)
    except Exception as e:
        return f"خطأ في تحميل الزوار: {str(e)}", 500
# ======================================================================


@app.route('/exam-center')
def exam_center():
    try:
        with open('exams_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template('exam_center.html', exams=data['exams'])
    except Exception as e:
        return f"خطأ: {str(e)}", 500

@app.route('/exam-center/<exam_slug>')
def exam_view(exam_slug):
    try:
        with open('exams_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        exam = next((e for e in data['exams'] if e['slug'] == exam_slug), None)
        if not exam: abort(404)
        return render_template('exam_view.html', exam=exam)
    except Exception as e:
        return f"خطأ: {str(e)}", 500



@app.route('/news')
def news_page():
    try:
        with open('news_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template('news.html', news=data['news'])
    except Exception as e:
        return f"خطأ في تحميل الأخبار: {str(e)}", 500


@app.route('/exams')
def exams_hub():
    try:
        with open('exams_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template('exams_hub.html', exams=data['exams'])
    except Exception as e:
        return f"Error loading exams: {e}", 500

@app.route('/exams/<exam_id>')
def exam_take(exam_id):
    try:
        with open('exams_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        exam = next((e for e in data['exams'] if e['id'] == exam_id), None)
        if not exam: abort(404)
        return render_template('exam_take.html', exam=exam)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/api/save-result', methods=['POST'])
def save_result():
    try:
        from supabase import create_client
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            return {"status": "error", "msg": "No DB"}, 500
        supabase = create_client(url, key)
        
        data = request.json
        supabase.table('exam_results').insert({
            "student_name": data.get('name', 'مجهول'),
            "exam_id": data.get('exam_id'),
            "score": data.get('score'),
            "total_questions": data.get('total')
        }).execute()
        return {"status": "success"}, 200
    except Exception as e:
        print("Supabase Error:", e)
        return {"status": "error", "msg": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

@app.route('/bac-exam/<stream_slug>/<subject_slug>')
def bac_exam(stream_slug, subject_slug):
    data = load_data()
    stream = next((s for s in data['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject or 'bac_exam' not in subject: abort(404)
    return render_template('bac_exam.html', stream=stream, subject=subject)


