import os
import json
import urllib.request
from flask import Flask, render_template, abort, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'bac_2026_super_secret_key_change_this'
BASE = os.path.dirname(os.path.abspath(__file__))

# ==================== دوال تحميل البيانات ====================
def load_json(filename, default):
    path = os.path.join(BASE, filename)
    if not os.path.exists(path):
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    try:
        with open(os.path.join(BASE, filename), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_data(): return load_json('data.json', {'streams': [], 'tips': []})
def load_exams(): return load_json('exams_data.json', {'exams': []})
def load_news(): return load_json('news_data.json', {'news': []})
def load_users(): return load_json('users.json', [])
def load_chats(): return load_json('chat_messages.json', [])
def load_messages(): return load_json('messages.json', [])

# ==================== Supabase ====================
def save_to_supabase(name, exam_id, score, total):
    url = os.environ.get('SUPABASE_URL', '')
    key = os.environ.get('SUPABASE_KEY', '')
    if not url or not key: return False
    try:
        payload = json.dumps({
            'student_name': name, 'exam_id': exam_id,
            'score': int(score), 'total_questions': int(total)
        }).encode('utf-8')
        req = urllib.request.Request(
            url + '/rest/v1/exam_results', data=payload,
            headers={'apikey': key, 'Authorization': 'Bearer ' + key,
                     'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
            method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 201)
    except Exception as e:
        print('Supabase Error:', e)
        return False

# ==================== Routes ====================
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', streams=data.get('streams', []), tips=data.get('tips', []))

@app.route('/test')
def test(): return "OK - Server Works", 200

@app.route('/stream/<stream_slug>')
def stream_page(stream_slug):
    stream = next((s for s in load_data()['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    return render_template('stream.html', stream=stream)

@app.route('/stream/<stream_slug>/<subject_slug>')
def subject_page(stream_slug, subject_slug):
    stream = next((s for s in load_data()['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject: abort(404)
    return render_template('subject.html', stream=stream, subject=subject)

@app.route('/stream/<stream_slug>/<subject_slug>/<unit_slug>')
def unit_page(stream_slug, subject_slug, unit_slug):
    stream = next((s for s in load_data()['streams'] if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject: abort(404)
    unit = next((u for u in subject['units'] if u['slug'] == unit_slug), None)
    if not unit: abort(404)
    return render_template('unit.html', stream=stream, subject=subject, unit=unit)

@app.route('/exams')
def exams_hub():
    return render_template('exams_hub.html', exams=load_exams().get('exams', []))

@app.route('/exams/<exam_id>')
def exam_take(exam_id):
    exam = next((e for e in load_exams().get('exams', []) if e['id'] == exam_id), None)
    if not exam: abort(404)
    return render_template('exam_take.html', exam=exam)

@app.route('/api/save-result', methods=['POST'])
def save_result():
    d = request.json or {}
    ok = save_to_supabase(d.get('name', 'مجهول'), d.get('exam_id', ''), d.get('score', 0), d.get('total', 20))
    return {'status': 'success' if ok else 'error'}, (200 if ok else 500)

@app.route('/news')
def news_page():
    return render_template('news.html', news=load_news().get('news', []))

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
    return render_template('admin.html', streams=load_data().get('streams', []))

@app.route('/admin/visitors')
def admin_visitors():
    if not session.get('admin'): return redirect(url_for('login'))
    visitors = load_json('visitors.json', [])
    unique = len(set(v.get('ip', '') for v in visitors))
    return render_template('admin_visitors.html', total=len(visitors), unique=unique, visits=list(reversed(visitors)))

@app.route('/register', methods=['GET', 'POST'])
def register():
    from werkzeug.security import generate_password_hash
    import datetime
    if request.method == 'POST':
        users = load_users()
        username = request.form.get('username', '').strip()
        if any(u['username'] == username for u in users):
            flash('اسم المستخدم محجوز', 'error')
            return redirect(url_for('register'))
        new_id = (max([u['id'] for u in users]) + 1) if users else 1
        users.append({'id': new_id, 'username': username, 'name': request.form.get('name', ''),
                      'password_hash': generate_password_hash(request.form.get('password', '')),
                      'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
        save_json('users.json', users)
        session['user_id'] = new_id
        return redirect(url_for('user_chat'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    from werkzeug.security import check_password_hash
    if request.method == 'POST':
        users = load_users()
        user = next((u for u in users if u['username'] == request.form.get('username', '').strip()), None)
        if user and check_password_hash(user['password_hash'], request.form.get('password', '')):
            session['user_id'] = user['id']
            return redirect(url_for('user_chat'))
        flash('بيانات خاطئة', 'error')
    return render_template('user_login.html')

@app.route('/logout')
def user_logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/chat')
def user_chat():
    if not session.get('user_id'): return redirect(url_for('user_login'))
    chats = [c for c in load_chats() if c['user_id'] == session['user_id']]
    return render_template('user_chat.html', chats=chats)

@app.route('/chat/send', methods=['POST'])
def user_send_message():
    import datetime
    if not session.get('user_id'): return redirect(url_for('user_login'))
    msg = request.form.get('message', '').strip()
    if msg:
        chats = load_chats()
        nid = (max([c['id'] for c in chats]) + 1) if chats else 1
        chats.append({'id': nid, 'user_id': session['user_id'], 'sender': 'user',
                      'message': msg, 'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                      'read_by_admin': False, 'read_by_user': True})
        save_json('chat_messages.json', chats)
    return redirect(url_for('user_chat'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    import datetime
    if request.method == 'POST':
        msgs = load_messages()
        nid = (max([m['id'] for m in msgs]) + 1) if msgs else 1
        msgs.append({'id': nid, 'name': request.form.get('name', ''),
                     'email': request.form.get('email', ''),
                     'subject': request.form.get('subject', 'استفسار'),
                     'message': request.form.get('message', ''),
                     'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                     'read': False})
        save_json('messages.json', msgs)
        flash('✅ تم إرسال رسالتك!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
