"""PROGRAM.md → data/program.yaml + заготовки уроков в content/.

Заготовка — страница с placeholders: true (noindex, не в sitemap, в программе помечена «скоро»).
Готовые уроки (файл без placeholders) не трогаются. Запуск из корня проекта:
    python scripts/gen_program.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TR = dict(zip("абвгдеёзийклмнопрстуфы", "abvgdeeziyklmnoprstufy"))
TR.update({"ж": "zh", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ь": "", "э": "e", "ю": "yu", "я": "ya"})

COURSES = [  # номер модуля = порядок изучения (маршрут ROUTE.md)
    (1, "elektrika", "Электрика с нуля", "Ток, напряжение, питание, земля, помехи — для тех, у кого электричество это розетка", "#F59E0B", "⚡"),
    (2, "proizvodstvo", "Производство для айтишника", "Станки, допуски, износ, данные с оборудования", "#475569", "🏭"),
    (3, "english", "Технический английский для инженера", "Даташиты, документация и статьи без переводчика", "#0EA5E9", "📘"),
    (4, "matematika", "Математика под задачу", "Только то, что понадобится, со ссылкой на полный урок", "#7C3AED", "∫"),
    (5, "signaly", "Сигналы и измерения", "Вибрация, ток, спектр, признаки из сырых данных", "#0891B2", "📈"),
    (6, "dannye", "Данные с оборудования", "ПЛК, SCADA, OPC UA, историки, метки времени", "#2563EB", "🔌"),
    (7, "ml-bazis", "Классический ML на промышленных данных", "Бустинг, валидация по времени, метрики и цена ошибки", "#C2410C", "🌳"),
    (8, "ryady", "Временные ряды и прогнозирование", "Тренд, сезонность, прогноз нагрузки и энергии", "#0D9488", "⏱"),
    (9, "anomalii", "Детекция аномалий и предиктивное обслуживание", "Без разметки, остаточный ресурс, ложные тревоги", "#B45309", "⚙️"),
    (10, "vision", "Компьютерное зрение", "CNN, детекция, сегментация, дефекты на изображениях", "#7C3AED", "👁"),
    (11, "prom-vision", "Промышленное зрение: физика и стенд", "Свет, объектив, калибровка, синхронизация, приёмка", "#C026D3", "🔬"),
    (12, "prod", "ML в продакшене и edge", "Инференс, задержки, дрейф, мониторинг, откаты", "#DC2626", "🚀"),
    (13, "ekonomika", "Экономика и внедрение", "ROI, пилот, сопротивление людей, стандарты", "#9333EA", "💰"),
    (14, "proekty", "Проекты", "Пять сквозных проектов от постановки до защиты", "#E11D48", "🎯"),
]

# Уроки курса 14 ведут в полный урок на сайте математики: {номер нашего урока: url}
SOURCES = {
    230: "https://www.matematika-ai.ru/base-course/28-procenty/",
    231: "https://www.matematika-ai.ru/high-school/76-ponyatie-funkcii/",
    232: "https://www.matematika-ai.ru/high-school/78-grafik-funkcii/",
    233: "https://www.matematika-ai.ru/high-school/133-proizvodnaya-funkcii-opredelenie/",
    234: "https://www.matematika-ai.ru/high-school/136-pravila-differencirovaniya/",
    235: "https://www.matematika-ai.ru/high-school/137-proizvodnaya-slozhnoy-funkcii/",
    236: "https://www.matematika-ai.ru/ml-course/285-gradientnyy-spusk/",
    237: "https://www.matematika-ai.ru/university/151-vektory-na-ploskosti-i-v-prostranstve/",
    238: "https://www.matematika-ai.ru/university/153-skalyarnoe-proizvedenie/",
    239: "https://www.matematika-ai.ru/university/157-operacii-nad-matricami/",
    240: "https://www.matematika-ai.ru/university/172-sobstvennye-vektory-i-sobstvennye-znacheniya/",
    241: "https://www.matematika-ai.ru/ml-course/227-klassicheskoe-opredelenie-veroyatnosti/",
    242: "https://www.matematika-ai.ru/ml-course/230-uslovnaya-veroyatnost/",
    243: "https://www.matematika-ai.ru/ml-course/232-formula-bayesa/",
    244: "https://www.matematika-ai.ru/ml-course/235-funkciya-raspredeleniya/",
    245: "https://www.matematika-ai.ru/ml-course/236-plotnost-veroyatnosti/",
    246: "https://www.matematika-ai.ru/ml-course/237-matematicheskoe-ozhidanie/",
    247: "https://www.matematika-ai.ru/ml-course/240-osnovnye-raspredeleniya/",
    248: "https://www.matematika-ai.ru/ml-course/241-centralnaya-predelnaya-teorema/",
    249: "https://www.matematika-ai.ru/ml-course/245-vyborka-i-generalnaya-sovokupnost/",
    250: "https://www.matematika-ai.ru/ml-course/246-ocenka-parametrov/",
    251: "https://www.matematika-ai.ru/ml-course/247-proverka-statisticheskih-gipotez/",
    252: "https://www.matematika-ai.ru/ml-course/244-kovariaciya-i-korrelyaciya/",
    253: "https://www.matematika-ai.ru/university/208-ryady-fure/",
    254: "https://www.matematika-ai.ru/ml-course/310-lineynaya-regressiya/",
    255: "https://www.matematika-ai.ru/ml-course/307-metriki-kachestva/",
    256: "https://www.matematika-ai.ru/ml-course/308-roc-krivaya-i-auc/",
    257: "https://www.matematika-ai.ru/ml-course/309-confusion-matrix/",
}


def slug(text):
    t = text.lower().replace("—", " ").replace("–", " ")
    t = "".join(TR.get(c, c) for c in t)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    words = t.split("-")
    out = ""
    for w in words:                      # не длиннее ~60 символов, по словам
        if len(out) + len(w) + 1 > 60:
            break
        out = f"{out}-{w}" if out else w
    return out or "urok"


def parse():
    text = (ROOT / "PROGRAM.md").read_text(encoding="utf-8")
    courses, cur, sec = {}, None, None
    for line in text.splitlines():
        m = re.match(r"^## Курс (\d+)\.", line)
        if m:
            cur = int(m.group(1)); courses[cur] = []; sec = None
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        m = re.match(r"^\*\*Раздел [\d.]+\. (.+)\*\*$", line)
        if m:
            sec = {"title": m.group(1), "lessons": []}; courses[cur].append(sec)
            continue
        m = re.match(r"^(\d+)\. (.+)$", line)
        if m:
            if sec is None:
                sec = {"title": "", "lessons": []}; courses[cur].append(sec)
            sec["lessons"].append((int(m.group(1)), m.group(2).strip()))
    return courses


def main():
    parsed = parse()
    yaml = ["# Сгенерировано scripts/gen_program.py из PROGRAM.md — правь PROGRAM.md и перезапускай", "courses:"]
    made = 0
    for num, d, title, sub, color, emoji in COURSES:
        secs = parsed.get(num, [])
        if not secs:
            print(f"  ВНИМАНИЕ: курс {num} не найден в PROGRAM.md")
            continue
        n = sum(len(s["lessons"]) for s in secs)
        yaml += [f"  - id: {d}", f"    num: {num}", f'    title: "{title}"', f'    subtitle: "{sub}"', f'    color: "{color}"',
                 f'    emoji: "{emoji}"', f"    count: {n}", "    sections:"]
        (ROOT / "content" / d).mkdir(parents=True, exist_ok=True)
        idx = ROOT / "content" / d / "_index.md"
        if not idx.exists():
            idx.write_text(f'---\ntitle: "{title}"\ndescription: "{sub}"\nweight: {num}\n---\n', encoding="utf-8")
        flat = [l for s in secs for l in s["lessons"]]
        idx = 0
        for s in secs:
            yaml += [f'      - title: "{s["title"]}"', "        lessons:"]
            for no, t in s["lessons"]:
                idx += 1
                sl = f"{no:03d}-{slug(t)}"
                existing = list((ROOT / "content" / d).glob(f"{no:03d}-*.md"))
                if existing:
                    sl = existing[0].stem
                yaml.append(f'          - {{ num: {no}, idx: {idx}, slug: "{sl}", title: "{t}" }}')
                f = ROOT / "content" / d / f"{sl}.md"
                if f.exists():
                    continue
                src = SOURCES.get(no)
                src_note = f"\n\nПолный урок по теме: [математика-ai.ru]({src})" if src else ""
                f.write_text(f"""---
title: "{t}"
date: 2026-11-19
lastmod: 2026-11-19
lesson_number: {no}
placeholders: true
weight: {no}
---

{{{{< kratko >}}}}
**Урок готовится.** Здесь будет урок по теме «{t}»: объяснение механики с аналогиями и схемами, разбор данных и метрик, рабочий код с реальным выводом, цена ошибки на производстве и 20 заданий с решениями.
{{{{< /kratko >}}}}

Пока урок пишется, посмотри [всю программу](/program/) — готовые уроки отмечены в ней.{src_note}
""", encoding="utf-8")
                made += 1
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "program.yaml").write_text("\n".join(yaml) + "\n", encoding="utf-8")
    print("заготовок создано:", made)


if __name__ == "__main__":
    main()
