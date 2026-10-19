import os

# 1. إنشاء مجلد templates
os.makedirs('templates', exist_ok=True)

# 2. محتوى ملف data.py (قاعدة البيانات الضخمة)
data_content = '''# -*- coding: utf-8 -*-

STREAMS = [
    {
        "slug": "sciences", "name": "علوم تجريبية", "icon": "🧬", "description": "شعبة العلوم التجريبية - علوم الطبيعة، رياضيات، فيزياء", "gradient": "from-emerald-400 to-teal-500",
        "subjects": [
            {
                "slug": "svt", "name": "علوم الطبيعة والحياة", "icon": "🧬", "description": "الوحدات السبع المعتمدة في المنهاج.",
                "units": [
                    {"id": 1, "slug": "protein", "title": "تركيب البروتين", "icon": "🧬", "summary": "التعبير المورثي: الاستنساخ في النواة، والترجمة في الهيولى.", "videos": [{"title": "القصة الكاملة لتركيب البروتين", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "45:00"}, {"title": "الاستنساخ", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "20:00"}, {"title": "الترجمة", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "25:00"}, {"title": "ملخص شامل", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "حل تمارين", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "40:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "أثناء النضج، ما الذي يتم حذفه؟", "options": ["الإكسونات", "الإنترونات", "الكاب", "ذيل البولي A"], "a": 1}, {"q": "العلاقة بين النيوكليوتيدات والأحماض الأمينية:", "options": ["1:1", "2:1", "3:1", "4:1"], "a": 2}]},
                    {"id": 2, "slug": "immunity", "title": "المناعة", "icon": "🛡️", "summary": "المناعة الطبيعية والمكتسبة، الاستجابة الخلطية والخلوية.", "videos": [{"title": "المناعة من الألف إلى الياء", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "المناعة الخلطية", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "المناعة الخلوية", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "الذاكرة المناعية", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة شاملة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "الخلايا التي تفرز الأجسام المضادة:", "options": ["LTc", "البلعميات", "الخلايا البلازمية", "الجذعية"], "a": 2}]},
                    {"id": 3, "slug": "enzymes", "title": "الإنزيمات", "icon": "⚡", "summary": "الإنزيمات كحفازات حيوية، الخصوصية، وتأثير العوامل.", "videos": [{"title": "الإنزيمات كاملة", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "45:00"}, {"title": "آلية العمل", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "30:00"}, {"title": "التثبيط", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "25:00"}, {"title": "تأثير الحرارة", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "35:00"}, {"title": "حل تمارين", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "40:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "خصائص الإنزيمات:", "options": ["طاقة عالية", "الخصوصية والبروتينية", "حرارة عالية", "استهلاكها"], "a": 1}]},
                    {"id": 4, "slug": "nervous", "title": "الاتصال العصبي", "icon": "🧠", "summary": "السيالة العصبية، كمون الراحة والعمل، والنقل المشبكي.", "videos": [{"title": "الاتصال العصبي كامل", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "كمون الراحة", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "كمون العمل", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "المشبك", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "المبلغ العصبي في العضلات:", "options": ["الدوبامين", "الأستيل كولين", "السيروتونين", "لا شيء"], "a": 1}]},
                    {"id": 5, "slug": "photo", "title": "التركيب الضوئي", "icon": "☀️", "summary": "المرحلة الكيموضوئية وحلقة كالفن.", "videos": [{"title": "التركيب الضوئي كامل", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "الكيموضوئية", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "حلقة كالفن", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "أفكار التمارين", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "تفكك الماء يحدث في:", "options": ["الكالفينية", "الكيموضوئية", "الهيولى", "الميتوكوندريا"], "a": 1}]},
                    {"id": 6, "slug": "respiration", "title": "التنفس والتخمر", "icon": "💨", "summary": "تحرير الطاقة، التنفس الخلوي والتخمرات.", "videos": [{"title": "التنفس والتخمر", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "التحلل السكري", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "حلقة كريبس", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "السلسلة التنفسية", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "المرحلة المشتركة:", "options": ["كريبس", "التحلل السكري", "السلسلة", "لا شيء"], "a": 1}]}
                ]
            },
            {"slug": "math", "name": "الرياضيات", "icon": "📐", "description": "الدوال، المتتاليات، الأعداد المركبة.", "units": [
                {"id": 1, "slug": "functions", "title": "الدوال العددية", "icon": "📈", "summary": "النهايات، الاشتقاق، والتمثيل البياني.", "videos": [{"title": "الدوال كاملة", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "النهايات", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الاشتقاق", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "التغيرات", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "مشتقة x^2:", "options": ["x", "2x", "x^3", "2"], "a": 1}]},
                {"id": 2, "slug": "sequences", "title": "المتتاليات", "icon": "🔢", "summary": "الحسابية والهندسية.", "videos": [{"title": "المتتاليات كاملة", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "الحسابية", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الهندسية", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "التراجع", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "المتتالية الحسابية:", "options": ["نضرب", "نضيف", "نقسم", "لا شيء"], "a": 1}]}
            ]},
            {"slug": "physics", "name": "العلوم الفيزيائية", "icon": "⚛️", "description": "الميكانيك، الكهرباء، والنووية.", "units": [
                {"id": 1, "slug": "mechanics", "title": "الميكانيك", "icon": "🚀", "summary": "قوانين نيوتن والحركة.", "videos": [{"title": "الميكانيك كامل", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "نيوتن", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الطاقة", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "تمارين", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "وحدة القوة:", "options": ["kg", "N", "J", "W"], "a": 1}]}
            ]}
        ]
    },
    {
        "slug": "letters", "name": "آداب وفلسفة", "icon": "📚", "description": "فلسفة، عربية، تاريخ.", "gradient": "from-purple-400 to-pink-500",
        "subjects": [
            {"slug": "philosophy", "name": "الفلسفة", "icon": "🧠", "description": "المقالات والإشكاليات.", "units": [
                {"id": 1, "slug": "mind-body", "title": "العقل والجسد", "icon": "🧠", "summary": "دراسة العلاقة بين العقل والجسد.", "videos": [{"title": "العقل والجسد", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "ديكارت", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "المادية", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "منهجية", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مقالة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "أنا أفكر إذن أنا موجود:", "options": ["أفلاطون", "أرسطو", "ديكارت", "كانط"], "a": 2}]}
            ]},
            {"slug": "arabic", "name": "اللغة العربية", "icon": "📖", "description": "الشعر والنثر.", "units": [
                {"id": 1, "slug": "poetry", "title": "الشعر العباسي", "icon": "🖋️", "summary": "المتنبي وأبو نواس.", "videos": [{"title": "الشعر العباسي", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "المتنبي", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "البلاغة", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "تحليل", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "شاعر الحكمة:", "options": ["أبو نواس", "المتنبي", "البحتري", "جرير"], "a": 1}]}
            ]}
        ]
    },
    {
        "slug": "languages", "name": "لغات أجنبية", "icon": "🌐", "description": "فرنسية، إنجليزية، ألمانية، إسبانية.", "gradient": "from-teal-400 to-cyan-500",
        "subjects": [
            {"slug": "french", "name": "الفرنسية", "icon": "🇫🇷", "description": "القواعد.", "units": [
                {"id": 1, "slug": "grammar", "title": "القواعد", "icon": "🇫🇷", "summary": "الأزمنة والأفعال.", "videos": [{"title": "القواعد", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "الأزمنة", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الأفعال", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "تمارين", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "الماضي المركب:", "options": ["être", "avoir", "aller", "faire"], "a": 1}]}
            ]},
            {"slug": "english", "name": "الإنجليزية", "icon": "🇬🇧", "description": "القواعد.", "units": [
                {"id": 1, "slug": "grammar", "title": "القواعد", "icon": "🇬🇧", "summary": "الأزمنة والأفعال.", "videos": [{"title": "القواعد", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "الأزمنة", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الأفعال", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "تمارين", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "المضارع التام:", "options": ["have", "be", "do", "will"], "a": 0}]}
            ]},
            {"slug": "german", "name": "الألمانية", "icon": "🇩🇪", "description": "القواعد.", "units": [
                {"id": 1, "slug": "grammar", "title": "القواعد", "icon": "🇩🇪", "summary": "الأزمنة والأفعال.", "videos": [{"title": "القواعد", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "الأزمنة", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الأفعال", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "تمارين", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "الماضي التام:", "options": ["haben", "sein", "werden", "machen"], "a": 0}]}
            ]},
            {"slug": "spanish", "name": "الإسبانية", "icon": "🇪🇸", "description": "القواعد.", "units": [
                {"id": 1, "slug": "grammar", "title": "القواعد", "icon": "🇪🇸", "summary": "الأزمنة والأفعال.", "videos": [{"title": "القواعد", "url": "https://www.youtube.com/watch?v=VJxvdaOvdTA", "source": "YouTube", "duration": "50:00"}, {"title": "الأزمنة", "url": "https://www.youtube.com/watch?v=8Q1l6j8Z9lE", "source": "YouTube", "duration": "40:00"}, {"title": "الأفعال", "url": "https://www.youtube.com/watch?v=5G2dX1Y8w1w", "source": "YouTube", "duration": "35:00"}, {"title": "تمارين", "url": "https://www.youtube.com/watch?v=9k14Qi2G1JE", "source": "YouTube", "duration": "30:00"}, {"title": "مراجعة", "url": "https://www.youtube.com/watch?v=ehVFcVNx-XE", "source": "YouTube", "duration": "60:00"}], "pdfs": [], "exams": [], "quiz": [{"q": "الماضي المركب:", "options": ["haber", "ser", "estar", "tener"], "a": 0}]}
            ]}
        ]
    }
]
'''

# 3. محتوى ملف app.py
app_content = '''from flask import Flask, render_template, abort
import re
from data import STREAMS

app = Flask(__name__)

def get_youtube_id(url):
    match = re.search(r'(?:youtube\\.com/(?:watch\\?v=|embed/|shorts/)|youtu\\.be/)([^&\\n?#]+)', url)
    return match.group(1) if match else None

app.jinja_env.filters['youtube_id'] = get_youtube_id

@app.route('/')
def index():
    return render_template('index.html', streams=STREAMS)

@app.route('/stream/<stream_slug>')
def stream_page(stream_slug):
    stream = next((s for s in STREAMS if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    return render_template('stream.html', stream=stream)

@app.route('/stream/<stream_slug>/<subject_slug>')
def subject_page(stream_slug, subject_slug):
    stream = next((s for s in STREAMS if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject: abort(404)
    return render_template('subject.html', stream=stream, subject=subject)

@app.route('/stream/<stream_slug>/<subject_slug>/<unit_slug>')
def unit_page(stream_slug, subject_slug, unit_slug):
    stream = next((s for s in STREAMS if s['slug'] == stream_slug), None)
    if not stream: abort(404)
    subject = next((sub for sub in stream['subjects'] if sub['slug'] == subject_slug), None)
    if not subject: abort(404)
    unit = next((u for u in subject['units'] if u['slug'] == unit_slug), None)
    if not unit: abort(404)
    return render_template('unit.html', stream=stream, subject=subject, unit=unit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
'''

# 4. التصميم الأساسي base.html
base_html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SVT PRO | بكالوريا 2026{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = { theme: { extend: { fontFamily: { sans: ['Readex Pro', 'sans-serif'] }, colors: { brand: { green: '#00ff88', blue: '#00d4ff' } } } } }
    </script>
    <style>
        body { background-color: #050510; color: #ffffff; font-family: 'Readex Pro', sans-serif; overflow-x: hidden; }
        .glass { background: rgba(10, 10, 26, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .glass-hover:hover { border-color: rgba(0, 255, 136, 0.4); box-shadow: 0 0 30px rgba(0, 255, 136, 0.1); transform: translateY(-5px); }
        .text-glow { background: linear-gradient(to right, #00ff88, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .btn-neon { background: linear-gradient(135deg, #00ff88, #00d4ff); color: #050510; font-weight: 800; transition: all 0.3s; }
        .btn-neon:hover { box-shadow: 0 0 20px rgba(0, 255, 136, 0.5); transform: scale(1.02); }
    </style>
</head>
<body class="antialiased min-h-screen relative">
    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-brand-green/10 blur-[150px] rounded-full pointer-events-none"></div>
    <nav class="fixed top-0 w-full z-50 glass border-b border-white/5">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="/" class="flex items-center gap-3 group">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-green to-brand-blue flex items-center justify-center text-xl text-black font-bold">SVT</div>
                <h1 class="text-lg font-bold text-white group-hover:text-glow transition">SVT PRO</h1>
            </a>
            <a href="/" class="text-sm font-bold text-gray-300 hover:text-brand-green transition">الرئيسية</a>
        </div>
    </nav>
    {% block content %}{% endblock %}
    <footer class="border-t border-white/5 pt-10 pb-6 text-center mt-20">
        <p class="text-gray-400 text-sm">تطوير وبرمجة <span class="text-glow font-bold text-lg mx-1">واشمي محمد</span> · © 2026</p>
    </footer>
</body>
</html>
'''

# 5. الصفحة الرئيسية index.html
index_html = '''{% extends "base.html" %}
{% block content %}
<section class="pt-40 pb-20 px-6 text-center">
    <h1 class="text-6xl md:text-8xl font-black mb-6 leading-[1.1]">
        <span class="text-white">بوابتك الشاملة لـ </span>
        <span class="text-glow">البكالوريا</span>
    </h1>
    <p class="text-xl text-gray-400 max-w-3xl mx-auto mb-10">كل الشعب، كل المواد، دروس، فيديوهات، واختبارات في مكان واحد.</p>
</section>

<section id="streams" class="py-20 px-6">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-4xl font-black text-center text-white mb-16">اختر <span class="text-glow">شعبتك</span></h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for stream in streams %}
            <a href="/stream/{{ stream.slug }}" class="glass glass-hover rounded-3xl p-8 transition-all duration-300 relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br {{ stream.gradient }} opacity-10 rounded-bl-full group-hover:scale-150 transition-transform"></div>
                <div class="flex items-center gap-4 mb-6">
                    <div class="w-16 h-16 rounded-2xl bg-gradient-to-br {{ stream.gradient }} flex items-center justify-center text-3xl">{{ stream.icon }}</div>
                    <h3 class="text-2xl font-bold text-white group-hover:text-brand-green transition">{{ stream.name }}</h3>
                </div>
                <p class="text-sm text-gray-400 mb-6">{{ stream.description }}</p>
                <div class="flex justify-between items-center text-xs font-bold text-gray-500 pt-4 border-t border-white/5">
                    <span><i class="fa-solid fa-book text-brand-green ml-1"></i> {{ stream.subjects|length }} مواد</span>
                    <span class="text-brand-green">استكشف <i class="fa-solid fa-arrow-left ml-1"></i></span>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
'''

# 6. صفحة الشعبة stream.html
stream_html = '''{% extends "base.html" %}
{% block title %}{{ stream.name }} | SVT PRO{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-7xl mx-auto">
    <div class="flex items-center gap-6 mb-12">
        <div class="w-24 h-24 rounded-3xl bg-gradient-to-br {{ stream.gradient }} flex items-center justify-center text-5xl">{{ stream.icon }}</div>
        <div>
            <h1 class="text-4xl font-black text-white">{{ stream.name }}</h1>
            <p class="text-gray-400 mt-2">{{ stream.description }}</p>
        </div>
    </div>
    <h2 class="text-2xl font-bold text-white mb-8">المواد الدراسية</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for subject in stream.subjects %}
        <a href="/stream/{{ stream.slug }}/{{ subject.slug }}" class="glass glass-hover rounded-2xl p-6 flex flex-col">
            <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-2xl">{{ subject.icon }}</div>
                <h3 class="text-xl font-bold text-white">{{ subject.name }}</h3>
            </div>
            <p class="text-sm text-gray-400 mb-4 flex-1">{{ subject.description }}</p>
            <div class="text-xs font-bold text-brand-green flex items-center gap-2">
                <i class="fa-solid fa-layer-group"></i> {{ subject.units|length }} وحدات دراسية
            </div>
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}
'''

# 7. صفحة المادة subject.html
subject_html = '''{% extends "base.html" %}
{% block title %}{{ subject.name }} | {{ stream.name }}{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-7xl mx-auto">
    <div class="flex items-center gap-2 text-sm text-gray-400 mb-6">
        <a href="/stream/{{ stream.slug }}" class="hover:text-brand-green">{{ stream.name }}</a>
        <i class="fa-solid fa-chevron-left text-[10px]"></i>
        <span class="text-brand-green">{{ subject.name }}</span>
    </div>
    <div class="flex items-center gap-6 mb-12">
        <div class="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center text-4xl">{{ subject.icon }}</div>
        <div>
            <h1 class="text-4xl font-black text-white">{{ subject.name }}</h1>
            <p class="text-gray-400 mt-2">{{ subject.description }}</p>
        </div>
    </div>
    <h2 class="text-2xl font-bold text-white mb-8">الوحدات والدروس</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {% for unit in subject.units %}
        <a href="/stream/{{ stream.slug }}/{{ subject.slug }}/{{ unit.slug }}" class="glass glass-hover rounded-2xl p-6 relative overflow-hidden group">
            <div class="flex items-start justify-between mb-4">
                <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-green/20 to-brand-blue/20 flex items-center justify-center text-3xl">{{ unit.icon }}</div>
                <span class="text-xs font-bold bg-white/5 px-3 py-1 rounded-full">الوحدة {{ unit.id }}</span>
            </div>
            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-brand-green">{{ unit.title }}</h3>
            <p class="text-sm text-gray-400 line-clamp-2">{{ unit.summary }}</p>
            <div class="mt-6 flex items-center justify-between text-xs font-bold text-gray-500 pt-4 border-t border-white/5">
                <span><i class="fa-solid fa-video text-brand-green ml-1"></i> {{ unit.videos|length }} فيديو</span>
                <span><i class="fa-solid fa-gamepad text-brand-blue ml-1"></i> اختبار</span>
            </div>
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}
'''

# 8. صفحة الوحدة unit.html (مع إصلاح مشكلة الاختبار)
unit_html = '''{% extends "base.html" %}
{% block title %}{{ unit.title }} | {{ subject.name }}{% endblock %}
{% block content %}
<div class="pt-32 pb-24 px-6 max-w-7xl mx-auto">
    <div class="flex items-center gap-2 text-sm text-gray-400 mb-8">
        <a href="/stream/{{ stream.slug }}" class="hover:text-brand-green">{{ stream.name }}</a>
        <i class="fa-solid fa-chevron-left text-[10px]"></i>
        <a href="/stream/{{ stream.slug }}/{{ subject.slug }}" class="hover:text-brand-green">{{ subject.name }}</a>
        <i class="fa-solid fa-chevron-left text-[10px]"></i>
        <span class="text-brand-green">{{ unit.title }}</span>
    </div>
    <div class="flex flex-col md:flex-row items-center gap-8 mb-12">
        <div class="w-24 h-24 rounded-3xl bg-gradient-to-br from-brand-green to-brand-blue flex items-center justify-center text-5xl">{{ unit.icon }}</div>
        <div class="flex-1 text-center md:text-right">
            <h1 class="text-4xl font-black text-white mb-2">{{ unit.title }}</h1>
            <p class="text-gray-400">{{ unit.summary }}</p>
        </div>
        <a href="#quiz" class="btn-neon px-6 py-3 rounded-xl flex items-center gap-2"><i class="fa-solid fa-gamepad"></i> اختبر مستواك</a>
    </div>
    <h2 class="text-2xl font-bold text-white mb-6"><i class="fa-solid fa-video text-brand-green ml-2"></i> الفيديوهات ({{ unit.videos|length }})</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
        {% for v in unit.videos %}
            {% set vid = v.url|youtube_id %}
            <div class="glass rounded-2xl overflow-hidden group">
                <div class="aspect-video relative">
                    <iframe src="https://www.youtube.com/embed/{{ vid }}?rel=0" class="w-full h-full absolute inset-0" loading="lazy" allowfullscreen></iframe>
                </div>
                <div class="p-4">
                    <h3 class="text-sm font-bold text-white line-clamp-1">{{ v.title }}</h3>
                    <p class="text-xs text-gray-500 mt-1">{{ v.source }} · {{ v.duration }}</p>
                </div>
            </div>
        {% endfor %}
    </div>
    <div id="quiz" class="glass rounded-3xl p-8 border-t-4 border-t-brand-blue">
        <h2 class="text-2xl font-bold text-white mb-6"><i class="fa-solid fa-brain text-brand-blue ml-2"></i> اختبار سريع</h2>
        <form id="quizForm" class="space-y-6">
            {% for item in unit.quiz %}
            {% set q_index = loop.index %}
            <div class="bg-white/5 p-6 rounded-2xl quiz-item">
                <h3 class="text-lg font-bold text-white mb-4">{{ q_index }}. {{ item.q }}</h3>
                <div class="space-y-2">
                    {% for option in item.options %}
                    <label class="flex items-center gap-3 p-3 rounded-xl border border-white/10 hover:border-brand-blue/50 cursor-pointer">
                        <input type="radio" name="q{{ q_index }}" value="{{ loop.index0 }}" class="w-5 h-5 accent-brand-blue" required>
                        <span class="text-gray-300">{{ option }}</span>
                    </label>
                    {% endfor %}
                </div>
                <div class="mt-3 hidden result-msg font-bold text-sm"></div>
            </div>
            {% endfor %}
            <button type="submit" class="w-full btn-neon py-4 rounded-xl text-lg">إنهاء الاختبار</button>
        </form>
        <div id="finalScore" class="mt-8 text-center hidden">
            <div class="text-5xl font-black text-glow mb-2">0/0</div>
            <p class="text-gray-400">النتيجة النهائية</p>
        </div>
    </div>
</div>
<script>
    const answers = {{ unit.quiz | map(attribute='a') | list | tojson }};
    document.getElementById('quizForm').addEventListener('submit', function(e) {
        e.preventDefault();
        let score = 0;
        const formData = new FormData(this);
        const quizItems = document.querySelectorAll('.quiz-item');
        answers.forEach((correct, i) => {
            const selected = formData.get('q' + (i+1));
            const parentDiv = quizItems[i];
            const msgDiv = parentDiv.querySelector('.result-msg');
            msgDiv.classList.remove('hidden');
            if (selected == correct) {
                score++;
                msgDiv.innerHTML = '✅ إجابة صحيحة';
                msgDiv.classList.add('text-brand-green');
                msgDiv.classList.remove('text-red-500');
            } else {
                msgDiv.innerHTML = '❌ إجابة خاطئة';
                msgDiv.classList.add('text-red-500');
                msgDiv.classList.remove('text-brand-green');
            }
        });
        document.getElementById('quizForm').style.display = 'none';
        const final = document.getElementById('finalScore');
        final.classList.remove('hidden');
        final.querySelector('div').textContent = `${score} / ${answers.length}`;
    });
</script>
{% endblock %}
'''

# --- كتابة الملفات ---
with open('data.py', 'w', encoding='utf-8') as f: f.write(data_content)
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_content)
with open('templates/base.html', 'w', encoding='utf-8') as f: f.write(base_html)
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)
with open('templates/stream.html', 'w', encoding='utf-8') as f: f.write(stream_html)
with open('templates/subject.html', 'w', encoding='utf-8') as f: f.write(subject_html)
with open('templates/unit.html', 'w', encoding='utf-8') as f: f.write(unit_html)

print("✅ تم إنشاء جميع الملفات بنجاح! (data.py, app.py, templates)")
