import os

# 1. إضافة مسار البحث إلى app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

search_route = '''
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

'''

marker = "if __name__ == '__main__':"
if "/search" not in content and marker in content:
    content = content.replace(marker, search_route + marker)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ تمت إضافة مسار البحث إلى app.py")
else:
    print("ℹ️ مسار البحث موجود مسبقاً")

# 2. إنشاء search.html
with open('templates/search.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block title %}البحث: {{ query }} | SVT PRO{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-5xl mx-auto">
    <div class="text-center mb-10">
        <h1 class="text-3xl md:text-5xl font-black text-white mb-3">
            {% if query %}نتائج البحث عن: <span class="text-glow">"{{ query }}"</span>{% else %}🔍 البحث{% endif %}
        </h1>
        {% if query %}<p class="text-gray-400">{{ total }} نتيجة</p>{% endif %}
    </div>
    
    <form action="/search" method="GET" class="mb-12">
        <div class="relative">
            <input type="text" name="q" value="{{ query }}" placeholder="ابحث عن درس، فيديو، مادة..." autofocus class="w-full px-6 py-4 pl-16 rounded-2xl glass text-white text-lg focus:border-brand-green outline-none">
            <button type="submit" class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-xl bg-brand-green/20 text-brand-green flex items-center justify-center hover:bg-brand-green/30 transition">
                <i class="fa-solid fa-search"></i>
            </button>
        </div>
    </form>
    
    {% if not query %}
    <div class="text-center py-16">
        <i class="fa-solid fa-magnifying-glass text-6xl text-gray-700 mb-6"></i>
        <p class="text-gray-400 text-lg mb-6">اكتب كلمة للبحث في كل المحتوى</p>
        <div class="flex flex-wrap justify-center gap-2">
            <span class="text-sm text-gray-500 py-1">جرّب:</span>
            {% for term in ['المناعة','الدوال','البروتين','الفلسفة','التنفس','الأعداد المركبة'] %}
            <a href="/search?q={{ term }}" class="px-3 py-1 rounded-full bg-white/5 text-brand-green text-sm hover:bg-white/10 transition">{{ term }}</a>
            {% endfor %}
        </div>
    </div>
    {% elif total == 0 %}
    <div class="text-center py-16">
        <i class="fa-solid fa-face-frown text-6xl text-gray-700 mb-6"></i>
        <p class="text-gray-400 text-lg">لا توجد نتائج لـ "{{ query }}"</p>
        <p class="text-gray-500 text-sm mt-2">جرب كلمات أخرى أو تحقق من الإملاء</p>
    </div>
    {% else %}
    
    {% if results.units %}
    <div class="mb-10">
        <h2 class="text-xl font-bold text-white mb-4"><i class="fa-solid fa-book text-brand-green ml-2"></i> الدروس ({{ results.units|length }})</h2>
        <div class="space-y-3">
            {% for r in results.units %}
            <a href="/stream/{{ r.stream.slug }}/{{ r.subject.slug }}/{{ r.unit.slug }}" class="glass glass-hover rounded-2xl p-5 flex items-center gap-4 group">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br {{ r.stream.gradient }} flex items-center justify-center text-2xl shrink-0">{{ r.unit.icon }}</div>
                <div class="flex-1 min-w-0">
                    <h3 class="text-lg font-bold text-white group-hover:text-brand-green truncate">{{ r.unit.title }}</h3>
                    <p class="text-sm text-gray-400">{{ r.stream.name }} · {{ r.subject.name }}</p>
                </div>
                <i class="fa-solid fa-arrow-left text-gray-500 group-hover:text-brand-green transition"></i>
            </a>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    {% if results.videos %}
    <div class="mb-10">
        <h2 class="text-xl font-bold text-white mb-4"><i class="fa-brands fa-youtube text-red-500 ml-2"></i> الفيديوهات ({{ results.videos|length }})</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            {% for r in results.videos %}
            <a href="/stream/{{ r.stream.slug }}/{{ r.subject.slug }}/{{ r.unit.slug }}" class="glass glass-hover rounded-2xl p-4 flex items-center gap-3 group">
                <i class="fa-brands fa-youtube text-red-500 text-2xl shrink-0"></i>
                <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-bold text-white group-hover:text-brand-green truncate">{{ r.video.title }}</h3>
                    <p class="text-xs text-gray-500 truncate">{{ r.unit.title }}</p>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    {% if results.exams %}
    <div class="mb-10">
        <h2 class="text-xl font-bold text-white mb-4"><i class="fa-solid fa-file-pdf text-purple-400 ml-2"></i> امتحانات البكالوريا ({{ results.exams|length }})</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            {% for r in results.exams %}
            <a href="/exams/{{ r.stream.slug }}/{{ r.subject.slug }}" class="glass glass-hover rounded-2xl p-4 flex items-center gap-3 group">
                <i class="fa-solid fa-file-pdf text-purple-400 text-2xl shrink-0"></i>
                <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-bold text-white group-hover:text-purple-400 truncate">{{ r.subject.name }}</h3>
                    <p class="text-xs text-gray-500">{{ r.stream.name }}</p>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    {% endif %}
</div>
{% endblock %}''')
print("✅ تم إنشاء templates/search.html")

# 3. إضافة شريط البحث إلى base.html
with open('templates/base.html', 'r', encoding='utf-8') as f:
    base = f.read()

search_bar = '''<form action="/search" method="GET" class="hidden md:block flex-1 max-w-xs mx-4">
                <div class="relative">
                    <input type="text" name="q" placeholder="🔍 ابحث..." class="w-full px-4 py-2 pr-10 rounded-full bg-white/5 border border-white/10 text-white text-sm focus:border-brand-green outline-none">
                </div>
            </form>
            <a href="/search" class="md:hidden w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-gray-300 hover:text-brand-green transition"><i class="fa-solid fa-search"></i></a>
            '''

marker = '<div class="flex items-center gap-3 md:gap-6 text-sm font-bold">'
if marker in base and "/search" not in base:
    base = base.replace(marker, search_bar + marker, 1)
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base)
    print("✅ تمت إضافة شريط البحث إلى base.html")
else:
    print("ℹ️ شريط البحث موجود مسبقاً")

print("\n🎉 تم كل شيء بنجاح!")
