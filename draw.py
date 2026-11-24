#!/usr/bin/env python3
"""news-23 b57 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"

def serif(bold=True, size=20):
    return ImageFont.truetype(f"{FD}/DejaVuSerif-{'Bold' if bold else 'Book'}.ttf", size)
def sans(bold=False, size=12):
    return ImageFont.truetype(f"{FD}/DejaVuSans{'-Bold' if bold else ''}.ttf", size)
def sansb(size=12):
    return sans(True, size)

BLACK = (0, 0, 0); WHITE = (255, 255, 255); GOLD = (212, 175, 55)
RED = (178, 34, 34); DARKRED = (139, 0, 0); TEAL = (0, 128, 128)
NAVY = (16, 32, 64); CREAM = (250, 244, 224); GREY = (90, 90, 90)
LGREY = (230, 230, 230); GREEN = (140, 198, 140); DARKGREEN = (60, 140, 60)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=BLACK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words = s.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, right=None):
    """Draw REPORTED/CLAIM chip; x is left edge unless right given."""
    f = sansb(10)
    w = int(d.textlength(label, font=f)) + 12
    h = 14
    if right is not None:
        x = right - w
    col = (30, 90, 160) if label == "REPORTED" else (178, 34, 34)
    d.rectangle([x, y, x + w, y + h], fill=col)
    d.text((x + 6, y + 2), label, font=f, fill=WHITE)
    return x + w

# ---------- MASTHEAD ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
text(12, 6, "THE WORLD TODAY", serif(True, 40), WHITE)
text(W - 12, 16, "MONDAY 23 NOVEMBER 2026", sansb(16), GOLD, anchor="ra")

# ---------- KICKER ----------
text(12, 60, "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
     sansb(12), RED)

# ---------- NUMBER STRIP (2 rows x 5) ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", (30, 90, 160)),
    ("11,762", "EBOLA CASES, DRC", (0, 110, 60)), ("10T won", "SEOUL STABILISATION FUND", (150, 110, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", (110, 40, 140)),
    ("$450M", "SKUBAL DEAL", (110, 40, 140)), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", (30, 90, 160)), ("264 kg", "EXPLOSIVES IN LEBANON", (150, 110, 0)),
    ("$107.3B", "ANTHROPIC IPO", (110, 40, 140)),
]
colw = (W - 24) // 5
for i, (v, lab, col) in enumerate(nums):
    r, c = divmod(i, 5)
    x = 12 + c * colw
    y = 78 + r * 30
    text(x, y, v, sansb(18), col)
    text(x, y + 20, lab, sans(9), BLACK)
d.line([0, 148, W, 148], fill=BLACK, width=1)

# ---------- REGION BAR ----------
regions = [("ASIA-PACIFIC 7", (0, 128, 128), 200), ("AMERICAS 8", (30, 90, 160), 200),
           ("MIDDLE EAST 6", (180, 140, 0), 200), ("EUROPE 5", (110, 40, 140), 150),
           ("AFRICA 3", (178, 34, 34), 140), ("WORLD 2", (90, 90, 90), 134)]
x = 0
for name, col, w in regions:
    d.rectangle([x, 149, x + w, 168], fill=col)
    text(x + 8, 153, name, sansb(11), WHITE)
    x += w
# UTC strip
text(8, 171, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     sans(10), BLACK)
text(W - 8, 171, "~ APPROX", sans(9), GREY, anchor="ra")

# ---------- HERO SCENES ----------
HX = [8, 352, 696]; HW = [332, 332, 320]; HY = 186; HH = 132
# Scene 1: Kospi chart
d.rectangle([HX[0], HY, HX[0] + HW[0], HY + HH], fill=NAVY)
pts = [(HX[0] + 12 + i * 30, HY + 78 - v) for i, v in enumerate([8, 28, 14, 42, 26, 52, 34, 58, 44, 66, 52])]
for i in range(len(pts) - 1):
    d.line([pts[i], pts[i + 1]], fill=(255, 170, 60), width=3)
for (px, py) in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 100))
for i, bh in enumerate([34, 52, 28, 62, 40, 70, 48, 76, 56, 82]):
    bx = HX[0] + 12 + i * 31
    top = HY + HH - 34 - bh
    d.rectangle([bx, top, bx + 22, HY + HH - 34], fill=(30, 50, 95))
    for wy in range(2, bh - 6, 12):
        for wx in (5, 13):
            d.rectangle([bx + wx, top + wy, bx + wx + 3, top + wy + 4], fill=(255, 220, 120))
text(HX[0] + 10, HY + 6, "-3.3%", sansb(30), (255, 80, 60))
# Scene 2: Guterres
d.rectangle([HX[1], HY, HX[1] + HW[1], HY + HH], fill=TEAL)
text(HX[1] + 12, HY + 10, "150 DELEGATES", sansb(26), GOLD)
text(HX[1] + 12, HY + 40, "BACK A RISK", sansb(26), GOLD)
text(HX[1] + 12, HY + 70, "FRAMEWORK", sansb(26), GOLD)
cx, cy, r = HX[1] + HW[1] - 52, HY + HH - 42, 34
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=1)
d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=1)
d.line([cx, cy - r, cx, cy + r], fill=WHITE, width=1)
# Scene 3: Power index bars
d.rectangle([HX[2], HY, HX[2] + HW[2], HY + HH], fill=CREAM)
text(HX[2] + 10, HY + 4, "NARROWEST SINCE 2018", sansb(12), BLACK)
text(HX[2] + HW[2] - 10, HY + 4, "GAP 5.3", sansb(12), (150, 110, 0), anchor="ra")
bars = [("78.9", "US", NAVY, 70), ("73.6", "CHINA", (178, 34, 34), 64), ("40.5", "INDIA", (200, 160, 40), 38)]
for i, (val, lab, col, bh) in enumerate(bars):
    bx = HX[2] + 22 + i * 102
    by = HY + HH - 10 - bh
    text(bx + 29, by - 18, val, sansb(15), BLACK, anchor="ma")
    d.rectangle([bx, by, bx + 58, HY + HH - 10], fill=col)
    text(bx + 29, by + bh - 15, lab, sansb(11), WHITE, anchor="ma")
# Caption strips under scenes
caps = ["KOSPI 4,708.54   ·   -161 PTS", "UN  ·  BRIDGETOWN", "ASIA POWER INDEX 2026"]
for i in range(3):
    d.rectangle([HX[i], HY + HH, HX[i] + HW[i], HY + HH + 18], fill=BLACK)
    text(HX[i] + 8, HY + HH + 3, caps[i], sansb(10), WHITE)

# ---------- HERO TEXT ----------
HTY = HY + HH + 18 + 6  # 342
heroes = [
    ("1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS"),
    ("3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (num, head, body, src) in enumerate(heroes):
    x = HX[i]; w = HW[i]
    d.ellipse([x, HTY, x + 22, HTY + 22], fill=RED)
    text(x + 11, HTY + 3, num, sansb(13), WHITE, anchor="ma")
    hl = wrap(head, serif(True, 19), w - 30)
    for j, ln in enumerate(hl[:2]):
        text(x + 28, HTY + j * 22, ln, serif(True, 19), BLACK)
    by = HTY + 46
    bl = wrap(body, sans(False, 11), w - 6)
    for j, ln in enumerate(bl[:2]):
        text(x, by + j * 14, ln, sans(False, 11), BLACK)
    sy = HTY + 78
    text(x, sy, src, sans(9), GREY)
    chip(x, sy - 1, "REPORTED", right=x + w - 2)

# ---------- MORE OF THE DAY BAR ----------
MBY = 446
d.rectangle([0, MBY, W, MBY + 18], fill=BLACK)
text(8, MBY + 3, "MORE OF THE DAY  —  10 STORIES", sansb(12), WHITE)

# ---------- CARDS ----------
cards = [
    ("AMERICAS", "1", "BESSENT: NVIDIA ANSWERS", "Treasury chief wants answers.", "Reuters", "REPORTED"),
    ("FBI", "2", "FBI PROBES NCIC HACK", "Hackers hit NCIC database.", "AP", "REPORTED"),
    ("WHITE HOUSE", "3", "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", "4", "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", "5", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", "6", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", "7", "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED"),
    ("TECH", "8", "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", "9", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", "10", "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM"),
]
regcol = {"AMERICAS": (30, 90, 160), "FBI": (178, 34, 34), "WHITE HOUSE": (180, 140, 0),
          "MARKETS": (30, 90, 160), "SPORT": (178, 34, 34), "LEGAL": (110, 40, 140),
          "TECH": (30, 90, 160), "EUROPE": (110, 40, 140), "SPACE": (90, 90, 90)}
cw = 200; gap = 4
CY0 = MBY + 18
for i, (reg, num, head, body, src, cl) in enumerate(cards):
    r, c = divmod(i, 5)
    x = 8 + c * (cw + gap)
    y = CY0 + r * 72
    d.rectangle([x, y, x + cw, y + 14], fill=regcol[reg])
    text(x + 4, y + 2, reg, sansb(9), WHITE)
    text(x + cw - 4, y + 1, num, sansb(11), WHITE, anchor="ra")
    hl = wrap(head, sansb(12), cw - 4)
    for j, ln in enumerate(hl[:2]):
        text(x + 2, y + 15 + j * 13, ln, sansb(12), BLACK)
    text(x + 2, y + 44, body, sans(False, 10), BLACK)
    sy = y + 59
    text(x + 2, sy, src, sans(9), GREY)
    chip(x, sy - 1, cl, right=x + cw - 2)

# ---------- MAP + ALSO ----------
MY = CY0 + 144 + 6  # 614
d.rectangle([0, MY - 2, W, MY + 16], fill=BLACK)
text(8, MY + 1, "WHERE IT HAPPENED", sansb(12), WHITE)
text(318, MY + 1, "ALSO ON MONDAY", sansb(12), WHITE)
MAPY = MY + 18
# map blobs
d.rectangle([8, MAPY, 310, MAPY + 218], fill=(245, 245, 245), outline=(200, 200, 200))
d.ellipse([20, MAPY + 20, 150, MAPY + 150], fill=GREEN)
d.ellipse([150, MAPY + 10, 290, MAPY + 130], fill=GREEN)
d.ellipse([60, MAPY + 150, 180, MAPY + 210], fill=GREEN)
d.ellipse([210, MAPY + 160, 290, MAPY + 205], fill=GREEN)
pins = [(44, 40), (88, 158), (238, 22), (30, 92), (78, 66), (168, 118),
        (26, 66), (30, 128), (58, 148), (112, 160), (176, 44), (196, 82), (212, 34)]
for i, (px, py) in enumerate(pins, 1):
    X, Y = 8 + px, MAPY + py
    d.ellipse([X - 8, Y - 8, X + 8, Y + 8], fill=RED, outline=WHITE, width=1)
    text(X, Y - 5, str(i), sansb(9), WHITE, anchor="ma")
text(12, MAPY + 186, "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing", sans(9), BLACK)
text(12, MAPY + 197, "4 Washington · 5 New York · 6 Tehran · 7 Chicago", sans(9), BLACK)
text(12, MAPY + 208, "8 SF · 9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow", sans(9), BLACK)
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
for i, a in enumerate(also):
    col = i % 2
    x = 322 + col * 350
    y = MAPY + 6 + (i // 2) * 23
    text(x, y, a, sans(False, 11), BLACK)

# ---------- DATE CHECK ----------
DY = MAPY + 224  # ~856
d.rectangle([8, DY, W - 8, DY + 74], outline=RED, width=2)
text(12, DY + 4, "DATE CHECK", sansb(12), RED)
text(W - 12, DY + 4, "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", sansb(9), RED, anchor="ra")
text(12, DY + 22, "LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
     sans(False, 10), BLACK)
text(12, DY + 36, "EU-Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
     sans(False, 10), BLACK)
text(12, DY + 54, "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
     sans(False, 10), BLACK)

# ---------- FOOTER ----------
FY = DY + 80
text(8, FY, "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
     sans(False, 9), GREY)
text(8, FY + 12, "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing.",
     sans(False, 9), GREY)
text(8, FY + 24, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     sans(False, 9), GREY)
d.rectangle([0, H - 34, W, H], fill=BLACK)
text(W // 2, H - 28, "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions",
     sansb(13), GOLD, anchor="ma")

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
