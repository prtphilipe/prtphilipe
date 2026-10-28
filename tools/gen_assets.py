import os, random, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# ---------- palette ----------
BG = "#0a0c0c"
TILE, TILE_D = "#141818", "#1b2021"
OUTL, DARK, MID, LIGHT = "#111515", "#2c3435", "#4b5657", "#6e7b7a"
MOSS, MOSS_L, VINE = "#4f6b2e", "#7a9a3e", "#35502a"
GOLD, GOLD_D = "#e0b85a", "#4a3410"
STONE_TXT = "#b8c4c2"

# ---------- 5x7 pixel font ----------
F = {
 'A':".###.|#...#|#...#|#####|#...#|#...#|#...#", 'B':"####.|#...#|#...#|####.|#...#|#...#|####.",
 'C':".###.|#...#|#....|#....|#....|#...#|.###.", 'D':"####.|#...#|#...#|#...#|#...#|#...#|####.",
 'E':"#####|#....|#....|####.|#....|#....|#####", 'F':"#####|#....|#....|####.|#....|#....|#....",
 'G':".###.|#...#|#....|#.###|#...#|#...#|.####", 'H':"#...#|#...#|#...#|#####|#...#|#...#|#...#",
 'I':".###.|..#..|..#..|..#..|..#..|..#..|.###.", 'J':"..###|...#.|...#.|...#.|...#.|#..#.|.##..",
 'K':"#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#", 'L':"#....|#....|#....|#....|#....|#....|#####",
 'M':"#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#", 'N':"#...#|#...#|##..#|#.#.#|#..##|#...#|#...#",
 'O':".###.|#...#|#...#|#...#|#...#|#...#|.###.", 'P':"####.|#...#|#...#|####.|#....|#....|#....",
 'Q':".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#", 'R':"####.|#...#|#...#|####.|#.#..|#..#.|#...#",
 'S':".####|#....|#....|.###.|....#|....#|####.", 'T':"#####|..#..|..#..|..#..|..#..|..#..|..#..",
 'U':"#...#|#...#|#...#|#...#|#...#|#...#|.###.", 'V':"#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
 'W':"#...#|#...#|#...#|#.#.#|#.#.#|#.#.#|.#.#.", 'X':"#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
 'Y':"#...#|#...#|.#.#.|..#..|..#..|..#..|..#..", 'Z':"#####|....#|...#.|..#..|.#...|#....|#####",
 '0':".###.|#...#|#..##|#.#.#|##..#|#...#|.###.", '1':"..#..|.##..|..#..|..#..|..#..|..#..|.###.",
 '2':".###.|#...#|....#|...#.|..#..|.#...|#####", '3':"####.|....#|....#|.###.|....#|....#|####.",
 '4':"...#.|..##.|.#.#.|#..#.|#####|...#.|...#.", '5':"#####|#....|####.|....#|....#|#...#|.###.",
 '6':".###.|#....|#....|####.|#...#|#...#|.###.", '7':"#####|....#|...#.|..#..|.#...|.#...|.#...",
 '8':".###.|#...#|#...#|.###.|#...#|#...#|.###.", '9':".###.|#...#|#...#|.####|....#|....#|.###.",
 '.':".....|.....|.....|.....|.....|.....|..#..", ',':".....|.....|.....|.....|.....|..#..|.#...",
 '!':"..#..|..#..|..#..|..#..|..#..|.....|..#..", '?':".###.|#...#|....#|...#.|..#..|.....|..#..",
 '-':".....|.....|.....|.###.|.....|.....|.....", ':':".....|.....|..#..|.....|.....|..#..|.....",
 '>':".#...|..#..|...#.|....#|...#.|..#..|.#...", '<':"...#.|..#..|.#...|#....|.#...|..#..|...#.",
 '/':"....#|....#|...#.|..#..|.#...|#....|#....", '+':".....|..#..|..#..|#####|..#..|..#..|.....",
 '·':".....|.....|.....|..#..|.....|.....|.....", '&':".##..|#..#.|#.#..|.#...|#.#.#|#..#.|.##.#",
 "'":"..#..|..#..|.....|.....|.....|.....|.....", ' ':".....|.....|.....|.....|.....|.....|.....",
}
MARKS = {'tilde':(-2, ".##.#|#.##."), 'acute':(-2, "...#.|..#.."), 'circ':(-2, "..#..|.#.#."),
         'ced':(7, "..#..|.##..")}
ACC = {'Ã':('A','tilde'),'Õ':('O','tilde'),'Á':('A','acute'),'É':('E','acute'),'Í':('I','acute'),
       'Ó':('O','acute'),'Ú':('U','acute'),'Â':('A','circ'),'Ê':('E','circ'),'Ô':('O','circ'),
       'Ç':('C','ced')}

def glyph_cells(ch):
    mark = None
    if ch in ACC:
        ch, mark = ACC[ch]
    cells = [(x, y) for y, row in enumerate(F[ch].split('|')) for x, c in enumerate(row) if c == '#']
    if mark:
        oy, pat = MARKS[mark]
        cells += [(x, oy + y) for y, row in enumerate(pat.split('|')) for x, c in enumerate(row) if c == '#']
    return cells

def text_cells(s):
    cells, cx = [], 0
    for ch in s.upper():
        cells += [(cx + x, y) for x, y in glyph_cells(ch)]
        cx += 6
    return cells, cx - 1

def text_w(s, sc):
    return text_cells(s)[1] * sc

def cells_path(cells, x0, y0, s):
    return "".join(f"M{x0+x*s} {y0+y*s}h{s}v{s}h-{s}z" for x, y in cells)

def ptext(s, x, y, sc, fill, shadow=None, cls=""):
    cells, _ = text_cells(s)
    out = ""
    if shadow:
        out += f'<path fill="{shadow}" d="{cells_path(cells, x+sc, y+sc, sc)}"/>'
    c = f' class="{cls}"' if cls else ""
    return out + f'<path{c} fill="{fill}" d="{cells_path(cells, x, y, sc)}"/>'

def ptext_c(s, cx, y, sc, fill, shadow=None):
    return ptext(s, round(cx - text_w(s, sc) / 2), y, sc, fill, shadow)

def sprite(rows, colors, x0, y0, s):
    paths = {}
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != '.':
                paths.setdefault(c, []).append(f"M{x0+x*s} {y0+y*s}h{s}v{s}h-{s}z")
    return "".join(f'<path fill="{colors[c]}" d="{"".join(p)}"/>' for c, p in paths.items())

def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'

# ---------- carved stone block ----------
def block(x, y, s, v=0, eye=None, pal=None):
    OUTL, DARK, MID, LIGHT = pal or (globals()['OUTL'], globals()['DARK'], globals()['MID'], globals()['LIGHT'])
    u = max(1, s // 8)
    o = max(1, s // 16)
    fx, fy, fw = x + o + u, y + o + u, s - 2 * o - 2 * u
    r = rect(x, y, s, s, OUTL) + rect(x+o, y+o, s-2*o, s-2*o, DARK) \
        + rect(x+o, y+o, s-2*o-u, s-2*o-u, LIGHT) + rect(fx, fy, fw, fw, MID)
    if v == 1:    # carved square
        r += rect(fx+u, fy+u, fw-2*u, fw-2*u, DARK) + rect(fx+2*u, fy+2*u, max(u, fw-4*u), max(u, fw-4*u), MID)
    elif v == 2:  # grooves
        r += rect(fx+u, fy+u, fw-2*u, u, DARK) + rect(fx+u, fy+fw-2*u, fw-2*u, u, DARK)
    elif v == 3:  # skull face
        e = eye or DARK
        cls = ' class="eye"' if eye else ""
        r += rect(fx+u, fy+u, u, u, e, cls) + rect(fx+fw-2*u, fy+u, u, u, e, cls)
        r += rect(fx+u, fy+fw-2*u, fw-2*u, max(1, u//2), DARK)
    elif v == 4:  # glyph hook
        r += rect(fx+u, fy+u, fw-2*u, u, DARK) + rect(fx+fw-2*u, fy+u, u, fw-2*u, DARK) \
             + rect(fx+u, fy+fw-2*u, fw-2*u, u, DARK) + rect(fx+u, fy+fw//2, u, fw//2-u, DARK)
    elif v == 5:  # crack
        r += rect(fx+u, fy, u, u, DARK) + rect(fx+2*u, fy+u, u, u, DARK) + rect(fx+2*u, fy+2*u, u, u, DARK)
    return r

def bg_tiles(w, h, rng, step=30, p=0.45):
    out = [rect(0, 0, w, h, BG)]
    for gy in range(0, h, step):
        for gx in range(0, w, step):
            if rng.random() < p:
                t = step - 4
                out.append(rect(gx+2, gy+2, t, t, TILE))
                k = rng.randrange(4)
                if k == 0:
                    out.append(rect(gx+8, gy+8, t-12, t-12, TILE_D) + rect(gx+12, gy+12, t-20, t-20, TILE))
                elif k == 1:
                    out.append(rect(gx+7, gy+9, 6, 6, TILE_D) + rect(gx+t-9, gy+9, 6, 6, TILE_D))
                elif k == 2:
                    out.append(rect(gx+6, gy+8, t-8, 3, TILE_D) + rect(gx+6, gy+t-8, t-8, 3, TILE_D))
    return "".join(out)

def moss_on(x, y, w, rng):
    out = ""
    n = rng.randint(1, 3)
    for _ in range(n):
        mx = x + rng.randrange(0, max(1, w - 6))
        mw = rng.randint(4, 8)
        out += rect(mx, y - 2, mw, 2, MOSS) + rect(mx + rng.randrange(mw), y - 4, 2, 2, MOSS_L)
    return out

def vine(x, y, length, rng):
    out = rect(x, y, 2, length, VINE)
    for ly in range(y + 4, y + length, 6):
        out += rect(x + (2 if rng.random() < .5 else -2), ly, 2, 2, MOSS)
    return out

def flame(x, y, s):
    c = {'r': "#c0392b", 'o': "#f08a24", 'y': "#ffd23f", 'w': "#fff3b0"}
    f1 = ["...r...", "..ror..", "..ror..", ".roor..", ".royor.", "rroyorr", "royywor", "royywor", ".rooor."]
    f2 = ["....r..", "...or..", "..ror..", "..roor.", ".royor.", "rroyyor", "roywyor", "royywor", ".rooor."]
    return f'<g class="f1">{sprite(f1, c, x, y, s)}</g><g class="f2">{sprite(f2, c, x, y, s)}</g>'

def embers(cx, y, rng, n=5, spread=24):
    out = ""
    for _ in range(n):
        ex = cx + rng.randint(-spread // 2, spread // 2)
        d = rng.uniform(0, 2.4)
        out += rect(ex, y, 3, 3, rng.choice(["#f08a24", "#ffd23f", "#e0502e"]),
                    f' class="em" style="animation-delay:{d:.2f}s"')
    return out

def torch(cx, base_y, rng):
    out = ""
    for i in range(2):
        out += block(cx - 10, base_y - 20 * (i + 1), 20, 2 if i else 1)
    by = base_y - 50
    out += rect(cx - 18, by, 36, 10, OUTL) + rect(cx - 16, by + 2, 32, 6, "#3a2a18") + rect(cx - 16, by, 32, 2, GOLD)
    out += flame(cx - 14, by - 36, 4)
    out += embers(cx, by - 36, rng)
    return out

CSS = """<style>
.f1{animation:fa .5s steps(1) infinite}.f2{animation:fb .5s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.glow{animation:gl 1.3s ease-in-out infinite alternate}@keyframes gl{from{opacity:.45}to{opacity:.85}}
.em{animation:rise 2.4s linear infinite;opacity:0}
@keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(-70px);opacity:0}}
.eye{animation:eye 3s ease-in-out infinite}@keyframes eye{0%,60%,100%{fill:#2c3435}75%{fill:#ff3b2f}}
.bob{animation:bob 1s steps(1) infinite}@keyframes bob{0%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.wave{animation:wave 2s steps(8) infinite}@keyframes wave{from{transform:translateX(0)}to{transform:translateX(-32px)}}
.bub{animation:bub 2.8s ease-in infinite;opacity:0}
@keyframes bub{0%{transform:translateY(0);opacity:0}20%{opacity:1}90%{opacity:1}100%{transform:translateY(-34px);opacity:0}}
</style>"""

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges" role="img"><title>{title}</title>'
            f'<defs><radialGradient id="g"><stop offset="0" stop-color="#f08a24" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="#f08a24" stop-opacity="0"/></radialGradient></defs>'
            f'{CSS}{body}</svg>')

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)

# ================= HEADER =================
def header():
    W, H = 900, 360
    rng = random.Random(7)
    b = [bg_tiles(W, H, rng)]
    b.append(f'<ellipse class="glow" cx="70" cy="230" rx="120" ry="110" fill="url(#g)"/>')
    b.append(f'<ellipse class="glow" cx="830" cy="230" rx="120" ry="110" fill="url(#g)"/>')
    # ceiling
    for i, x in enumerate(range(0, W, 24)):
        v = 3 if i in (9, 28) else rng.choice([0, 1, 2, 4, 0, 5])
        b.append(block(x, 0, 24, v, eye=DARK if v == 3 else None))
        if rng.random() < .25:
            b.append(block(x, 24, 24, rng.choice([1, 2, 4])))
            if rng.random() < .6:
                b.append(vine(x + rng.randint(4, 18), 48, rng.randint(12, 40), rng))
        elif rng.random() < .3:
            b.append(vine(x + rng.randint(4, 18), 24, rng.randint(10, 46), rng))
    # title made of stone blocks
    s = 18
    cells, wcols = text_cells("PHILIPE")
    cs = set(cells)
    tx, ty = (W - wcols * s) // 2, 72
    b.append(rect(tx - 12, ty - 8, wcols * s + 24, 7 * s + 16, BG, ' opacity=".7"'))
    b.append(f'<path fill="#000" d="{cells_path(cells, tx + 5, ty + 5, s)}"/>')
    tpal = ("#111515", "#3d4748", "#7d8a88", "#aab6b3")
    for (cx, cy) in cells:
        x, y = tx + cx * s, ty + cy * s
        b.append(block(x, y, s, rng.choice([0, 0, 1, 2, 4, 5]), pal=tpal))
    for (cx, cy) in cells:
        x, y = tx + cx * s, ty + cy * s
        if (cx, cy - 1) not in cs and rng.random() < .45:
            b.append(moss_on(x, y, s, rng))
        if (cx, cy + 1) not in cs and rng.random() < .12:
            b.append(vine(x + rng.randint(3, 11), y + s, rng.randint(8, 22), rng))
    b.append(ptext_c("ENGENHEIRO DA COMPUTAÇÃO", W / 2, 222, 3, GOLD, GOLD_D))
    b.append(ptext_c("RPA · POWER AUTOMATE · PYTHON · SQL SERVER · DEVOPS", W / 2, 264, 2, STONE_TXT, OUTL))
    # floor
    for row, y in enumerate((300, 330)):
        for x in range(-15 if row else 0, W, 30):
            b.append(block(x, y, 30, rng.choice([0, 1, 2, 4, 5, 0])))
    for x in range(0, W, 30):
        if rng.random() < .5:
            b.append(moss_on(x, 300, 30, rng))
    for sx in (250, 600):  # spikes
        for k in range(5):
            x = sx + k * 10
            b.append(rect(x + 3, 290, 4, 10, "#8a8f86") + rect(x + 4, 286, 2, 4, GOLD) + rect(x + 1, 296, 8, 4, "#5b6058"))
    b.append(torch(70, 300, rng))
    b.append(torch(830, 300, rng))
    save("header.svg", svg(W, H, "".join(b), "PHILIPE - Engenheiro da Computação"))

# ================= SECTION BANNER =================
def banner(name, label):
    W, H = 900, 76
    rng = random.Random(hash(label) & 0xffff)
    tw = text_w(label, 3)
    pw = tw + 64
    px = (W - pw) // 2
    b = [rect(0, 0, W, H, BG)]
    # chain line
    for x in range(0, W, 12):
        if x < px - 30 or x > px + pw + 30:
            b.append(rect(x, 37, 8, 3, "#3a2a18") + rect(x + 1, 37, 6, 1, "#8a5a2b"))
    b.append(rect(px, 14, pw, 50, OUTL) + rect(px + 2, 16, pw - 4, 46, LIGHT) + rect(px + 4, 18, pw - 6, 44, DARK)
             + rect(px + 4, 18, pw - 8, 42, "#1c2223"))
    b.append(ptext(label, px + 32, 29, 3, GOLD, GOLD_D))
    b.append(moss_on(px + 6, 14, pw // 3, rng) + moss_on(px + pw // 2, 14, pw // 3, rng))
    b.append(block(px - 30, 21, 32, 3, eye=DARK) + block(px + pw - 2, 21, 32, 3, eye=DARK))
    b.append(vine(px + pw - 40, 64, 10, rng))
    save(name, svg(W, H, "".join(b), label))

# ================= ABOUT TABLET =================
def about():
    W, H = 900, 300
    rng = random.Random(3)
    b = [rect(0, 0, W, H, BG)]
    b.append(rect(16, 16, W - 32, H - 32, "#151a1b"))
    for gy in range(24, H - 40, 28):
        for gx in range(24, W - 40, 28):
            if rng.random() < .25:
                b.append(rect(gx, gy, 22, 22, "#191f20"))
    for x in range(0, W, 16):
        b.append(block(x, 0, 16, rng.choice([0, 1, 2])) + block(x, H - 16, 16, rng.choice([0, 1, 4])))
    for y in range(16, H - 16, 16):
        b.append(block(0, y, 16, rng.choice([0, 2])) + block(W - 16, y, 16, rng.choice([0, 2])))
    for x in range(0, W, 16):
        if rng.random() < .3:
            b.append(moss_on(x, 0, 16, rng))
        if rng.random() < .12:
            b.append(vine(x + 6, 16, rng.randint(10, 30), rng))
    lines = [("NOME", "PHILIPE"), ("CLASSE", "ENG. DA COMPUTAÇÃO"), ("GUILDA", "RPA & AUTOMAÇÃO"),
             ("BASE", "SÃO PAULO - SP"), ("MISSÃO", "AUTOMATIZAR O REPETITIVO"),
             ("LEMA", "TRUST ME, I'M AN ENGINEER!")]
    y = 48
    for k, v in lines:
        b.append(ptext(">", 44, y, 3, "#e0502e"))
        b.append(ptext(k, 74, y, 3, GOLD, GOLD_D))
        b.append(ptext(v, 74 + 8 * 18, y, 3, STONE_TXT, OUTL))
        y += 36
    # explorer sprite on a pedestal
    rows = ["................", ".....hhhhhh.....", "....hhhhhhhh....", "....HHHHHHHH....",
            "..hhhhhhhhhhhh..", ".....ssssss.....", ".....sdssds.....", ".....ssssss.....",
            "......ssss......", "....gggggggg....", "...sggggGgggs...", "...sgggGGgggs...",
            "....bbbbbbbb....", "....bbb..bbb....", "....bbb..bbb....", "...kkkk..kkkk..."]
    col = {'h': "#8a5a2b", 'H': GOLD, 's': "#e0a878", 'd': "#1a1f20", 'g': "#4f7a3a",
           'G': "#3b5c2b", 'b': "#4a3b2a", 'k': "#2a2016"}
    b.append(f'<g class="bob">{sprite(rows, col, 726, 96, 6)}</g>')
    for i in range(3):
        b.append(block(726 + i * 32, 192, 32, [2, 3, 2][i], eye="#2c3435" if i == 1 else None))
    b.append(block(742, 224, 32, 1) + block(774, 224, 32, 4))
    save("about.svg", svg(W, H, "".join(b), "Ficha do personagem: Philipe, Engenheiro da Computação, RPA e Automação"))

# ================= SKILLS =================
ICONS = {
 "RPA": ([".....gg.....", ".....gg.....", "..gggggggg..", ".gddddddddg.", ".gdccddccdg.", ".gdccddccdg.",
          ".gddddddddg.", ".gddggggddg.", ".gddddddddg.", "..gggggggg..", "...g....g...", "..ggg..ggg.."],
         {'g': GOLD, 'd': "#1a1f20", 'c': "#5fe0d0"}),
 "POWER AUTOMATE": (["............", "BB....BB....", ".BB....BB...", "..BB....BB..", "...bb....bb.", "....bb....bb",
                     "....bb....bb", "...bb....bb.", "..bb....bb..", ".bb....bb...", "bb....bb....", "............"],
                    {'b': "#2f7bff", 'B': "#7fb0ff"}),
 "PYTHON": (["...bbbbb....", "..bebbbbb...", "..bbbbbbb...", ".......bb...", ".bbbbbbbb.yy", "bbbbbbbbb.yy",
             "bb.yyyyyyyyy", "yy.yyyyyyyy.", "...yy.......", "...yyyyyyy..", "...yyyyyey..", "....yyyyy..."],
            {'b': "#3a74b0", 'y': "#f2c94c", 'e': "#ffffff"}),
 "SQL SERVER": (["..RRRRRRRR..", ".RRRRRRRRRR.", "rrRRRRRRRRrr", "rrrrrrrrrrrr", "drrrrrrrrrrd", "rddrrrrrrddr",
                 "rrrddddddrrr", "rrrrrrrrrrrr", "drrrrrrrrrrd", "rddrrrrrrddr", ".rrddddddrr.", "..rrrrrrrr.."],
                {'r': "#c8393b", 'R': "#e86a5c", 'd': "#7a1f22"}),
 "HTML": (["oooooooooooo", "oooooooooooo", ".oowwwwwwOo.", ".oowOOOOOOo.", ".oowOOOOOOo.", ".oowwwwwwOo.",
           ".oooOOOOwOo.", ".oooOOOOwOo.", "..owwwwwwO..", "..ooooOOOO..", "...oooOOO...", ".....oO....."],
          {'o': "#e8622c", 'O': "#f08a50", 'w': "#ffffff"}),
 "CSS": (["cccccccccccc", "cccccccccccc", ".ccwwwwwwCc.", ".ccccccCwCc.", ".ccccwwwwCc.", ".ccccccCwCc.",
          ".ccccccCwCc.", ".ccwwwwwwCc.", "..ccccCCCC..", "..ccccCCCC..", "...cccCCC...", ".....cC....."],
         {'c': "#2d6fd1", 'C': "#5b95e8", 'w': "#ffffff"}),
 "DOCKER": (["............", "......BB....", "...BB.BB....", "BB.BB.BB....", "BB.BB.BB..b.", "bbbbbbbbbbbb",
             "bbbbbbbbbbbb", "bbbdbbbbbbb.", "bbbbbbbbbb..", ".bbbbbbbb...", "..bbbbbb....", "............"],
            {'b': "#2496ed", 'B': "#6cc0f5", 'd': "#0b2a40"}),
 "DEVOPS": (["............", "............", "............", ".ppp....PPP.", "p...p..P...P", "p....pP....P",
             "p....pP....P", "p...p..P...P", ".ppp....PPP.", "............", "............", "............"],
            {'p': "#a07ae8", 'P': "#5fe0d0"}),
}

def skills():
    W, H = 900, 220
    rng = random.Random(11)
    b = [rect(0, 0, W, H, BG)]
    sw, sh, gap = 210, 96, 10
    x0 = (W - (4 * sw + 3 * gap)) // 2
    for i, (name, (rows, col)) in enumerate(ICONS.items()):
        r, c = divmod(i, 4)
        x, y = x0 + c * (sw + gap), 10 + r * (sh + gap)
        b.append(rect(x, y, sw, sh, OUTL) + rect(x + 2, y + 2, sw - 4, sh - 4, LIGHT)
                 + rect(x + 4, y + 4, sw - 6, sh - 6, DARK) + rect(x + 4, y + 4, sw - 8, sh - 8, "#1c2223"))
        # icon socket
        b.append(rect(x + 14, y + 16, 64, 64, OUTL) + rect(x + 16, y + 18, 60, 60, "#0e1112"))
        b.append(sprite(rows, col, x + 22, y + 24, 4))
        words = name.split()
        ty = y + sh // 2 - (len(words) * 22 - 8) // 2
        for wd in words:
            b.append(ptext(wd, x + 92, ty, 2, STONE_TXT, OUTL))
            ty += 22
        b.append(moss_on(x + 8, y, sw - 16, rng))
    save("skills.svg", svg(W, H, "".join(b), "Arsenal: " + ", ".join(ICONS)))

# ================= FOOTER (lava) =================
def footer():
    W, H = 900, 200
    rng = random.Random(5)
    b = [bg_tiles(W, H, rng, p=.35)]
    b.append(ptext_c("VOLTE SEMPRE, EXPLORADOR!", W / 2, 24, 3, GOLD, GOLD_D))
    b.append(f'<ellipse class="glow" cx="450" cy="150" rx="420" ry="70" fill="url(#g)"/>')
    pool_x, pool_w, top = 120, 660, 142
    b.append(rect(pool_x, top, pool_w, H - top, "#a8302a") + rect(pool_x, top + 18, pool_w, H - top, "#c0392b"))
    wave = "".join(rect(pool_x + x, top - 4 + (0 if (x // 16) % 2 else 4), 16, 4, "#e0502e")
                   + rect(pool_x + x + 4, top + (0 if (x // 16) % 2 else 4), 8, 2, "#f08a24")
                   for x in range(0, pool_w + 64, 16))
    b.append(f'<svg x="{pool_x}" y="0" width="{pool_w}" height="{H}" viewBox="{pool_x} 0 {pool_w} {H}">'
             f'<g class="wave">{wave}</g></svg>')
    for _ in range(9):
        bx = pool_x + rng.randint(20, pool_w - 20)
        d = rng.uniform(0, 2.8)
        b.append(rect(bx, top + 4, 6, 6, "#f08a24", f' class="bub" style="animation-delay:{d:.2f}s"'))
    b.append(embers(450, top - 6, rng, n=8, spread=500))
    for side in (0, pool_x + pool_w):
        for y in (top - 32, top, top + 32):
            for x in range(side, side + pool_x, 30):
                b.append(block(x, y, 30, rng.choice([0, 1, 2, 4, 5])))
        b.append(moss_on(side + 10, top - 32, 90, rng))
    b.append(torch(60, top - 32, rng) + torch(840, top - 32, rng))
    save("footer.svg", svg(W, H, "".join(b), "Volte sempre, explorador!"))

header(); about(); skills(); footer()
banner("title-sobre.svg", "SOBRE MIM")
banner("title-arsenal.svg", "ARSENAL")
banner("title-stats.svg", "ESTATÍSTICAS")
print("ok")
