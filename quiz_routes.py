# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify
import json, os, random, uuid, urllib.request
from urllib.parse import quote
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

DATA_DIR = 'data'
QUESTIONS_FILE = os.path.join(DATA_DIR, 'questions.json')
ATTEMPTS_FILE = os.path.join(DATA_DIR, 'attempts.json')


def load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []


def save_json(path, data):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)




def load_all_questions():
    """يجمع كل الأسئلة من data/questions*.json"""
    all_q = []
    if os.path.isdir(DATA_DIR):
        for name in os.listdir(DATA_DIR):
            if name.startswith('questions') and name.endswith('.json'):
                all_q.extend(load_json(os.path.join(DATA_DIR, name), []))
    return all_q


def get_week_key():
    now = datetime.now()
    return f"{now.year}-W{now.isocalendar()[1]:02d}"


# ========== Supabase helpers (مع fallback محلي) ==========
def _sb_creds():
    return os.environ.get('SUPABASE_URL', ''), os.environ.get('SUPABASE_KEY', '')


def sb_enabled():
    url, key = _sb_creds()
    return bool(url and key)


def sb_request(method, path, data=None, query=None):
    url, key = _sb_creds()
    if not url or not key:
        return None
    full = url.rstrip('/') + '/rest/v1/' + path
    if query:
        full += '?' + query
    headers = {
        'apikey': key,
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    body = json.dumps(data, ensure_ascii=False).encode('utf-8') if data is not None else None
    req = urllib.request.Request(full, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            txt = resp.read().decode('utf-8')
            return json.loads(txt) if txt else []
    except Exception as e:
        print(f'Supabase error ({method} {path}):', e)
        return None


def get_attempts(week_key=None, subject_id=None, user_name=None, limit=None):
    """يقرأ المحاولات. Supabase إن مفعّل، وإلا محليًا."""
    if sb_enabled():
        filters = []
        if week_key:
            filters.append(f'week_key=eq.{quote(week_key)}')
        if subject_id:
            filters.append(f'subject_id=eq.{quote(subject_id)}')
        if user_name:
            filters.append(f'user_name=eq.{quote(user_name)}')
        q = '&'.join(filters)
        if limit:
            q = (q + '&' if q else '') + f'limit={limit}'
        result = sb_request('GET', 'quiz_attempts', query=q)
        if result is not None:
            return result
    # fallback محلي
    attempts = load_json(ATTEMPTS_FILE)
    if week_key:
        attempts = [a for a in attempts if a.get('week_key') == week_key]
    if subject_id:
        attempts = [a for a in attempts if a.get('subject_id') == subject_id]
    if user_name:
        attempts = [a for a in attempts if (a.get('user_name') or '').strip() == user_name]
    if limit:
        attempts = attempts[-limit:]
    return attempts


def persist_attempt(attempt):
    """يحفظ المحاولة. Supabase إن مفعّل، وإلا محليًا."""
    if sb_enabled():
        result = sb_request('POST', 'quiz_attempts', data=attempt)
        if result is not None:
            return True
        print('⚠️ فشل الحفظ في Supabase، سيحفظ محليًا')
    attempts = load_json(ATTEMPTS_FILE)
    attempts.append(attempt)
    save_json(ATTEMPTS_FILE, attempts)
    return True


@quiz_bp.route('/quiz/<subject_id>/<unit_id>')
def quiz_page(subject_id, unit_id):
    return render_template('quiz.html', subject_id=subject_id, unit_id=unit_id)


@quiz_bp.route('/api/quiz/start', methods=['POST'])
def quiz_start():
    data = request.get_json() or {}
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')
    num_questions = int(data.get('num_questions', 10))

    all_questions = load_all_questions()
    filtered = [
        q for q in all_questions
        if q.get('subjectId') == subject_id
        and (unit_id == 'all' or q.get('unitId') == unit_id)
        and q.get('status') == 'published'
    ]

    if not filtered:
        return jsonify({'error': 'لا توجد أسئلة منشورة لهذه الوحدة بعد'}), 404

    random.shuffle(filtered)
    selected = filtered[:num_questions]

    safe = []
    for q in selected:
        safe.append({
            'id': q['id'],
            'type': q['type'],
            'question': q['question'],
            'options': q.get('options') or q.get('reasonOptions') or []
        })

    return jsonify({
        'quiz_id': str(uuid.uuid4()),
        'questions': safe,
        'total': len(safe)
    })


@quiz_bp.route('/api/quiz/submit', methods=['POST'])
def quiz_submit():
    data = request.get_json() or {}
    answers = data.get('answers', [])
    duration_sec = int(data.get('duration_sec', 0))
    user_name = (data.get('user_name') or '').strip() or 'مجهول'
    subject_id = data.get('subject_id', '')
    unit_id = data.get('unit_id', '')

    if duration_sec < 3:
        return jsonify({'error': 'محاولة سريعة بشكل غير طبيعي'}), 400

    all_questions = load_all_questions()
    qmap = {q['id']: q for q in all_questions}

    score = 0
    details = []
    for ans in answers:
        q = qmap.get(ans.get('question_id'))
        if not q:
            continue

        correct = False
        correct_answer = ''

        if q['type'] in ('qcm', 'term_match', 'date_event'):
            correct_answer = q.get('correctOptionId', '')
            correct = ans.get('given') == correct_answer
        elif q['type'] == 'true_false_reason':
            correct_answer = f"{q.get('correctBoolean')} / {q.get('correctReasonId')}"
            given_bool = str(ans.get('given_bool', '')).lower() == 'true'
            correct = (given_bool == bool(q.get('correctBoolean'))
                       and ans.get('given_reason') == q.get('correctReasonId'))

        if correct:
            score += 1

        details.append({
            'question_id': q['id'],
            'question': q['question'],
            'correct': correct,
            'given': ans.get('given') or ans.get('given_reason') or '',
            'correct_answer': correct_answer,
            'explanation': q.get('explanation', '')
        })

    week_key = get_week_key()
    attempt = {
        'id': str(uuid.uuid4()),
        'user_name': user_name,
        'subject_id': subject_id,
        'unit_id': unit_id,
        'score': score,
        'total': len(answers),
        'duration_sec': duration_sec,
        'week_key': week_key,
        'created_at': datetime.now().isoformat(),
        'answers': answers
    }

    persist_attempt(attempt)

    return jsonify({
        'attempt_id': attempt['id'],
        'score': score,
        'total': len(answers),
        'details': details
    })


@quiz_bp.route('/leaderboard')
def leaderboard():
    """لوحة الصدارة مع تصفية حسب المادة"""
    subject_filter = request.args.get('subject', 'all')
    week_key = get_week_key()
    weekly = get_attempts(
        week_key=week_key,
        subject_id=subject_filter if subject_filter != 'all' else None
    )

    # تجميع حسب المستخدم
    agg = {}
    for a in weekly:
        name = (a.get('user_name') or 'مجهول').strip()
        if name == 'مجهول' or not name:
            name = 'مجهول'
        if name not in agg:
            agg[name] = {'name': name, 'points': 0, 'quizzes': 0,
                         'correct': 0, 'total': 0, 'subjects': set()}
        agg[name]['points'] += a.get('score', 0) * 10
        agg[name]['quizzes'] += 1
        agg[name]['correct'] += a.get('score', 0)
        agg[name]['total'] += a.get('total', 0)
        if a.get('subject_id'):
            agg[name]['subjects'].add(a['subject_id'])

    # حساب الدقة + تحويل set إلى list
    for u in agg.values():
        u['accuracy'] = round(100 * u['correct'] / u['total']) if u['total'] else 0
        u['subjects'] = list(u['subjects'])

    # ترتيب: النقاط ← الدقة ← عدد الكويزات
    top = sorted(agg.values(),
                 key=lambda x: (-x['points'], -x['accuracy'], -x['quizzes']))[:10]

    # إحصائيات المادة (لمعرفة أي مادة نعرض)
    subject_totals = {}
    for a in weekly:
        sid = a.get('subject_id')
        if sid:
            subject_totals[sid] = subject_totals.get(sid, 0) + 1

    meta = load_meta()
    subjects_for_tabs = []
    for sid in ['all'] + list(subject_totals.keys()):
        if sid == 'all':
            subjects_for_tabs.append({
                'id': 'all',
                'name': 'الكل',
                'icon': '🌍',
                'count': len(weekly)
            })
        else:
            info = meta.get(sid, {})
            subjects_for_tabs.append({
                'id': sid,
                'name': info.get('name', sid),
                'icon': info.get('icon', '📚'),
                'count': subject_totals[sid]
            })

    return render_template('leaderboard.html',
                           top=top,
                           week_key=week_key,
                           current_filter=subject_filter,
                           subjects=subjects_for_tabs,
                           total_attempts=len(weekly))


    agg = {}
    for a in weekly:
        name = a.get('user_name', 'مجهول')
        if name not in agg:
            agg[name] = {'name': name, 'points': 0, 'quizzes': 0, 'correct': 0, 'total': 0}
        agg[name]['points'] += a.get('score', 0) * 10
        agg[name]['quizzes'] += 1
        agg[name]['correct'] += a.get('score', 0)
        agg[name]['total'] += a.get('total', 0)

    top = sorted(agg.values(), key=lambda x: (-x['points'], -x['correct']))[:10]
    return render_template('leaderboard.html', top=top, week_key=week_key)


# ========== المسارات الجديدة: الصفحة المركزية ==========
META_FILE = os.path.join(DATA_DIR, 'quiz_subjects_meta.json')


def load_meta():
    return load_json(META_FILE, {})


@quiz_bp.route('/quiz')
def quiz_home():
    all_q = load_all_questions()
    meta = load_meta()
    counts = {}
    for q in all_q:
        if q.get('status') != 'published':
            continue
        sid = q.get('subjectId')
        if sid:
            counts[sid] = counts.get(sid, 0) + 1

    subjects = []
    for sid, count in counts.items():
        info = meta.get(sid, {})
        subjects.append({
            'id': sid,
            'name': info.get('name', sid),
            'icon': info.get('icon', '📚'),
            'gradient': info.get('gradient', 'from-gray-400 to-gray-500'),
            'count': count,
        })
    subjects.sort(key=lambda x: -x['count'])
    return render_template('quiz_home.html', subjects=subjects)


@quiz_bp.route('/quiz/<subject_id>')
def quiz_subject(subject_id):
    all_q = load_all_questions()
    meta = load_meta().get(subject_id, {})
    units_meta = meta.get('units', {})

    unit_counts = {}
    for q in all_q:
        if q.get('status') != 'published' or q.get('subjectId') != subject_id:
            continue
        uid = q.get('unitId', 'default')
        unit_counts[uid] = unit_counts.get(uid, 0) + 1

    units = []
    for uid, cnt in unit_counts.items():
        units.append({
            'id': uid,
            'name': units_meta.get(uid, uid),
            'count': cnt,
        })
    units.sort(key=lambda x: units_meta.get(x['id'], x['id']))

    total = sum(unit_counts.values())
    return render_template('quiz_subject.html',
                           subject_id=subject_id,
                           subject_name=meta.get('name', subject_id),
                           subject_icon=meta.get('icon', '📚'),
                           gradient=meta.get('gradient', 'from-gray-400 to-gray-500'),
                           total=total,
                           units=units)


# ========== مسار الملف الشخصي ==========
@quiz_bp.route('/profile')
def profile():
    name = request.args.get('name', '').strip()
    if not name:
        return render_template('profile.html', name=None, empty=True)

    user_attempts = get_attempts(user_name=name)

    if not user_attempts:
        return render_template('profile.html', name=name, empty=True)

    all_q = load_all_questions()
    qmap = {q['id']: q for q in all_q}
    meta = load_meta()

    total_attempts = len(user_attempts)
    total_correct = sum(a.get('score', 0) for a in user_attempts)
    total_questions = sum(a.get('total', 0) for a in user_attempts)
    overall_accuracy = round(100 * total_correct / total_questions) if total_questions else 0
    total_points = total_correct * 10

    # حسب المادة
    subject_stats = {}
    for a in user_attempts:
        sid = a.get('subject_id')
        if not sid:
            continue
        if sid not in subject_stats:
            subject_stats[sid] = {'correct': 0, 'total': 0, 'attempts': 0}
        subject_stats[sid]['correct'] += a.get('score', 0)
        subject_stats[sid]['total'] += a.get('total', 0)
        subject_stats[sid]['attempts'] += 1

    subjects_list = []
    for sid, st in subject_stats.items():
        info = meta.get(sid, {})
        acc = round(100 * st['correct'] / st['total']) if st['total'] else 0
        subjects_list.append({
            'id': sid,
            'name': info.get('name', sid),
            'icon': info.get('icon', '📚'),
            'accuracy': acc,
            'attempts': st['attempts'],
            'correct': st['correct'],
            'total': st['total'],
        })
    subjects_list.sort(key=lambda x: -x['attempts'])

    # حسب الوحدة (نستخدم answers + qmap)
    unit_stats = {}
    for a in user_attempts:
        for ans in a.get('answers', []):
            qid = ans.get('question_id')
            q = qmap.get(qid)
            if not q:
                continue
            uid = q.get('unitId')
            if not uid:
                continue
            if uid not in unit_stats:
                unit_stats[uid] = {'correct': 0, 'total': 0, 'subjectId': q.get('subjectId')}
            unit_stats[uid]['total'] += 1
            if q.get('type') in ('qcm', 'term_match', 'date_event'):
                if ans.get('given') == q.get('correctOptionId'):
                    unit_stats[uid]['correct'] += 1

    units_list = []
    for uid, st in unit_stats.items():
        sid = st['subjectId']
        s_info = meta.get(sid, {})
        uname = s_info.get('units', {}).get(uid, uid)
        acc = round(100 * st['correct'] / st['total']) if st['total'] else 0
        units_list.append({
            'id': uid,
            'subjectId': sid,
            'name': uname,
            'subjectName': s_info.get('name', sid),
            'subjectIcon': s_info.get('icon', '📚'),
            'accuracy': acc,
            'correct': st['correct'],
            'total': st['total'],
        })
    units_list.sort(key=lambda x: (x['accuracy'], -x['total']))
    weak_units = [u for u in units_list if u['accuracy'] < 60 and u['total'] >= 2][:5]
    strong_units = sorted(
        [u for u in units_list if u['accuracy'] >= 80 and u['total'] >= 2],
        key=lambda x: -x['accuracy']
    )[:5]

    # محاولات أخيرة
    recent = sorted(user_attempts, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
    recent_list = []
    for r in recent:
        sid = r.get('subject_id', '')
        info = meta.get(sid, {})
        total = r.get('total', 0)
        score = r.get('score', 0)
        recent_list.append({
            'subject_id': sid,
            'subject_name': info.get('name', sid),
            'subject_icon': info.get('icon', '📚'),
            'score': score,
            'total': total,
            'accuracy': round(100 * score / total) if total else 0,
            'duration': r.get('duration_sec', 0),
            'date': (r.get('created_at', '') or '')[:10],
        })

    return render_template('profile.html',
                           name=name,
                           empty=False,
                           total_attempts=total_attempts,
                           total_correct=total_correct,
                           total_questions=total_questions,
                           overall_accuracy=overall_accuracy,
                           total_points=total_points,
                           subjects=subjects_list,
                           weak_units=weak_units,
                           strong_units=strong_units,
                           recent=recent_list)


@quiz_bp.route('/api/quiz/status')
def quiz_status():
    return jsonify({
        'storage': 'supabase' if sb_enabled() else 'local_json',
        'supabase_enabled': sb_enabled(),
        'attempts_file_exists': os.path.exists(ATTEMPTS_FILE),
    })
