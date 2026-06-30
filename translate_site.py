#!/usr/bin/env python3
"""Extract Persian strings, translate to English, apply LTR structure."""
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).parent
PERSIAN_RE = re.compile(
    r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF][^\n<]*"
)

STRUCTURAL = [
    (r'<html\s+dir="rtl"\s+lang="fa">', '<html lang="en" dir="ltr">'),
    (r'<html\s+lang="fa"\s+dir="rtl">', '<html lang="en" dir="ltr">'),
    (r'<html lang="en">', '<html lang="en" dir="ltr">'),
    ("css/bootstrap-rtl.min.css", "css/bootstrap.min.css"),
    ("navbar-nav mr-auto", "navbar-nav ms-auto"),
    ('alt="لوگو"', 'alt="GrainGuys logo"'),
    ("Movein - ", "GrainGuys - "),
    ("MoveIn", "GrainGuys"),
    (' dir="ltr"', ""),
]

REMOVE_LINES = [
    "jalalidatepicker@0.9.12.min.css",
    "jalalidatepicker@0.9.12.min.js",
    "<!-- Jalalidatepicker Css File -->",
    "<!-- Jalalidatepicker js file -->",
]

GOOGLE_FONTS = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
)

BRAND_OVERRIDES = {
    "خیابان آزادی، کوچه6": "123 Main Street, Suite 100",
    "کپی رایت©1404 کلیه حقوق محفوظ است .": "Copyright © 2026 All Rights Reserved.",
}


def extract_strings() -> list[str]:
    strings: set[str] = set()
    for pattern in ("*.html",):
        for path in ROOT.glob(pattern):
            for match in PERSIAN_RE.findall(path.read_text(encoding="utf-8")):
                s = match.strip()
                if s and len(s) < 300:
                    strings.add(s)
    for name in ("form-process.php", "form-appointment.php"):
        path = ROOT / name
        if path.exists():
            for match in PERSIAN_RE.findall(path.read_text(encoding="utf-8")):
                s = match.strip()
                if s:
                    strings.add(s)
    return sorted(strings, key=len, reverse=True)


def translate_strings(strings: list[str]) -> dict[str, str]:
    from deep_translator import GoogleTranslator

    translator = GoogleTranslator(source="fa", target="en")
    out: dict[str, str] = dict(BRAND_OVERRIDES)

    for i, s in enumerate(strings):
        if s in out:
            continue
        try:
            text = translator.translate(s)
            text = text.replace("MoveIn", "GrainGuys").replace("Movein", "GrainGuys")
            out[s] = text
        except Exception as exc:
            print(f"  skip [{i}]: {exc}")
            out[s] = s
        if i % 25 == 0:
            print(f"  translated {i + 1}/{len(strings)}")
            time.sleep(0.3)

    return out


def apply_structural(text: str) -> str:
    for old, new in STRUCTURAL:
        text = re.sub(old, new, text) if old.startswith("<html") else text.replace(old, new)
    lines = [ln for ln in text.splitlines(True) if not any(r in ln for r in REMOVE_LINES)]
    text = "".join(lines)
    if "fonts.googleapis.com" not in text and "<!-- Main Custom Css -->" in text:
        text = text.replace(
            "    <!-- Main Custom Css -->\n", GOOGLE_FONTS + "    <!-- Main Custom Css -->\n"
        )
    return text


def apply_translations(text: str, translations: dict[str, str]) -> str:
    for fa in sorted(translations.keys(), key=len, reverse=True):
        text = text.replace(fa, translations[fa])
    return text


def process_file(path: Path, translations: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = apply_structural(text)
    text = apply_translations(text, translations)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    strings = extract_strings()
    print(f"Found {len(strings)} Persian strings")

    translations_path = ROOT / "translations.json"
    if strings:
        translations = translate_strings(strings)
        translations_path.write_text(
            json.dumps(translations, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Wrote {len(translations)} entries to translations.json")
    elif translations_path.exists():
        translations = json.loads(translations_path.read_text(encoding="utf-8"))
        print(f"Loaded {len(translations)} entries from translations.json")
    else:
        translations = {}
        print("No Persian strings and no translations.json — applying structure only")

    targets = sorted(ROOT.glob("*.html"))
    for name in ("form-process.php", "form-appointment.php"):
        p = ROOT / name
        if p.exists():
            targets.append(p)

    for path in targets:
        process_file(path, translations)
        print(f"Updated {path.name}")

    remaining = sum(
        len(PERSIAN_RE.findall(p.read_text(encoding="utf-8"))) for p in ROOT.glob("*.html")
    )
    print(f"Done. Remaining Persian matches in HTML: {remaining}")


if __name__ == "__main__":
    main()
