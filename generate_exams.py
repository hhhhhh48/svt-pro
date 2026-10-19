import json

# كل شعبة بموادها ومصادرها
EXAMS_DATA = {
    "sciences": {
        "name": "علوم تجريبية", "icon": "🧬", "description": "أرشيف بكالوريا شعبة العلوم التجريبية", "gradient": "from-emerald-400 to-teal-500",
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
        }
    },
    "math-stream": {
        "name": "رياضيات", "icon": "📐", "description": "أرشيف بكالوريا شعبة الرياضيات", "gradient": "from-cyan-400 to-blue-500",
        "subjects": {
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
            "physics": {"name": "العلوم الفيزيائية", "icon": "⚛️", "slug": "physique"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
        }
    },
    "technique": {
        "name": "تقني رياضي", "icon": "⚙️", "description": "أرشيف بكالوريا شعبة تقني رياضي", "gradient": "from-orange-400 to-red-500",
        "subjects": {
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
            "physics": {"name": "العلوم الفيزيائية", "icon": "⚛️", "slug": "physique"},
            "technology": {"name": "التكنولوجيا", "icon": "⚙️", "slug": "technologie"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
        }
    },
    "gestion": {
        "name": "تسيير واقتصاد", "icon": "📊", "description": "أرشيف بكالوريا شعبة التسيير والاقتصاد", "gradient": "from-yellow-400 to-amber-500",
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
        }
    },
    "letters": {
        "name": "آداب وفلسفة", "icon": "📚", "description": "أرشيف بكالوريا شعبة الآداب والفلسفة", "gradient": "from-purple-400 to-pink-500",
        "subjects": {
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "math": {"name": "الرياضيات", "icon": "📐", "slug": "mathematiques"},
        }
    },
    "languages": {
        "name": "لغات أجنبية", "icon": "🌐", "description": "أرشيف بكالوريا شعبة اللغات الأجنبية", "gradient": "from-teal-400 to-cyan-500",
        "subjects": {
            "french": {"name": "الفرنسية", "icon": "🇫🇷", "slug": "francais"},
            "english": {"name": "الإنجليزية", "icon": "🇬🇧", "slug": "anglais"},
            "german": {"name": "الألمانية", "icon": "🇩🇪", "slug": "allemand"},
            "spanish": {"name": "الإسبانية", "icon": "🇪🇸", "slug": "espagnol"},
            "arabic": {"name": "اللغة العربية", "icon": "📖", "slug": "arabe"},
            "philosophy": {"name": "الفلسفة", "icon": "🧠", "slug": "philosophie"},
            "history": {"name": "التاريخ والجغرافيا", "icon": "🌍", "slug": "histoire-geographie"},
            "islamic": {"name": "العلوم الإسلامية", "icon": "🕌", "slug": "sciences-islamiques"},
        }
    }
}

# السنوات من 2025 إلى 2015
YEARS = ["2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]

def generate_exams_for_subject(eddirasa_slug):
    """توليد قائمة الامتحانات لمادة معينة"""
    exams = []
    for year in YEARS:
        # 2025 من SNVDZ (يحتوي الأحدث)
        if year == "2025":
            url = "https://www.snvdz.com/"
            source = "SNVDZ"
        else:
            # بقية السنوات من Eddirasa (الأرشيف الرسمي)
            url = f"https://eddirasa.com/ens-sec/3as/bac-solutions/subject/{eddirasa_slug}/"
            source = "Eddirasa"
        exams.append({"year": year, "url": url, "source": source})
    # أرشيف كامل
    exams.append({"year": "أرشيف كامل", "url": f"https://eddirasa.com/ens-sec/3as/bac-solutions/subject/{eddirasa_slug}/", "source": "Eddirasa", "is_archive": True})
    return exams

# بناء الهيكل النهائي
result = {"streams": []}
for stream_slug, stream_data in EXAMS_DATA.items():
    stream_obj = {
        "slug": stream_slug,
        "name": stream_data["name"],
        "icon": stream_data["icon"],
        "description": stream_data["description"],
        "gradient": stream_data["gradient"],
        "subjects": []
    }
    for subj_slug, subj_data in stream_data["subjects"].items():
        stream_obj["subjects"].append({
            "slug": subj_slug,
            "name": subj_data["name"],
            "icon": subj_data["icon"],
            "exams": generate_exams_for_subject(subj_data["slug"])
        })
    result["streams"].append(stream_obj)

# حفظ
with open('exams.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# إحصائيات
total_streams = len(result["streams"])
total_subjects = sum(len(s["subjects"]) for s in result["streams"])
total_exams = sum(len(sub["exams"]) for s in result["streams"] for sub in s["subjects"])
print(f"✅ تم إنشاء exams.json بنجاح!")
print(f"📊 الشعب: {total_streams}")
print(f"📚 المواد: {total_subjects}")
print(f"📝 الامتحانات: {total_exams}")
