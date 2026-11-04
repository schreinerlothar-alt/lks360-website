"""Share cards (1200x630 JPG) for every unit page and model page.
Called from build.py for every unit and model page.
Cards show public listing data only: no price, no location finer than continent."""
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "cards")
BG = os.path.join(ROOT, "img", "gas-turbine-rotor.jpg")
FD = "C:/Windows/Fonts/"
W, H = 1200, 630
CYAN = (95, 200, 215)
WHITE = (255, 255, 255)
GREY = (190, 200, 210)
CATNAME = {"gas": "Gas turbine", "steam": "Steam turbine", "genset": "Generator set"}


def font(bold, size):
    return ImageFont.truetype(FD + ("segoeuib.ttf" if bold else "segoeui.ttf"), size)


def background():
    im = Image.open(BG).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
    im = im.crop((0, 0, W, H))
    im = ImageEnhance.Brightness(im).enhance(0.45)
    shade = Image.new("RGB", (W, H), (12, 30, 52))
    return Image.blend(im, shade, 0.62)


BASE = None


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(path, kicker, title, chips, note):
    global BASE
    if BASE is None:
        BASE = background()
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    d.text((56, 44), kicker.upper(), font=font(True, 22), fill=CYAN)
    y = 88
    ft = font(True, 50)
    for line in wrap(d, title, ft, 1088)[:3]:
        d.text((56, y), line, font=ft, fill=WHITE)
        y += 62
    y += 18
    fc = font(False, 28)
    x = 56
    for c in chips:
        tw = d.textlength(c, font=fc)
        if x + tw + 36 > W - 56:
            x, y = 56, y + 58
        d.rounded_rectangle((x, y, x + tw + 32, y + 46), radius=8, outline=CYAN, width=2)
        d.text((x + 16, y + 6), c, font=fc, fill=WHITE)
        x += tw + 48
    d.text((56, 470), note, font=font(True, 34), fill=CYAN)
    d.line((56, 560, W - 56, 560), fill=CYAN, width=2)
    d.text((56, 574), "LKS 360-SCHREINER LLC · lks360.com · manager@lks360.com · WhatsApp +49 170 4656619",
           font=font(True, 21), fill=WHITE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", quality=84, optimize=True)
