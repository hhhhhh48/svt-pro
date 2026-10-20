import os, json, re

# 1. إنشاء ملف بيانات الاختبارات الحقيقية
exams_data = {
    "exams": [
        {
            "slug": "svt-2025",
            "subject": "علوم الطبيعة والحياة",
            "stream": "علوم تجريبية",
            "icon": "🧬",
            "duration": "2 ساعة و 30 دقيقة",
            "color": "from-emerald-500 to-teal-600",
            "description": "امتحان تجريبي شامل في علوم الطبيعة والحياة - مستوى بكالوريا 2025",
            "exercises": [
                {
                    "title": "التمرين الأول: (05 نقاط) - تركيب البروتين",
                    "text": "لاحظ الباحثون أن عملية تركيب البروتين تمر بمراحل دقيقة داخل الخلية. \n1. تعرف على البيانات المرقمة في الوثيقة (غير مرفقة، استعن بمعلوماتك).\n2. اكتب نصاً علمياً تشرح فيه آلية الاستنساخ والترجمة.\n3. ما هو تأثير استبدال قاعدة أزوتية واحدة في شفرة البداية؟",
                    "correction": "1. الاستنساخ: نسخ الـ ADN إلى ARNm في النواة بواسطة ARN بوليميراز. الترجمة: قراءة الشفرات على الريبوزوم بواسطة ARNt لتكوين سلسلة ببتيدية.\n2. نص علمي: ... (يجب أن يتضمن دور الإنزيمات والطاقة).\n3. يؤدي استبدال شفرة البداية إلى عدم بدء الترجمة نهائياً، وبالتالي عدم تصنيع البروتين."
                },
                {
                    "title": "التمرين الثاني: (07 نقاط) - المناعة",
                    "text": "أجريت تجارب على فئران لدراسة الاستجابة المناعية.\n1. قارن بين المناعة الطبيعية والمكتسبة.\n2. فسر سبب ارتفاع درجة الحرارة عند الإصابة بعدوى بكتيرية.\n3. ما هو دور خلايا الذاكرة في التلقيح؟",
                    "correction": "1. المناعة الطبيعية: سريعة، غير نوعية، لا تميز بين مولدات الضد. المناعة المكتسبة: بطيئة، نوعية، تستهدف مولد ضد محدد.\n2. ارتفاع الحرارة هو استجابة التهابية ناتجة عن إفراز مواد كيميائية مثل البروستاغلاندينات التي تؤثر على مركز تنظيم الحرارة في الدماغ لقتل البكتيريا.\n3. خلايا الذاكرة (LB و LT) تبقى في الجسم لفترة طويلة وتستجيب بسرعة وكفاءة أكبر عند التعرض لنفس مولد الضد مرة أخرى."
                },
                {
                    "title": "الوضعية الإدماجية: (08 نقاط) - التنفس والتخمر",
                    "text": "خلال حصة رياضية، شعر أحمد بتعب شديد وتشنجات عضلية. عند تحليل دمه، وجد الأطباء ارتفاعاً في حمض اللاكتيك.\n1. فسر سبب ارتفاع حمض اللاكتيك في عضلات أحمد.\n2. قارن بين التنفس الخلوي والتخمر اللبني من حيث المردود الطاقوي.\n3. اقترح نصائح لأحمد لتجنب هذه المشكلة.",
                    "correction": "1. أثناء المجهود العضلي العنيف ونقص الأكسجين، تلجأ الخلايا العضلية إلى التخمر اللبني لإنتاج الطاقة، مما يؤدي إلى تراكم حمض اللاكتيك المسبب للتشنجات.\n2. التنفس الخلوي: مع الأكسجين، إنتاج 36 ATP. التخمر اللبني: بدون أكسجين، إنتاج 2 ATP فقط.\n3. النصائح: الإحماء قبل الرياضة، التنفس بعمق، التدرج في المجهود، وشرب الماء."
                }
            ]
        },
        {
            "slug": "math-2025",
            "subject": "الرياضيات",
            "stream": "علوم تجريبية / رياضيات",
            "icon": "📐",
            "duration": "3 ساعات",
            "color": "from-blue-500 to-indigo-600",
            "description": "امتحان تجريبي في الرياضيات - يتضمن تمارين في الدوال، المتتاليات، والأعداد المركبة.",
            "exercises": [
                {
                    "title": "التمرين الأول: (04 نقاط) - الدوال",
                    "text": "نعتبر الدالة f المعرفة على R بـ: f(x) = x^3 - 3x + 1.\n1. ادرس تغيرات الدالة f.\n2. اكتب معادلة المماس للدالة f عند النقطة ذات الفاصلة 0.\n3. أنشئ الجدول التغيرات.",
                    "correction": "1. f'(x) = 3x^2 - 3. f'(x) = 0 => x = 1 أو x = -1. f متزايدة على ]-∞,-1[ و ]1,+∞[ ومتناقصة على ]-1,1[.\n2. f'(0) = -3، f(0) = 1. معادلة المماس: y = -3x + 1.\n3. الجدول: ..."
                },
                {
                    "title": "التمرين الثاني: (05 نقاط) - المتتاليات",
                    "text": "لتكن (Un) المتتالية المعرفة بـ: U0 = 1 و Un+1 = (Un + 2)/3.\n1. برهن بالتراجع أن 0 < Un < 1.\n2. ادرس رتابة المتتالية.\n3. احسب النهاية.",
                    "correction": "1. بالتراجع: من أجل n=0 صحيح. نفرض 0 < Un < 1 ونبرهن 0 < Un+1 < 1...\n2. Un+1 - Un = (2 - 2Un)/3. بما أن Un < 1 فإن الفرق موجب، إذن المتتالية متزايدة.\n3. المتتالية متزايدة ومحدودة بـ 1، إذن تتقارب. النهاية l تحقق l = (l+2)/3 => l = 1."
                },
                {
                    "title": "التمرين الثالث: (06 نقاط) - الأعداد المركبة",
                    "text": "في المستوي المركب، نعتبر النقط A, B, C ذات اللواحق: zA = 1+i, zB = 2-i, zC = 3.\n1. احسب الطول AB.\n2. ما هي طبيعة المثلث ABC؟\n3. عين مجموعة النقط M(z) التي تحقق |z - zA| = |z - zB|.",
                    "correction": "1. AB = |zB - zA| = |1 - 2i| = √5.\n2. AC = |2-i| = √5، BC = |1+i| = √2. المثلث متساوي الساقين.\n3. محور القطعة [AB]."
                }
            ]
        },
        {
            "slug": "physics-2025",
            "subject": "العلوم الفيزيائية",
            "stream": "علوم تجريبية",
            "icon": "⚛️",
            "duration": "3 ساعات",
            "color": "from-orange-500 to-red-600",
            "description": "امتحان تجريبي في الفيزياء - الميكانيك، الكهرباء، والتحولات النووية.",
            "exercises": [
                {
                    "title": "التمرين الأول: (06 نقاط) - الميكانيك",
                    "text": "ينزلق جسم كتلته m = 0.5 kg على مستوى مائل بزاوية α = 30° من نقطة A إلى نقطة B طولها 4m.\n1. مثل القوى المؤثرة على الجسم.\n2. احسب عمل قوة الثقل.\n3. إذا كانت السرعة في A معدومة، احسب السرعة في B (نهمل الاحتكاك، g=10).",
                    "correction": "1. القوى: الثقل P، رد الفعل R.\n2. W(P) = m*g*h = m*g*AB*sin(α) = 0.5*10*4*0.5 = 10 J.\n3. بتطبيق مبدأ انحفاظ الطاقة: Ec(B) = W(P) => 0.5*m*vB^2 = 10 => vB = √(40) ≈ 6.32 m/s."
                },
                {
                    "title": "التمرين الثاني: (07 نقاط) - الكهرباء",
                    "text": "دارة كهربائية تتكون من مولد (E=12V, r=1Ω)، ناقل أومي (R=5Ω)، ومكثف (C=10µF).\n1. احسب شدة التيار في الدارة.\n2. احسب التوتر بين طرفي المكثف.\n3. احسب الطاقة المخزنة في المكثف.",
                    "correction": "1. I = E / (R+r) = 12 / 6 = 2 A.\n2. Uc = R*I = 10 V.\n3. Ec = 0.5 * C * U^2 = 0.5 * 10e-6 * 100 = 5e-4 J."
                }
            ]
        }
    ]
}

# 2. حفظ البيانات
with open('exams_data.json', 'w', encoding='utf-8') as f:
    json.dump(exams_data, f, ensure_ascii=False, indent=2)

# 3. تحديث app.py لإضافة المسارات
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

if '/exam-center' not in app_code:
    routes = '''
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
'''
    app_code = app_code.replace("if __name__ == '__main__':", routes + "\nif __name__ == '__main__':")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_code)

# 4. إنشاء صفحة عرض الاختبارات
exam_center_html = '''{% extends "base.html" %}
{% block title %}مركز الاختبارات | BAC 2026{% endblock %}
{% block content %}
<div class="pt-32 pb-20 px-6 max-w-6xl mx-auto">
    <div class="text-center mb-16">
        <h1 class="text-5xl md:text-7xl font-black mb-4 text-white">مركز <span class="text-glow">الاختبارات</span></h1>
        <p class="text-xl text-gray-400">امتحانات تجريبية شاملة بنمط البكالوريا الجزائرية</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {% for exam in exams %}
        <a href="/exam-center/{{ exam.slug }}" class="glass glass-hover rounded-3xl p-8 relative overflow-hidden group">
            <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br {{ exam.color }} opacity-10 rounded-bl-full group-hover:scale-150 transition-transform"></div>
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br {{ exam.color }} flex items-center justify-center text-3xl mb-6">{{ exam.icon }}</div>
            <h3 class="text-2xl font-bold text-white mb-2">{{ exam.subject }}</h3>
            <p class="text-sm text-brand-green font-bold mb-4">{{ exam.stream }}</p>
            <p class="text-sm text-gray-400 mb-6">{{ exam.description }}</p>
            <div class="flex justify-between items-center text-xs text-gray-500 pt-4 border-t border-white/5">
                <span><i class="fa-regular fa-clock ml-1"></i> {{ exam.duration }}</span>
                <span><i class="fa-solid fa-file-lines ml-1"></i> {{ exam.exercises|length }} تمارين</span>
            </div>
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}'''
with open('templates/exam_center.html', 'w', encoding='utf-8') as f:
    f.write(exam_center_html)

# 5. إنشاء صفحة أداء الاختبار (مع المؤقت)
exam_view_html = '''{% extends "base.html" %}
{% block title %}{{ exam.subject }} | امتحان تجريبي{% endblock %}
{% block content %}
<div class="pt-24 pb-20 px-4 max-w-4xl mx-auto">
    <div class="glass rounded-3xl p-6 md:p-8 mb-8 flex flex-col md:flex-row items-center justify-between gap-4 border-t-4 border-t-brand-green">
        <div>
            <h1 class="text-2xl md:text-3xl font-black text-white">{{ exam.subject }}</h1>
            <p class="text-brand-green font-bold">{{ exam.stream }}</p>
        </div>
        <div class="flex items-center gap-4 bg-black/40 px-6 py-3 rounded-2xl border border-white/10">
            <i class="fa-solid fa-stopwatch text-3xl text-yellow-400"></i>
            <div id="timer" class="text-3xl font-black text-white font-mono">...</div>
        </div>
    </div>

    <form id="examForm">
        {% for ex in exam.exercises %}
        <div class="glass rounded-3xl p-6 md:p-8 mb-8">
            <h2 class="text-xl font-bold text-brand-green mb-4 border-b border-white/10 pb-3">{{ ex.title }}</h2>
            <div class="text-gray-300 leading-relaxed whitespace-pre-wrap mb-6">{{ ex.text }}</div>
            <textarea name="answer_{{ loop.index }}" rows="6" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 text-white focus:border-brand-green outline-none" placeholder="اكتب إجابتك هنا..."></textarea>
            <div class="correction-box hidden mt-4 p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-green-200 text-sm">
                <strong class="block mb-2 text-green-400"><i class="fa-solid fa-check-circle"></i> نموذج الإجابة:</strong>
                <div class="whitespace-pre-wrap">{{ ex.correction }}</div>
            </div>
        </div>
        {% endfor %}
        <button type="submit" class="w-full btn-neon py-5 rounded-2xl text-xl font-black mb-8">تسليم الامتحان وعرض التصحيح</button>
    </form>
</div>

<script>
    // مؤقت (ساعتان افتراضياً)
    let time = 120 * 60;
    const timerEl = document.getElementById('timer');
    const interval = setInterval(() => {
        if(time <= 0) { clearInterval(interval); timerEl.textContent = '00:00:00'; return; }
        time--;
        const h = String(Math.floor(time / 3600)).padStart(2, '0');
        const m = String(Math.floor((time % 3600) / 60)).padStart(2, '0');
        const s = String(time % 60).padStart(2, '0');
        timerEl.textContent = `${h}:${m}:${s}`;
        if(time < 300) timerEl.classList.add('text-red-500', 'animate-pulse');
    }, 1000);

    // عرض التصحيح عند التسليم
    document.getElementById('examForm').addEventListener('submit', function(e) {
        e.preventDefault();
        if(!confirm('هل أنت متأكد من تسليم الامتحان؟ سيتم عرض التصحيح.')) return;
        clearInterval(interval);
        document.querySelectorAll('.correction-box').forEach(box => box.classList.remove('hidden'));
        document.querySelector('button[type="submit"]').style.display = 'none';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
</script>
{% endblock %}'''
with open('templates/exam_view.html', 'w', encoding='utf-8') as f:
    f.write(exam_view_html)

print("✅ تم بناء مركز الاختبارات بنجاح! (3 امتحانات حقيقية)")
