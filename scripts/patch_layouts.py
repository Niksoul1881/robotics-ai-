"""Одноразовая адаптация шаблонов биологии под «Промышленный ML».

Каждая замена проверяется: если исходная строка не найдена — скрипт ругается,
чтобы не было тихой потери текста.
    python scripts/patch_layouts.py
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parent.parent

INDEX = [
    # hero: символы и прогрессия
    ('>2n</span>', '>Ø12 H7</span>'),
    ('>Aa</span>', '>0,1%</span>'),
    ('>C₆H₁₂O₆</span>', '>v = 1200</span>'),
    ('>ДНК</span>', '>G1 X102</span>'),
    ('<span class="num">5</span>', '<span class="num">цех</span>'),
    ('<span class="num">11</span>', '<span class="num">данные</span>'),
    ('<span class="num accent">Био-IT</span>', '<span class="num accent">модель</span>'),
    ('<span>класс: растения, животные, человек</span>', '<span>что происходит на заводе</span>'),
    ('<span>класс + ЕГЭ: клетка, генетика</span>', '<span>как выглядят данные с оборудования</span>'),
    ('<span class="accent">биоинформатика, геномика, ML</span>', '<span class="accent">модели, метрики, внедрение</span>'),
    ('Один непрерывный курс биологии — от строения цветка до того, как нейросети предсказывают форму белков и ищут новые лекарства. Со схемами, рисунками и заданиями ОГЭ и ЕГЭ в каждом уроке.',
     'Один непрерывный курс: от того, что такое допуск и износ фрезы, до модели, которая ловит дефект на конвейере. С аналогиями, схемами, рабочим кодом и ценой ошибки в каждом уроке.'),
    ('href="/obshchaya-biologiya/088-organoidy-kletki/" class="btn btn-secondary">Пример урока',
     'href="/proizvodstvo/" class="btn btn-secondary">Первый курс'),
    ('300 уроков', '204 урока'),
    # заголовки разделов
    ('{{ len site.Data.program.courses }} курсов: от школы до биоинформатики',
     '{{ len site.Data.program.courses }} курсов: от станка до модели'),
    ('Школьная биология, подготовка к экзаменам и то, чего почти нет на русском: биология для программистов, геномика и ML',
     'Производство, сигналы, зрение и предиктивное обслуживание — то, что нужно, чтобы работать с данными реального завода'),
    ('<h2>Почему Биология AI?</h2>', '<h2>Почему Промышленный ML?</h2>'),
    ('Биология — это картинки и понимание, а не зубрёжка терминов',
     'Механику нельзя выучить по формулам: её надо увидеть, потрогать и посчитать на данных'),
    # карточки «Почему»
    ('<h3>Схемы и рисунки</h3>', '<h3>Схемы и аналогии</h3>'),
    ('В каждом уроке 4–8 научных иллюстраций: клетки, органы, циклы, процессы — с подписями на русском',
     'В каждом уроке 5–8 своих схем: как устроен узел, как он выглядит в данных, что будет при ошибке'),
    ('<h3>30 заданий в формате экзамена</h3>', '<h3>20 заданий с кодом</h3>'),
    ('Выбор, соответствие, последовательность, задачи по генетике — как на ОГЭ и ЕГЭ, с подробными решениями',
     'Предсказать вывод, найти утечку данных, выбрать метрику под сценарий — с разбором каждого решения'),
    ('<h3>Понимание, а не зубрёжка</h3>', '<h3>Разжёванная механика</h3>'),
    ('Почему клетка устроена именно так: строение и функция, история открытий, аналогии из жизни',
     'Каждое понятие: аналогия из жизни → схема → разбор с числами → где аналогия ломается'),
    ('<h3>Биология будущего</h3>', '<h3>Цена ошибки</h3>'),
    ('В каждом уроке — где тема работает в биотехнологиях, медицине, агротехе и биоинформатике',
     'У каждой модели сказано, сколько стоит ложная тревога и сколько — пропущенный дефект'),
    ('<h3>Биоинформатика с нуля</h3>', '<h3>Данные и метрики</h3>'),
    ('Python, алгоритмы выравнивания, геномика, AlphaFold — понятным языком, на русском',
     'Открытые датасеты (NASA C-MAPSS, MVTec AD), ваш код, ваши метрики — не «посмотрели, как обучают»'),
    # CTA
    ('<h2>Начни с клетки — дойди до нейросетей</h2>', '<h2>Начни с цеха — дойди до модели</h2>'),
    ('Выбери тему в программе: от школьной ботаники до геномики и ML',
     'Выбери курс в программе: от производства для айтишника до предиктивного обслуживания'),
]

# секция «Экзамены» целиком заменяется на «С чего начать»
EXAMS_OLD_START = '<!-- Экзамены -->'
EXAMS_NEW = '''<!-- С чего начать -->
<section class="exam-promo fade-in">
    <div class="section-container">
        <div class="section-header">
            <span class="section-badge">С чего начать</span>
            <h2>Три входа — по твоему опыту</h2>
            <p>Не знаешь, что такое допуск и фреза, — начинай с производства. Знаешь Python и ML — иди сразу в ядро.</p>
        </div>
        <div class="exam-promo-grid">
            <a class="exam-promo-card" href="/proizvodstvo/">
                <span class="exam-promo-kicker">Новичок в железе</span>
                <h3>Производство для айтишника</h3>
                <p>16 уроков: как устроен цех, что такое допуск, откуда берётся вибрация и как читать задание технолога.</p>
                <span class="exam-promo-link">Начать с курса 1 →</span>
            </a>
            <a class="exam-promo-card" href="/ml-bazis/">
                <span class="exam-promo-kicker">Уже в ML</span>
                <h3>ML на промышленных данных</h3>
                <p>20 уроков: бустинг, валидация по времени, утечки данных, метрики и цена ошибки на реальном производстве.</p>
                <span class="exam-promo-link">Перейти к курсу 3 →</span>
            </a>
        </div>
    </div>
</section>
'''

FUTURE_OLD_START = '<!-- Биология будущего -->'
FUTURE_NEW = '''<!-- Где это работает -->
<section class="how-it-works fade-in">
    <div class="section-container">
        <div class="section-header">
            <span class="section-badge">Где это нужно</span>
            <h2>Где промышленный ML уже работает</h2>
            <p>Не «в будущем», а на действующих линиях: дефекты, износ, энергия, безопасность</p>
        </div>
        <div class="steps-grid">
            <a class="step-card bio-future" href="/vision/">
                <div class="step-number">👁</div>
                <h3>Контроль качества</h3>
                <p>Камера над конвейером ловит царапины и заусенцы быстрее и стабильнее человека</p>
            </a>
            <a class="step-card bio-future" href="/anomalii/">
                <div class="step-number">⚙️</div>
                <h3>Износ и отказы</h3>
                <p>По вибрации и току модель предсказывает поломку до того, как линия встала</p>
            </a>
            <a class="step-card bio-future" href="/ryady/">
                <div class="step-number">⚡</div>
                <h3>Энергия и загрузка</h3>
                <p>Прогноз потребления и нагрузки участка: без него нельзя планировать смены и счета</p>
            </a>
            <a class="step-card bio-future" href="/dannye/">
                <div class="step-number">🔌</div>
                <h3>Данные с оборудования</h3>
                <p>ПЛК, SCADA и историки дают цифры, из которых всё это считается</p>
            </a>
        </div>
    </div>
</section>
'''

BASEOF = [
    ('<span>Биология AI</span>', '<span>Промышленный ML</span>'),
    ('<p>Биология от школьной программы до биоинформатики и машинного обучения: уроки, схемы, задания ОГЭ и ЕГЭ.</p>',
     '<p>Промышленный ML: данные с оборудования, машинное зрение и предиктивное обслуживание. Уроки со схемами, кодом и метриками.</p>'),
    ('<p>© 2026 Биология AI. От клетки до нейросетей</p>', '<p>© 2026 Промышленный ML. От станка до модели</p>'),
    ('Математика онлайн: 350 бесплатных уроков — %s', 'Промышленный ML: %s'),
]


def patch(path, pairs, must_replace=True):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    missed = []
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
        else:
            missed.append(old[:70])
    p.write_text(text, encoding="utf-8")
    print(f"  {path}: заменено {len(pairs) - len(missed)} из {len(pairs)}")
    for m in missed:
        print(f"    НЕ НАЙДЕНО: {m}")


def replace_section(path, start_marker, end_marker, new_block):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    i = text.find(start_marker)
    j = text.find(end_marker)
    if i < 0 or j < 0 or j <= i:
        print(f"  {path}: не найдены маркеры {start_marker} / {end_marker}")
        return
    # сохраняем закрывающий </section> старой секции
    tail = text.find("</section>", i)
    block_end = tail + len("</section>") + 1
    text = text[:i] + new_block + text[block_end:]
    p.write_text(text, encoding="utf-8")
    print(f"  {path}: секция {start_marker} заменена")


print("index.html:")
replace_section("layouts/index.html", EXAMS_OLD_START, FUTURE_OLD_START, EXAMS_NEW)
replace_section("layouts/index.html", FUTURE_OLD_START, "<section class=\"cta-section\">", FUTURE_NEW)
patch("layouts/index.html", INDEX)
print("baseof.html:")
patch("layouts/_default/baseof.html", BASEOF)
print("готово")
