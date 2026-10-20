import os

with open('templates/subject.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'bac-exam' not in html:
    # إضافة الزر بعد رأس المادة مباشرة
    button_html = '''
    {% if subject.bac_exam %}
    <div class="mb-10 text-center md:text-right" data-aos="fade-up">
        <a href="/bac-exam/{{ stream.slug }}/{{ subject.slug }}" class="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-black text-lg shadow-[0_0_30px_rgba(250,204,21,0.3)] hover:scale-105 transition-transform">
            <i class="fa-solid fa-file-signature text-2xl"></i>
            دخول امتحان البكالوريا التجريبي (20 سؤالاً)
        </a>
    </div>
    {% endif %}
    '''
    
    # حقن الزر قبل قائمة الوحدات
    marker = '<h2 class="text-2xl font-bold text-white mb-8">الوحدات والدروس</h2>'
    if marker in html:
        html = html.replace(marker, button_html + '\n    ' + marker)
        with open('templates/subject.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ تمت إضافة زر الامتحان في صفحة المادة.")
    else:
        print("⚠️ لم يتم العثور على مكان الزر في subject.html")
