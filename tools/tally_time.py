"""Tally speaker-note time estimates: required / standard / full."""
import re, sys
from collections import defaultdict

text = open(sys.argv[1], encoding="utf-8").read()
verbose = "-v" in sys.argv
# strip front matter
if text.startswith("---"):
    text = text.split("\n---\n", 1)[1]
# split slides on lines that are exactly --- outside fences
slides, cur, fence = [], [], False
for line in text.splitlines():
    if line.strip().startswith("```"):
        fence = not fence
    if line.strip() == "---" and not fence:
        slides.append("\n".join(cur)); cur = []
    else:
        cur.append(line)
slides.append("\n".join(cur))

chapter = 0
fizz = False
tot = defaultdict(float)
per_ch = defaultdict(lambda: defaultdict(float))
for i, s in enumerate(slides, 1):
    m = re.search(r"<!-- _class: ([^>]*?) -->", s)
    cls = m.group(1).split() if m else []
    cm = re.search(r'<span class="num">(\d+)</span>', s)
    if cm:
        chapter = int(cm.group(1)); fizz = False
    if "FizzBuzz を関数だけで" in s:
        fizz = True
    notes = re.findall(r"<!--(?! _)(.*?)-->", s, re.S)
    t = None; nchars = 0
    for n in notes:
        mm = re.search(r"目安 ([\d.]+) 分", n)
        if mm:
            t = float(mm.group(1)); nchars = len(re.sub(r"\s", "", n))
    if t is None:
        print("NO TIME slide", i); continue
    opt = "optional" in cls
    if not opt:
        cat = "req"
    elif chapter in (2, 3, 4, 5, 6) or (chapter == 7 and not fizz):
        cat = "std"
    else:
        cat = "full"
    tot[cat] += t
    per_ch[chapter][cat] += t
    if verbose:
        title = (re.search(r"^#+ (.*)$", s, re.M) or [None, "?"])[1]
        flag = " !" if nchars / 300 > t + 0.26 else ""
        print(f"{i:3d} ch{chapter} {cat:4s} {t:5.2f} {nchars:4d}字{flag} {title[:40]}")
print("slides:", len(slides))
for ch in sorted(per_ch):
    d = per_ch[ch]
    print(f"ch{ch}: req {d['req']:.2f} std+ {d['std']:.2f} full+ {d['full']:.2f}")
r = tot["req"]; s = r + tot["std"]; f = s + tot["full"]
print(f"必須 {r:.2f} / 標準 {s:.2f} / 全部入り {f:.2f}")
