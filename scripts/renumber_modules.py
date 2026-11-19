"""Перенумеровывает модули под порядок изучения (маршрут ROUTE.md).

Было: номера присваивались по мере создания курсов.
Стало: модуль 1 — то, с чего начинаешь.

Меняет: course_num в frontmatter уроков, num в data/program.yaml,
COURSES в scripts/gen_program.py, заголовки «## Курс N.» в PROGRAM.md.
Номера уроков (001, 205, 233…) НЕ меняются — это адреса, а не порядок.

    python scripts/renumber_modules.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parent.parent

# старый номер -> новый
MAP = {12: 1, 1: 2, 13: 3, 14: 4, 2: 5, 9: 6, 3: 7, 4: 8,
       5: 9, 6: 10, 7: 11, 8: 12, 10: 13, 11: 14}

changed = 0
for f in (ROOT / "content").rglob("[0-9]*.md"):
    text = f.read_text(encoding="utf-8")
    m = re.search(r"(?m)^course_num: (\d+)$", text)
    if not m:
        continue
    old = int(m.group(1))
    if old not in MAP:
        continue
    new = MAP[old]
    if old == new:
        continue
    text = re.sub(r"(?m)^course_num: \d+$", f"course_num: {new}", text, count=1)
    f.write_text(text, encoding="utf-8")
    changed += 1
print("уроков перенумеровано:", changed)

# data/program.yaml: num идёт строкой сразу после id; сопоставляем по id
yaml_path = ROOT / "data" / "program.yaml"
yaml_text = yaml_path.read_text(encoding="utf-8")
sys.path.insert(0, str(ROOT / "scripts"))
from gen_program import COURSES  # noqa: E402

for num, folder, *_ in COURSES:
    pass  # COURSES уже в новом порядке, но со старыми номерами — правим ниже файл генератора

# переписываем num в yaml по порядку следования курсов
blocks = yaml_text.split("\n")
new_order = [c[0] for c in COURSES]
idx = 0
for i, line in enumerate(blocks):
    if line.strip().startswith("- id:"):
        if idx < len(new_order):
            target = MAP[new_order[idx]]
            for j in range(i, min(i + 5, len(blocks))):
                if blocks[j].strip().startswith("num:"):
                    blocks[j] = f"    num: {target}"
                    break
        idx += 1
yaml_path.write_text("\n".join(blocks), encoding="utf-8")
print("модулей в program.yaml:", idx)

# gen_program.py: номера в COURSES
gen = ROOT / "scripts" / "gen_program.py"
g = gen.read_text(encoding="utf-8")
for old, new in MAP.items():
    g = re.sub(rf"(?m)^    \({old}, \"", f"    ({new}, \"", g)
gen.write_text(g, encoding="utf-8")

# PROGRAM.md: «## Курс N.»
prog = ROOT / "PROGRAM.md"
p = prog.read_text(encoding="utf-8")
p = re.sub(r"(?m)^## Курс (\d+)\.",
           lambda m: f"## Курс {MAP.get(int(m.group(1)), int(m.group(1)))}.", p)
prog.write_text(p, encoding="utf-8")
print("готово")
