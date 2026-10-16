"""Generate theme/quiet-webfonts.css from Google Fonts (Noto Sans Mono / JP).

The theme prefers locally installed Noto fonts. For viewers without them,
this file declares web fallbacks under separate family names, so they never
shadow the local fonts (Google's Noto Sans Mono, for one, lacks box drawing):

- "Quiet Web Mono": Noto Sans Mono, placed after the local one in --font-code.
- "Quiet Code CJK": web sources for the code alias that aligns Japanese to
  exactly two columns (size-adjust: 120%). It reuses the woff2 subsets of
  Noto Sans JP, which the body font loads anyway, and keeps only CJK ranges
  like the local() faces in quiet.css.

    python tools/gen_webfonts.py   # or: make webfonts
"""

from pathlib import Path
import re
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "theme" / "quiet-webfonts.css"
API = "https://fonts.googleapis.com/css2?family={}:wght@400;700&display=swap"
# Google Fonts returns woff2 with unicode-range subsets only to modern UAs.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
FACE = re.compile(r"@font-face\s*{(.*?)}", re.S)
# Same ranges as the local() faces of "Quiet Code CJK" in quiet.css.
CJK = [(0x3000, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF),
       (0xF900, 0xFAFF), (0xFF01, 0xFF60), (0xFFE0, 0xFFE6)]


def descriptor(body, name):
    match = re.search(rf"{name}:\s*([^;]+);", body)
    return match[1].strip() if match else None


def cjk_only(unicode_range):
    """Intersect a unicode-range value with CJK; None if nothing is left."""
    kept = []
    for part in unicode_range.split(","):
        first, _, last = part.strip().removeprefix("U+").partition("-")
        lo, hi = int(first, 16), int(last or first, 16)
        for cjk_lo, cjk_hi in CJK:
            a, b = max(lo, cjk_lo), min(hi, cjk_hi)
            if a == b:
                kept.append(f"U+{a:X}")
            elif a < b:
                kept.append(f"U+{a:X}-{b:X}")
    return ", ".join(kept) or None


def google_faces(family):
    """Return {woff2 url: unicode-range}; both weights share one variable file."""
    url = API.format(family.replace(" ", "+"))
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    css = urllib.request.urlopen(request, timeout=30).read().decode()
    faces = {}
    for body in FACE.findall(css):
        src = re.search(r"url\(([^)]+)\)", descriptor(body, "src"))[1]
        faces.setdefault(src, descriptor(body, "unicode-range"))
    if not faces:
        raise SystemExit(f"no @font-face rules for {family}")
    return faces


def rule(family, src, unicode_range, extra=""):
    return ("@font-face {\n"
            f'  font-family: "{family}";\n'
            f'  src: url({src}) format("woff2");\n'
            "  font-weight: 400 700;\n"
            "  font-display: swap;\n"
            f"{extra}"
            f"  unicode-range: {unicode_range};\n"
            "}")


def main():
    mono = [rule("Quiet Web Mono", src, unicode_range)
            for src, unicode_range in google_faces("Noto Sans Mono").items()]
    cjk = [rule("Quiet Code CJK", src, kept, "  size-adjust: 120%;\n")
           for src, unicode_range in google_faces("Noto Sans JP").items()
           if (kept := cjk_only(unicode_range))]
    OUT.write_text(
        "/* @theme quiet-webfonts */\n"
        "/* tools/gen_webfonts.py が生成。手で編集しない。 */\n"
        "/* Noto 未インストールの閲覧環境向けの Web フォント（quiet.css から読み込む）。 */\n\n"
        + "\n".join(mono + cjk) + "\n",
        encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: Quiet Web Mono {len(mono)} faces, "
          f"Quiet Code CJK {len(cjk)} faces")


if __name__ == "__main__":
    main()
