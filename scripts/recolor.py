"""Перекраска сайта из биологической палитры в «заводскую».

Зелёный акцент «Биологии AI» заменяется на предохранительный оранжевый,
светлые зелёные подложки — на тёплые песочные.

    python scripts/recolor.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parent.parent

MAP = {
    "16a34a": "c2410c",   # основной акцент: зелёный → оранжевый
    "166534": "7c2d12",   # тёмный текст акцента
    "f0fdf4": "fff7ed",   # светлая подложка
    "86efac": "fdba74",   # рамка
    "bbf7d0": "fed7aa",   # заливка
    "dcfce7": "ffedd5",   # фон бейджа
    "0f766e": "9a3412",   # второй акцент в градиенте
    "22c55e": "ea580c",   # яркий зелёный → яркий оранжевый
}

pattern = re.compile(r"#(" + "|".join(MAP) + r")\b", re.IGNORECASE)

changed = 0
for folder, exts in (("layouts", ("*.html",)), ("static", ("*.svg",))):
    for ext in exts:
        for f in (ROOT / folder).rglob(ext):
            text = f.read_text(encoding="utf-8")
            new = pattern.sub(lambda m: "#" + MAP[m.group(1).lower()], text)
            if new != text:
                f.write_text(new, encoding="utf-8")
                changed += 1

print("файлов перекрашено:", changed)
