# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

def yt(q): return f"https://www.youtube.com/results?search_query={quote(q)}"

def vids(title):
    return [
        {"title": f"مراجعة شاملة: {title}", "url": yt(f"مراجعة {title} بكالوريا"), "source": "YouTube", "duration": "متاح"},
        {"title": f"شرح مفصل: {title}", "url": yt(f"شرح {title} بكالوريا"), "source": "YouTube", "duration": "متاح"},
        {"title": f"ملخص {title}", "url": yt(f"ملخص {title} بكالوريا"), "source": "YouTube", "duration": "متاح"},
        {"title": f"تمارين {title}", "url": yt(f"تمارين {title} بكالوريا محلولة"), "source": "YouTube", "duration": "متاح"},
        {"title": f"أفكار {title}", "url": yt(f"أفكار {title} بكالوريا 2026"), "source": "YouTube", "duration": "متاح"},
    ]

def qz(title):
    return [
        {"q": f"ما هو المفهوم الأساسي في {title}؟", "options": ["المفهوم الصحيح", "خيار خاطئ 1", "خيار خاطئ 2", "خيار خاطئ 3"], "a": 0},
        {"q": f"أي من التالي يرتبط بـ {title}؟", "options": ["خيار خاطئ", "المفهوم الصحيح", "خيار خاطئ", "خيار خاطئ"], "a": 1},
    ]

def make_unit(uid, slug, title, icon, summary):
    return {"id": uid, "slug": slug, "title": title, "icon": icon, "summary": summary,
            "videos": vids(title), "pdfs": [{"title": f"ملخص {title} PDF", "url": "https://eddirasa.com/", "source": "Eddirasa"}],
            "exams": [{"title": f"بكالوريا {title}", "url": "https://www.snvdz.com/", "source": "SNVDZ", "year": "2025"}],
            "quiz": qz(title)}

def make_subject(slug, name, icon, desc, units):
    return {"slug": slug, "name": name, "icon": icon, "description": desc,
            "units": [make_unit(i+1, u[0], u[1], u[2], u[3]) for i, u in enumerate(units)]}

# --- بيانات كل الشعب والمواد والوحدات ---
DATA = [
    {"slug":"sciences","name":"علوم تجريبية","icon":"🧬","description":"علوم الطبيعة، رياضيات، فيزياء","gradient":"from-emerald-400 to-teal-500","subjects":[
        make_subject("svt","علوم الطبيعة والحياة","🧬","الوحدات السبع",[
            ("protein-synthesis","تركيب البروتين","🧬","التعبير المورثي"),
            ("protein-structure","بنية البروتين ووظيفته","🔗","العلاقة بنية-وظيفة"),
            ("enzymes","الإنزيمات","⚡","الحفازات الحيوية"),
            ("immunity","المناعة","🛡️","الاستجابة المناعية"),
            ("nervous-communication","الاتصال العصبي","🧠","السيالة العصبية"),
            ("photosynthesis","التركيب الضوئي","☀️","تحويل الطاقة"),
            ("respiration-fermentation","التنفس والتخمر","💨","تحرير الطاقة"),
        ]),
        make_subject("math","الرياضيات","📐","الدوال والتحليل",[
            ("functions","الدوال العددية","📈","النهايات والاشتقاق"),
            ("derivatives","الاشتقاق وتطبيقاته","✏️","الاشتقاق"),
            ("primitives","الدوال الأصلية","∫","التكامل"),
            ("log-exp","الدوال الأسية واللوغاريتمية","📊","اللوغاريتم"),
            ("sequences","المتتاليات العددية","🔢","الحسابية والهندسية"),
            ("complex","الأعداد المركبة","🔮","الأعداد العقدية"),
            ("probability","الاحتمالات","🎲","حساب الاحتمالات"),
            ("geometry","الهندسة في الفضاء","🧊","الهندسة الفراغية"),
        ]),
        make_subject("physics","العلوم الفيزيائية","⚛️","الميكانيك والكهرباء",[
            ("mechanics","الميكانيك","🚀","قوانين نيوتن"),
            ("nuclear","التحولات النووية","☢️","النشاط الإشعاعي"),
            ("electricity","الكهرباء","⚡","الظواهر الكهربائية"),
            ("kinetics","المتابعة الزمنية","⏱️","التحولات الكيميائية"),
        ]),
        make_subject("philosophy","الفلسفة","🧠","المقالات",[
            ("mind-body","العقل والجسد","🧠","العلاقة بينهما"),
            ("truth","الحقيقة","🔍","البحث عنها"),
            ("freedom","الحرية","🕊️","الحرية والمسؤولية"),
            ("art","الفن","🎨","الفن والجمال"),
            ("science","العلم والتقنية","🔬","العلم والتقنية"),
        ]),
        make_subject("arabic","اللغة العربية","📖","الشعر والنثر",[
            ("abbasid-poetry","الشعر العباسي","🖋️","المتنبي"),
            ("abbasid-prose","النثر العباسي","📜","الجاحظ"),
            ("modern-poetry","الشعر الحديث","🌙","الحداثة"),
            ("article","المقالة","📰","فن المقالة"),
            ("story","القصة القصيرة","📚","فن القصة"),
        ]),
        make_subject("history","التاريخ والجغرافيا","🌍","تاريخ وجغرافيا",[
            ("revolution","الثورة التحريرية","🇩🇿","ثورة نوفمبر"),
            ("world-history","التاريخ العالمي","🌐","الحروب العالمية"),
            ("physical-geo","الجغرافيا الطبيعية","🗺️","التضاريس"),
            ("human-geo","الجغرافيا البشرية","👥","السكان"),
        ]),
        make_subject("french","الفرنسية","🇫🇷","اللغة الفرنسية",[
            ("grammar-fr","القواعد","📝","Grammaire"),
            ("text-fr","النصوص","📖","Textes"),
            ("expression-fr","التعبير","✍️","Expression"),
        ]),
        make_subject("english","الإنجليزية","🇬🇧","English",[
            ("grammar-en","القواعد","📝","Grammar"),
            ("text-en","النصوص","📖","Texts"),
            ("expression-en","التعبير","✍️","Writing"),
        ]),
        make_subject("islamic","العلوم الإسلامية","🕌","العلوم الإسلامية",[
            ("quran","القرآن الكريم","📗","التفسير"),
            ("hadith","الحديث النبوي","📘","السنة"),
            ("aqida","العقيدة","🕋","الإيمان"),
        ]),
    ]},
    {"slug":"math-stream","name":"رياضيات","icon":"📐","description":"الرياضيات والفيزياء","gradient":"from-cyan-400 to-blue-500","subjects":[
        make_subject("math","الرياضيات","📐","برنامج متقدم",[
            ("functions","الدوال العددية","📈","النهايات"),
            ("arithmetic","الأعداد والحساب","🔢","الموافقات"),
            ("complex","الأعداد المركبة","🔮","العقدية"),
            ("sequences","المتتاليات","🔗","الحسابية"),
            ("integration","التكامل","∫","الدوال الأصلية"),
            ("probability","الاحتمالات","🎲","الاحتمالات"),
            ("geometry","الهندسة","🧊","الفضاء"),
        ]),
        make_subject("physics","العلوم الفيزيائية","⚛️","الميكانيك",[
            ("mechanics","الميكانيك","🚀","نيوتن"),
            ("nuclear","التحولات النووية","☢️","الإشعاع"),
            ("electricity","الكهرباء","⚡","الظواهر"),
        ]),
        make_subject("philosophy","الفلسفة","🧠","المقالات",[
            ("mind-body","العقل والجسد","🧠","العلاقة"),
            ("truth","الحقيقة","🔍","البحث"),
        ]),
        make_subject("arabic","اللغة العربية","📖","الشعر والنثر",[
            ("abbasid-poetry","الشعر العباسي","🖋️","المتنبي"),
            ("article","المقالة","📰","الفن"),
        ]),
        make_subject("french","الفرنسية","🇫🇷","اللغة",[
            ("grammar-fr","القواعد","📝","Grammaire"),
        ]),
        make_subject("english","الإنجليزية","🇬🇧","English",[
            ("grammar-en","القواعد","📝","Grammar"),
        ]),
        make_subject("history","التاريخ والجغرافيا","🌍","تاريخ",[
            ("revolution","الثورة","🇩🇿","نوفمبر"),
        ]),
    ]},
    {"slug":"technique","name":"تقني رياضي","icon":"⚙️","description":"هندسة وتقنية","gradient":"from-orange-400 to-red-500","subjects":[
        make_subject("math","الرياضيات","📐","الرياضيات",[
            ("functions","الدوال","📈","النهايات"),
            ("sequences","المتتاليات","🔢","الحسابية"),
            ("complex","الأعداد المركبة","🔮","العقدية"),
            ("geometry","الهندسة","🧊","الفضاء"),
        ]),
        make_subject("physics","الفيزياء","⚛️","الميكانيك",[
            ("mechanics","الميكانيك","🚀","نيوتن"),
            ("electricity","الكهرباء","⚡","الظواهر"),
            ("nuclear","التحولات النووية","☢️","الإشعاع"),
        ]),
        make_subject("technology","التكنولوجيا","⚙️","هندسة",[
            ("civil","الهندسة المدنية","🏗️","المنشآت"),
            ("mechanical","الهندسة الميكانيكية","🔧","الآلات"),
            ("electrical","الهندسة الكهربائية","💡","الدارات"),
            ("process","هندسة الطرائق","⚗️","العمليات"),
        ]),
        make_subject("philosophy","الفلسفة","🧠","المقالات",[
            ("science","العلم والتقنية","🔬","التقنية"),
            ("mind-body","العقل والجسد","🧠","العلاقة"),
        ]),
        make_subject("arabic","اللغة العربية","📖","الشعر",[
            ("abbasid-poetry","الشعر العباسي","🖋️","المتنبي"),
        ]),
        make_subject("french","الفرنسية","🇫🇷","اللغة",[
            ("grammar-fr","القواعد","📝","Grammaire"),
        ]),
        make_subject("english","الإنجليزية","🇬🇧","English",[
            ("grammar-en","القواعد","📝","Grammar"),
        ]),
    ]},
    {"slug":"gestion","name":"تسيير واقتصاد","icon":"📊","description":"محاسبة واقتصاد","gradient":"from-yellow-400 to-amber-500","subjects":[
        make_subject("accounting","التسيير المحاسبي","📊","المحاسبة",[
            ("intro","مدخل إلى المحاسبة","📊","المفاهيم"),
            ("balance","الميزانية","⚖️","التوازن"),
            ("closing","الحسابات الختامية","📉","النتائج"),
            ("flows","التدفقات المالية","💵","الخزينة"),
            ("analytical","المحاسبة التحليلية","📈","التكاليف"),
        ]),
        make_subject("economy","الاقتصاد والمناجمنت","💼","اقتصاد",[
            ("supply-demand","العرض والطلب","📊","السوق"),
            ("elasticity","المرونة","📉","المرونة"),
            ("consumer","نظرية المستهلك","🛒","الاستهلاك"),
            ("producer","نظرية المنتج","🏭","الإنتاج"),
            ("algerian","الاقتصاد الجزائري","🇩🇿","الاقتصاد"),
        ]),
        make_subject("math","الرياضيات","📐","الرياضيات",[
            ("functions","الدوال","📈","النهايات"),
            ("sequences","المتتاليات","🔢","الحسابية"),
            ("probability","الاحتمالات","🎲","الاحتمالات"),
        ]),
        make_subject("law","القانون","⚖️","قانون",[
            ("civil","القانون المدني","⚖️","العقود"),
            ("commercial","القانون التجاري","💼","التجارة"),
            ("work","قانون العمل","👷","العمل"),
            ("admin","القانون الإداري","🏛️","الإدارة"),
        ]),
        make_subject("philosophy","الفلسفة","🧠","المقالات",[
            ("mind-body","العقل والجسد","🧠","العلاقة"),
            ("state","الدولة","🏛️","المجتمع"),
        ]),
        make_subject("arabic","اللغة العربية","📖","الشعر",[
            ("abbasid-poetry","الشعر العباسي","🖋️","المتنبي"),
        ]),
        make_subject("french","الفرنسية","🇫🇷","اللغة",[
            ("grammar-fr","القواعد","📝","Grammaire"),
        ]),
        make_subject("english","الإنجليزية","🇬🇧","English",[
            ("grammar-en","القواعد","📝","Grammar"),
        ]),
        make_subject("history","التاريخ والجغرافيا","🌍","تاريخ",[
            ("revolution","الثورة","🇩🇿","نوفمبر"),
        ]),
    ]},
    {"slug":"letters","name":"آداب وفلسفة","icon":"📚","description":"فلسفة وعربية وتاريخ","gradient":"from-purple-400 to-pink-500","subjects":[
        make_subject("philosophy","الفلسفة","🧠","المقالات",[
            ("mind-body","العقل والجسد","🧠","العلاقة"),
            ("truth","الحقيقة","🔍","البحث"),
            ("freedom","الحرية","🕊️","المسؤولية"),
            ("art","الفن","🎨","الجمال"),
            ("science","العلم والتقنية","🔬","التقنية"),
            ("state","الدولة","🏛️","المجتمع"),
            ("language","اللغة","🗣️","التواصل"),
            ("ethics","الأخلاق","⚖️","القيم"),
            ("history","التاريخ","📜","الزمن"),
        ]),
        make_subject("arabic","اللغة العربية","📖","الشعر والنثر",[
            ("abbasid-poetry","الشعر العباسي","🖋️","المتنبي"),
            ("abbasid-prose","النثر العباسي","📜","الجاحظ"),
            ("modern-poetry","الشعر الحديث","🌙","الحداثة"),
            ("article","المقالة","📰","الفن"),
            ("story","القصة","📚","فن القصة"),
            ("novel","الرواية","📕","فن الرواية"),
            ("theater","المسرح","🎭","المسرح"),
        ]),
        make_subject("history","التاريخ والجغرافيا","🌍","تاريخ",[
            ("revolution","الثورة التحريرية","🇩🇿","نوفمبر"),
            ("world-history","التاريخ العالمي","🌐","الحروب"),
            ("physical-geo","الجغرافيا الطبيعية","🗺️","التضاريس"),
            ("human-geo","الجغرافيا البشرية","👥","السكان"),
            ("economic-geo","الجغرافيا الاقتصادية","💰","الاقتصاد"),
        ]),
        make_subject("islamic","العلوم الإسلامية","🕌","العلوم الإسلامية",[
            ("quran","القرآن الكريم","📗","التفسير"),
            ("hadith","الحديث النبوي","📘","السنة"),
            ("aqida","العقيدة","🕋","الإيمان"),
        ]),
        make_subject("french","الفرنسية","🇫🇷","اللغة",[
            ("grammar-fr","القواعد","📝","Grammaire"),
            ("text-fr","النصوص","📖","Textes"),
        ]),
        make_subject("english","الإنجليزية","🇬🇧","English",[
            ("grammar-en","القواعد","📝","Grammar"),
            ("text-en","النصوص","📖","Texts"),
        ]),
        make_subject("math","الرياضيات","📐","الرياضيات",[
            ("functions","الدوال","📈","النهايات"),
        ]),
    ]},
    {"slug":"languages","name":"لغات أجنبية","icon":"🌐","description":"فرنسية وإنجليزية وألمانية وإسبانية","gradient":"from-teal-400 to-cyan-500","subjects":[
        make_subject("french","الفرنسية","🇫🇷","اللغة الفرنسية",[
            ("grammar-fr","القواعد","📝","Grammaire"),
            ("text-fr","النصوص","📖","Textes"),
            ("expression-fr","التعبير","✍️","Expression"),
            ("literature-fr","الأدب","📚","Littérature"),
        ]),
        make_subject("english","الإنجليزية","🇬🇧","English",[
            ("grammar-en","القواعد","📝","Grammar"),
            ("text-en","النصوص","📖","Texts"),
            ("expression-en","التعبير","✍️","Writing"),
            ("literature-en","الأدب","📚","Literature"),
        ]),
        make_subject("german","الألمانية","🇩🇪","Deutsch",[
            ("grammar-de","القواعد","📝","Grammatik"),
            ("text-de","النصوص","📖","Texte"),
            ("expression-de","التعبير","✍️","Ausdruck"),
        ]),
        make_subject("spanish","الإسبانية","🇪🇸","Español",[
            ("grammar-es","القواعد","📝","Gramática"),
            ("text-es","النصوص","📖","Textos"),
            ("expression-es","التعبير","✍️","Expresión"),
        ]),
        make_subject("arabic","اللغة العربية","📖","العربية",[
            ("abbasid-poetry","الشعر العباسي","🖋️","المتنبي"),
            ("article","المقالة","📰","الفن"),
        ]),
        make_subject("philosophy","الفلسفة","🧠","المقالات",[
            ("mind-body","العقل والجسد","🧠","العلاقة"),
            ("science","العلم والتقنية","🔬","التقنية"),
        ]),
        make_subject("history","التاريخ والجغرافيا","🌍","تاريخ",[
            ("revolution","الثورة","🇩🇿","نوفمبر"),
        ]),
        make_subject("islamic","العلوم الإسلامية","🕌","العلوم",[
            ("quran","القرآن","📗","التفسير"),
        ]),
    ]},
]

# كتابة الملف النهائي
with open('data.py', 'w', encoding='utf-8') as f:
    f.write("# -*- coding: utf-8 -*-\n\n")
    f.write(f"STREAMS = {json.dumps(DATA, ensure_ascii=False, indent=2)}\n\n")
    f.write("TIPS = [\n")
    f.write('    {"icon": "fa-clock", "title": "نظم وقتك", "desc": "ساعتان يومياً للمراجعة."},\n')
    f.write('    {"icon": "fa-repeat", "title": "راجع باستمرار", "desc": "راجع الوحدة السابقة قبل الجديدة."},\n')
    f.write('    {"icon": "fa-pen-fancy", "title": "حل المواضيع", "desc": "ابدأ بحل مواضيع البكالوريا مبكراً."},\n')
    f.write('    {"icon": "fa-brain", "title": "اختبر نفسك", "desc": "استخدم الاختبارات لمعرفة نقاط ضعفك."}\n')
    f.write("]\n\n")
    f.write("EXAMS_ARCHIVE = [\n")
    f.write('    {"year": "2025", "subject": "علوم تجريبية", "url": "https://www.snvdz.com/", "source": "SNVDZ"},\n')
    f.write('    {"year": "2024", "subject": "علوم تجريبية", "url": "https://eddirasa.com/", "source": "Eddirasa"}\n')
    f.write("]\n")

# حساب الإحصائيات
total_streams = len(DATA)
total_subjects = sum(len(s["subjects"]) for s in DATA)
total_units = sum(len(sub["units"]) for s in DATA for sub in s["subjects"])
total_videos = total_units * 5
print(f"✅ تم توليد data.py بنجاح!")
print(f"📊 الشعب: {total_streams}")
print(f"📚 المواد: {total_subjects}")
print(f"📖 الوحدات: {total_units}")
print(f"🎬 الفيديوهات: {total_videos}")
