import os

# 1. تحديث صفحة عرض الاختبار (exam_view.html) لتكون أكثر إحكاماً
exam_view_html = '''{% extends "base.html" %}
{% block title %}{{ exam.subject }} | امتحان تجريبي{% endblock %}
{% block content %}
<div class="pt-24 pb-20 px-4 max-w-3xl mx-auto">
    <!-- رأس الصفحة -->
    <div class="glass rounded-2xl p-4 md:p-5 mb-6 flex flex-col md:flex-row items-center justify-between gap-4 border-t-4 border-t-brand-green sticky top-20 z-40 bg-black/80 backdrop-blur-md">
        <div class="text-center md:text-right">
            <h1 class="text-xl md:text-2xl font-black text-white">{{ exam.subject }}</h1>
            <p class="text-brand-green text-sm font-bold">{{ exam.stream }}</p>
        </div>
        <div class="flex items-center gap-3 bg-black/50 px-4 py-2 rounded-xl border border-white/10">
            <i class="fa-solid fa-stopwatch text-2xl text-yellow-400"></i>
            <div id="timer" class="text-2xl font-black text-white font-mono tracking-wider">...</div>
        </div>
    </div>

    <form id="examForm" class="space-y-6">
        {% for ex in exam.exercises %}
        <div class="glass rounded-2xl p-4 md:p-6">
            <h2 class="text-lg font-bold text-brand-green mb-3 border-b border-white/10 pb-2">{{ ex.title }}</h2>
            <div class="text-gray-300 text-sm md:text-base leading-relaxed whitespace-pre-wrap mb-4 bg-white/5 p-3 rounded-lg">{{ ex.text }}</div>
            
            <textarea name="answer_{{ loop.index }}" rows="3" 
                class="w-full bg-black/60 border border-white/10 rounded-xl p-3 text-sm text-white focus:border-brand-green outline-none transition resize-y" 
                placeholder="اكتب إجابتك هنا باختصار..."></textarea>
            
            <div class="correction-box hidden mt-3 p-3 rounded-xl bg-green-500/10 border border-green-500/30 text-green-100 text-sm">
                <strong class="block mb-1 text-green-400"><i class="fa-solid fa-check-circle"></i> نموذج الإجابة:</strong>
                <div class="whitespace-pre-wrap leading-relaxed">{{ ex.correction }}</div>
            </div>
        </div>
        {% endfor %}
        
        <button type="submit" class="w-full btn-neon py-4 rounded-xl text-lg font-black mb-8 shadow-lg shadow-brand-green/20">
            <i class="fa-solid fa-paper-plane ml-2"></i> تسليم الامتحان وعرض التصحيح
        </button>
    </form>
</div>

<script>
    // مؤقت (ساعتان)
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

    // عرض التصحيح
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
print("✅ تم تصغير وتجميل صفحة الاختبار")

# 2. تحديث صفحة مركز الاختبارات (exam_center.html) لتكون أكثر احترافية
exam_center_html = '''{% extends "base.html" %}
{% block title %}مركز الاختبارات | BAC 2026{% endblock %}
{% block content %}
<div class="pt-28 pb-20 px-4 md:px-6 max-w-5xl mx-auto">
    <div class="text-center mb-10 md:mb-16">
        <h1 class="text-4xl md:text-6xl font-black mb-3 text-white">مركز <span class="text-glow">الاختبارات</span></h1>
        <p class="text-gray-400 text-sm md:text-base">امتحانات تجريبية شاملة بنمط البكالوريا الجزائرية</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {% for exam in exams %}
        <a href="/exam-center/{{ exam.slug }}" class="glass glass-hover rounded-2xl p-5 relative overflow-hidden group flex flex-col">
            <div class="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br {{ exam.color }} opacity-10 rounded-bl-full group-hover:scale-150 transition-transform"></div>
            
            <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br {{ exam.color }} flex items-center justify-center text-2xl shrink-0">{{ exam.icon }}</div>
                <div>
                    <h3 class="text-lg font-bold text-white leading-tight">{{ exam.subject }}</h3>
                    <p class="text-xs text-brand-green font-bold">{{ exam.stream }}</p>
                </div>
            </div>
            
            <p class="text-sm text-gray-400 mb-5 flex-1">{{ exam.description }}</p>
            
            <div class="flex justify-between items-center text-xs text-gray-500 pt-3 border-t border-white/10">
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
print("✅ تم تصغير وتجميل صفحة مركز الاختبارات")
