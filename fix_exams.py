import json, os

# 1. توليد exams.json من الصفر
EXAMS_DATA = {
    "sciences": {"name": "علوم تجريبية", "icon": "🧬", "description": "أرشيف بكالوريا شعبة العلوم التجريبية", "gradient": "from-emerald-400 to-teal-500",
        "subjects": {
            "svt": {"name": "علوم الطبيعة والحياة", "icon": "🧬", "slug": "sciences"},
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
            "physics": {"name": "العلوم الفيزيائية", "icon": "⚛️", "slug": "physique"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
        }},
    "math-stream": {"name": "رياضيات", "icon": "📐", "description": "أرشيف بكالوريا شعبة الرياضيات", "gradient": "from-cyan-400 to-blue-500",
        "subjects": {
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
            "physics": {"name": "العلوم الفيزيائية", "icon": "⚛️", "slug": "physique"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
        }},
    "technique": {"name": "تقني رياضي", "icon": "⚙️", "description": "أرشيف بكالوريا شعبة تقني رياضي", "gradient": "from-orange-400 to-red-500",
        "subjects": {
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
            "physics": {"name": "العلوم الفيزيائية", "icon": "⚛️", "slug": "physique"},
            "technology": {"name": "التكنولوجيا", "icon": "⚙️", "slug": "technologie"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
        }},
    "gestion": {"name": "تسيير واقتصاد", "icon": "📊", "description": "أرشيف بكالوريا شعبة التسيير والاقتصاد", "gradient": "from-yellow-400 to-amber-500",
        "subjects": {
            "accounting": {"name": "التسيير المحاسبي", "icon": "📊", "slug": "gestion-comptable"},
            "economy": {"name": "الاقتصاد والمناجمنت", "icon": "💼", "slug": "economie"},
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
            "law": {"name": "القانون", "icon": "⚖️", "slug": "droit"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
        }},
    "letters": {"name": "آداب وفلسفة", "icon": "📚", "description": "أرشيف بكالوريا شعبة الآداب والفلسفة", "gradient": "from-purple-400 to-pink-500",
        "subjects": {
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
        }},
    "languages": {"name": "لغات أجنبية", "icon": "🌐", "description": "أرشيف بكالوريا شعبة اللغات الأجنبية", "gradient": "from-teal-400 to-cyan-500",
        "subjects": {
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "german": {"name": "الألمانية", "icon": "🇩🇪", "slug": "allemand"},
            "spanish": {"name": "الإسبانية", "icon": "🇪🇸", "slug": "espagnol"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
        }},
}

YEARS = ["2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]

def make_exams(eddirasa_slug):
    exams = []
    for year in YEARS:
        if year == "2025":
            url = "https://www.snvdz.com/"; source = "SNVDZ"
        else:
            url = f"https://eddirasa.com/ens-sec/3as/bac-solutions/subject/{eddirasa_slug}/"; source = "Eddirasa"
        exams.append({"year": year, "url": url, "source": source, "is_archive": False})
    exams.append({"year": "أرشيف كامل", "url": f"https://eddirasa.com/ens-sec/3as/bac-solutions/subject/{eddirasa_slug}/", "source": "Eddirasa", "is_archive": True})
    return exams

result = {"streams": []}
for stream_slug, stream_data in EXAMS_DATA.items():
    stream_obj = {"slug": stream_slug, "name": stream_data["name"], "icon": stream_data["icon"],
                  "description": stream_data["description"], "gradient": stream_data["gradient"], "subjects": []}
    for subj_slug, subj_data in stream_data["subjects"].items():
        stream_obj["subjects"].append({
            "slug": subj_slug, "name": subj_data["name"], "icon": subj_data["icon"],
            "exams": make_exams(subj_data["slug"])
        })
    result["streams"].append(stream_obj)

with open('exams.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("✅ exams.json تم إنشاؤه")


# 2. إنشاء exams.html
os.makedirs('templates', exist_ok=True)
with open('templates/exams.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block title %}أرشيف البكالوريا | SVT PRO{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-6">
            <span class="w-2 h-2 rounded-full bg-brand-green animate-pulse"></span>
            <span class="text-xs font-bold text-gray-300">2015 - 2025</span>
        </div>
        <h1 class="text-5xl md:text-7xl font-black text-white mb-4">أرشيف <span class="text-glow">البكالوريا</span></h1>
        <p class="text-xl text-gray-400">كل مواضيع البكالوريا لجميع الشعب والمواد مع التصحيح النموذجي</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for stream in streams %}
        <a href="/exams/{{ stream.slug }}" class="glass glass-hover rounded-3xl p-8 relative overflow-hidden group transition-all">
            <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br {{ stream.gradient }} opacity-10 rounded-bl-full group-hover:scale-150 transition-transform"></div>
            <div class="flex items-center gap-4 mb-6">
                <div class="w-16 h-16 rounded-2xl bg-gradient-to-br {{ stream.gradient }} flex items-center justify-center text-3xl">{{ stream.icon }}</div>
                <h3 class="text-2xl font-bold text-white group-hover:text-brand-green transition">{{ stream.name }}</h3>
            </div>
            <p class="text-sm text-gray-400 mb-6">{{ stream.description }}</p>
            <div class="flex justify-between items-center pt-4 border-t border-white/5">
                <div class="flex items-center gap-4 text-xs font-bold text-gray-500">
                    <span><i class="fa-solid fa-book text-brand-green ml-1"></i> {{ stream.subjects|length }} مواد</span>
                </div>
                <span class="text-brand-green"><i class="fa-solid fa-arrow-left group-hover:translate-x-[-5px] transition"></i></span>
            </div>
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}''')
print("✅ exams.html تم إنشاؤه")


# 3. إنشاء exams_stream.html
with open('templates/exams_stream.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block title %}{{ stream.name }} - الأرشيف{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-7xl mx-auto">
    <div class="flex items-center gap-2 text-sm text-gray-400 mb-6">
        <a href="/exams" class="hover:text-brand-green">الأرشيف</a>
        <i class="fa-solid fa-chevron-left text-[10px]"></i>
        <span class="text-brand-green">{{ stream.name }}</span>
    </div>
    <div class="flex items-center gap-6 mb-12">
        <div class="w-24 h-24 rounded-3xl bg-gradient-to-br {{ stream.gradient }} flex items-center justify-center text-5xl">{{ stream.icon }}</div>
        <div>
            <h1 class="text-4xl font-black text-white">{{ stream.name }}</h1>
            <p class="text-gray-400 mt-2">{{ stream.description }}</p>
        </div>
    </div>
    <h2 class="text-2xl font-bold text-white mb-8">المواد ({{ stream.subjects|length }})</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for subject in stream.subjects %}
        <a href="/exams/{{ stream.slug }}/{{ subject.slug }}" class="glass glass-hover rounded-2xl p-6 group">
            <div class="flex items-center gap-4 mb-4">
                <div class="w-14 h-14 rounded-xl bg-white/5 flex items-center justify-center text-3xl">{{ subject.icon }}</div>
                <h3 class="text-xl font-bold text-white group-hover:text-brand-green">{{ subject.name }}</h3>
            </div>
            <div class="flex items-center justify-between text-xs font-bold text-gray-500 pt-4 border-t border-white/5">
                <span><i class="fa-solid fa-file-pdf text-purple-400 ml-1"></i> {{ subject.exams|length }} موضوع</span>
                <span class="text-brand-green">استكشف <i class="fa-solid fa-arrow-left ml-1"></i></span>
            </div>
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}''')
print("✅ exams_stream.html تم إنشاؤه")


# 4. إنشاء exams_subject.html
with open('templates/exams_subject.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}
{% block title %}{{ subject.name }} - الأرشيف{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-4xl mx-auto">
    <div class="flex items-center gap-2 text-sm text-gray-400 mb-6 flex-wrap">
        <a href="/exams" class="hover:text-brand-green">الأرشيف</a>
        <i class="fa-solid fa-chevron-left text-[10px]"></i>
        <a href="/exams/{{ stream.slug }}" class="hover:text-brand-green">{{ stream.name }}</a>
        <i class="fa-solid fa-chevron-left text-[10px]"></i>
        <span class="text-brand-green">{{ subject.name }}</span>
    </div>
    <div class="flex items-center gap-6 mb-10">
        <div class="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center text-5xl">{{ subject.icon }}</div>
        <div>
            <h1 class="text-3xl font-black text-white">{{ subject.name }}</h1>
            <p class="text-gray-400 mt-1">{{ subject.exams|length }} مواضيع متاحة للتحميل</p>
        </div>
    </div>
    <div class="space-y-3">
        {% for exam in subject.exams %}
        <a href="{{ exam.url }}" target="_blank" rel="noopener noreferrer"
           class="glass glass-hover rounded-2xl p-5 flex items-center justify-between group {% if exam.is_archive %}border border-purple-500/30{% endif %}">
            <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-xl {% if exam.is_archive %}bg-purple-500/20 text-purple-400{% else %}bg-brand-green/10 text-brand-green{% endif %} flex items-center justify-center text-xl font-black">
                    {% if exam.is_archive %}<i class="fa-solid fa-folder-open"></i>{% else %}{{ exam.year }}{% endif %}
                </div>
                <div>
                    <h3 class="text-lg font-bold text-white group-hover:text-brand-green">
                        {% if exam.is_archive %}{{ exam.year }}{% else %}بكالوريا {{ exam.year }}{% endif %}
                    </h3>
                    <p class="text-sm text-gray-400">
                        <i class="fa-solid fa-circle-check text-brand-green text-xs ml-1"></i> موضوع + تصحيح
                        <span class="mx-2">·</span>
                        <i class="fa-solid fa-database text-gray-500 text-xs ml-1"></i> {{ exam.source }}
                    </p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <span class="hidden md:inline text-xs font-bold bg-white/5 px-3 py-1 rounded-full text-gray-400">PDF</span>
                <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-brand-green group-hover:bg-brand-green group-hover:text-black transition">
                    <i class="fa-solid fa-download"></i>
                </div>
            </div>
        </a>
        {% endfor %}
    </div>
    <div class="mt-10 glass rounded-2xl p-6 border-r-4 border-r-brand-blue text-sm text-gray-300">
        <p class="flex items-start gap-3">
            <i class="fa-solid fa-circle-info text-brand-blue mt-1"></i>
            <span>كل المواضيع مأخوذة من مصادر رسمية (<strong>Eddirasa</strong>، <strong>SNVDZ</strong>). الروابط تفتح مباشرة صفحة الموضوع والتصحيح.</span>
        </p>
    </div>
</div>
{% endblock %}''')
print("✅ exams_subject.html تم إنشاؤه")


# 5. التحقق النهائي
print("\n" + "="*50)
print("📋 التحقق من الملفات:")
for f in ['exams.json', 'templates/exams.html', 'templates/exams_stream.html', 'templates/exams_subject.html']:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"  ✅ {f} ({size} bytes)")
    else:
        print(f"  ❌ {f} مفقود!")

# إحصائيات exams.json
with open('exams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
total_exams = sum(len(s['exams']) for stream in data['streams'] for s in stream['subjects'])
print(f"\n📊 الأرشيف: {len(data['streams'])} شعب، {sum(len(s['subjects']) for s in data['streams'])} مادة، {total_exams} ملف")
print("✅ كل شيء جاهز!")
