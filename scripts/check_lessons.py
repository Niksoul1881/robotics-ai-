"""Проверка уроков «Промышленного ML»: не заготовка, объём, картинки на месте,
20 решений, обязательные блоки.

    python scripts/check_lessons.py            # все уроки
    python scripts/check_lessons.py 001 002    # только эти номера
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parent.parent
only = {f"{int(a):03d}" for a in sys.argv[1:]} if len(sys.argv) > 1 else None

bad = n = 0
for f in sorted((ROOT / "content").rglob("[0-9]*.md")):
    if only and not any(f.name.startswith(p) for p in only):
        continue
    s = f.read_text(encoding="utf-8")
    head, _, body = s[3:].partition("\n---")
    if "placeholders: true" in head:
        continue
    n += 1
    figs = re.findall(r'src="(/images/[^"]+)"', s)
    issues = []
    words = len(re.sub(r"\{\{<[^>]*>\}\}", "", body).split())
    if words < 3000:      # уроки с кодом плотнее текстовых: 3000 слов + код = нормальный объём
        issues.append(f"слов {words}")
    if len(figs) < 5:
        issues.append(f"картинок {len(figs)}")
    miss = [x for x in figs if not (ROOT / "static" / x.lstrip("/")).exists()]
    if miss:
        issues.append(f"нет файлов {miss}")
    if s.count("{{< solution >}}") != 20:
        issues.append(f"решений {s.count('{{< solution >}}')}")
    for block in ("Если не работает", "Метрика и цена ошибки", "Данные: что и откуда",
                  "Зачем это на производстве", "Практика: 20 заданий"):
        if block not in s:
            issues.append(f"нет блока «{block}»")
    if "{{< solution >}}" in s and "**Ответ:**" not in s:
        issues.append("нет «Ответ:» в решениях")
    if any(ord(c) < 32 and c not in "\n\r\t" for c in s):
        issues.append("управляющие символы")
    if s.startswith("\ufeff"):
        issues.append("BOM в начале файла")
    if issues:
        bad += 1
        print(f"  {f.relative_to(ROOT)}: {', '.join(issues)}")

print(f"уроков готово: {n}, с замечаниями: {bad}")
