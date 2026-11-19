"""Добавляет в frontmatter каждого урока поля для навигации по модулям:
    course:        название курса
    course_num:    номер модуля
    lesson_in_course / course_total: «урок 5 из 12»

Нужно, чтобы в уроке было видно «Модуль 12 · Электрика · урок 5 из 12», а не сквозной номер 205.
Запуск из корня:  python scripts/add_course_fields.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen_program import COURSES, parse  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

parsed = parse()
changed = 0

for num, folder, title, _sub, _color, _emoji in COURSES:
    secs = parsed.get(num, [])
    lessons = [no for s in secs for no, _ in s["lessons"]]
    total = len(lessons)
    for idx, no in enumerate(lessons, start=1):
        files = list((ROOT / "content" / folder).glob(f"{no:03d}-*.md"))
        if not files:
            print(f"  нет файла для урока {no} ({folder})")
            continue
        f = files[0]
        text = f.read_text(encoding="utf-8")
        if "course_num:" in text:
            continue
        head, sep, body = text.partition("\n---\n")
        if not sep:
            print(f"  нет frontmatter: {f.name}")
            continue
        block = (
            f'\ncourse: "{title}"'
            f"\ncourse_num: {num}"
            f"\nlesson_in_course: {idx}"
            f"\ncourse_total: {total}"
        )
        f.write_text(head + block + sep + body, encoding="utf-8")
        changed += 1

print("уроков обновлено:", changed)
