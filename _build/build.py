# Builds inventory.html, units/*.html, sitemap.xml and the shared header/footer.
# Run from the repo root:  python _build/build.py
# Unit data: _build/units.json (source of each unit in field "src").
import json, re, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALL_UNITS = json.loads((ROOT / "_build" / "units.json").read_text(encoding="utf-8"))
# Sold units leave the site; reserved units stay with a badge.
UNITS = [u for u in ALL_UNITS if u.get("status") not in ("sold", "hidden")]
LISTED = "21 October 2026"
UPDATED = "26 October 2026"
TODAY = datetime.date.today().isoformat()
SITE = "https://lks360.com"
MAIL = "manager@lks360.com"
PHONE = "+49 170 4656619"

CATS = {
    "gas": ("Gas turbine", "Gas turbines", "/gas-turbines.html"),
    "steam": ("Steam turbine", "Steam turbines", "/steam-turbines.html"),
    "genset": ("Generator set", "Generator sets", "/generator-sets.html"),
}
ICON = {
    "gas": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 18h8l6-6h10l6 6h6v12h-6l-6 6H20l-6-6H6z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M20 18v12M26 16v16M32 18v12" stroke="currentColor" stroke-width="2.4"/></svg>',
    "steam": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="26" r="11" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M24 15v22M13 26h22M16 18l16 16M32 18L16 34" stroke="currentColor" stroke-width="2"/><path d="M18 10c0-3 3-3 3-6M27 10c0-3 3-3 3-6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "genset": '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="5" y="14" width="38" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M10 36v4M38 36v4M11 20h14M11 25h14M11 30h14" stroke="currentColor" stroke-width="2.4"/><path d="M34 19l-4 7h5l-4 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/></svg>',
}

e = lambda s: html.escape(str(s), quote=True)
WA = "https://wa.me/491704656619"
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]


def long_date(d):
    # "26.10.2026" -> "26 October 2026"
    day, mon, year = d.split(".")
    return f"{int(day)} {MONTH_NAMES[int(mon) - 1]} {year}"


def approx(n, unit):
    # Owner rule: hours and starts only rounded ("approx. 86,000 h"); 0 stays exact.
    if n in ("", None):
        return ""
    n = int(str(n).replace(",", ""))
    if n == 0:
        return f"0 {unit}"
    step = 1000 if n >= 10000 else 100 if n >= 1000 else 10
    return f"approx. {round(n / step) * step:,} {unit}"


def badge(u):
    return '<span class="badge reserved">Reserved</span>' if u.get("status") == "reserved" else ""


def confirmed(u):
    return f"Last confirmed {long_date(u['confirmed'])}" if u.get("confirmed") else f"Listed {LISTED}"


def slug(u):
    s = (u["id"] + "-" + u["name"] + ("-" + u["output"] if u["output"] else "")).lower()
    s = s.replace("ä", "a").replace("+", "-plus")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:90].rstrip("-")


for u in UNITS:
    u["slug"] = slug(u)
    u["url"] = f"/units/{u['slug']}.html"


def header():
    return f"""<header><div class="wrap nav">
  <a class="brand" href="/">LKS <span>360</span>-SCHREINER LLC</a>
  <input type="checkbox" id="menu" class="menu-toggle"><label for="menu" class="menu-btn" aria-label="Open menu"><span></span><span></span><span></span></label>
  <nav><a href="/inventory.html">Inventory</a><a href="/gas-turbines.html">Gas turbines</a><a href="/steam-turbines.html">Steam turbines</a><a href="/generator-sets.html">Generator sets</a><a href="/sell.html">Sell equipment</a><a href="/news.html">News</a><a href="/how-we-work.html">How we work</a><a class="btn" href="/contact.html">Contact</a></nav>
</div></header>"""


def footer():
    return f"""<footer><div class="wrap fcols">
  <div><p class="fbrand">LKS <span>360</span>-SCHREINER LLC</p><p>Florida limited liability company<br>Document No. L26000221347<br>7901 4th St N, Ste 300<br>St. Petersburg, FL 33702, USA</p></div>
  <div><p class="fh">Equipment</p><a href="/inventory.html">Inventory</a><a href="/gas-turbines.html">Gas turbines</a><a href="/steam-turbines.html">Steam turbines</a><a href="/generator-sets.html">Generator sets</a><a href="/sell.html">Sell equipment</a></div>
  <div><p class="fh">Company</p><a href="/news.html">News</a><a href="/how-we-work.html">How we work</a><a href="/compliance.html">Compliance</a><a href="/imprint.html">Imprint</a><a href="/privacy.html">Privacy Policy</a><a href="https://www.linkedin.com/company/142908032">LinkedIn</a></div>
  <div><p class="fh">Contact</p><a href="mailto:{MAIL}">{MAIL}</a><a href="tel:+491704656619">{PHONE}</a><a href="/contact.html">Contact form</a></div>
</div><div class="wrap fbase">© 2026 LKS 360-SCHREINER LLC. Equipment is offered on behalf of its owners and subject to prior sale. Manufacturer names describe the equipment; we are not affiliated with any manufacturer.</div></footer>
<a class="wafloat" href="{WA}" aria-label="WhatsApp +49 170 4656619"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.6 14.6 0 0 0 5.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.2-.3-.3-.6-.4z"/></svg></a>"""


def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LKS 360-SCHREINER LLC">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/img/gas-turbine-rotor.jpg">
<link rel="stylesheet" href="/style.css">
{extra}</head>
<body>
"""


def chips(u):
    out = [u["output"], u["hz"], u["year"], u["condition"], approx(u.get("hours"), "h"),
           approx(u.get("starts"), "starts"), u.get("continent", "")]
    return "".join(f"<span>{e(x)}</span>" for x in out if x)


def row(u):
    cat = CATS[u["cat"]][0]
    hz = u["hz"].replace(" Hz", "") if u["hz"] else ""
    return f"""<article class="unit" data-cat="{u['cat']}" data-make="{e(u['make'] or 'Other')}" data-hz="{e(hz)}" data-mw="{u['mw'] if u['mw'] is not None else ''}" data-text="{e((u['id']+' '+u['name']+' '+u['model']).lower())}">
  <div class="uicon {u['cat']}">{ICON[u['cat']]}</div>
  <div class="ubody">
    <p class="ustock">Stock No. LKS-{u['id']} · {cat} {badge(u)}</p>
    <h3><a href="{u['url']}">{e(u['name'])}</a></h3>
    <p class="chips">{chips(u)}</p>
    <p class="confirmed">{confirmed(u)}</p>
  </div>
  <div class="uact"><p class="price">Price on request</p><a class="btn sm" href="{u['url']}">Details</a><a class="btn sm ghost" href="{mailto(u)}">Request offer</a></div>
</article>"""


def mailto(u):
    from urllib.parse import quote
    subj = f"Request LKS-{u['id']}: {u['name']}"
    body = (f"Stock No.: LKS-{u['id']}\nUnit: {u['name']}\n\nCompany:\nName:\nPhone:\n"
            "Delivery country:\nNumber of units:\nTimeline:\n")
    return f"mailto:{MAIL}?subject={quote(subj)}&body={quote(body)}"


def spec_rows(u):
    rows = [("Stock No.", f"LKS-{u['id']}"), ("Type", CATS[u["cat"]][0]), ("Manufacturer", u["make"]),
            ("Model", u["model"] if u["make"] else ""), ("Quantity", u.get("qty", "")), ("Output", u["output"]),
            ("Frequency", u["hz"]), ("Fuel", u["fuel"]), ("Year", u["year"]), ("Condition", u["condition"]),
            ("Operating hours", approx(u.get("hours"), "h")), ("Starts", approx(u.get("starts"), "starts")),
            ("Location", u.get("continent", "")), ("Status", "Reserved" if u.get("status") == "reserved" else "Available"),
            ("Price", "On request"), ("Last confirmed", long_date(u["confirmed"]) if u.get("confirmed") else LISTED)]
    return "\n".join(f"<tr><th>{k}</th><td>{e(v) if v else '<span class=muted>On request</span>'}</td></tr>" for k, v in rows)


def unit_page(u):
    catname, catplural, catpath = CATS[u["cat"]]
    title = f"{u['name']}{', ' + u['output'] if u['output'] and u['output'] not in u['name'] else ''} | LKS-{u['id']}"
    desc = (f"{u['name']}" + (f", {u['output']}" if u['output'] else "") + (f", {u['hz']}" if u['hz'] else "")
            + (f", year {u['year']}" if u['year'] else "") + (f", {u['condition'].lower()}" if u['condition'] else "")
            + ". Offered on behalf of the owner by LKS 360-SCHREINER LLC. Price on request.")
    props = [{"@type": "PropertyValue", "name": k, "value": v} for k, v in
             [("Output", u["output"]), ("Frequency", u["hz"]), ("Fuel", u["fuel"]), ("Year", u["year"]),
              ("Condition", u["condition"]), ("Operating hours", approx(u.get("hours"), "h")),
              ("Location", u.get("continent", ""))] if v]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": u["name"], "sku": f"LKS-{u['id']}", "category": catname,
         "description": desc, "url": SITE + u["url"],
         **({"brand": {"@type": "Brand", "name": u["make"]}} if u["make"] else {}),
         "additionalProperty": props},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Inventory", "item": SITE + "/inventory.html"},
            {"@type": "ListItem", "position": 3, "name": u["name"], "item": SITE + u["url"]}]}]}
    related = [x for x in UNITS if x["cat"] == u["cat"] and x["id"] != u["id"]][:3]
    scope = f"<h2>Scope</h2><p>{e(u['scope'])}</p>" if u["scope"] else ""
    return head(title, desc, u["url"], f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/inventory.html">Inventory</a> / <a href="{catpath}">{catplural}</a> / LKS-{u['id']}</div>
<section class="unitpage"><div class="wrap two">
  <div>
    <p class="kicker">{catname} · Stock No. LKS-{u['id']} {badge(u)}</p>
    <h1>{e(u['name'])}</h1>
    <p class="chips big">{chips(u)}</p>
    <table class="spec">{spec_rows(u)}</table>
    {scope}
    <p class="muted small">Offered on behalf of the owner and subject to prior sale. Serial numbers, unit location and full technical documents are released after receipt of a letter of intent.</p>
  </div>
  <aside class="card side">
    <p class="price big">Price on request</p>
    <a class="btn full" href="{mailto(u)}">Request offer</a>
    <a class="btn ghost full" href="/contact.html?unit=LKS-{u['id']}">Contact form</a>
    <a class="btn wa full" href="{WA}">WhatsApp</a>
    <h3>Next steps</h3>
    <ol class="nextsteps"><li>Send your requirement with company details.</li><li>You receive an offer with the owner's conditions.</li><li>With your letter of intent: full data and inspection.</li><li>Purchase contract between you and the owner.</li></ol>
    <p class="small">Questions: <a href="mailto:{MAIL}">{MAIL}</a><br>{PHONE}</p>
  </aside>
</div></section>
<section class="soft"><div class="wrap">
  <p class="kicker">More {catplural.lower()}</p>
  <h2>Similar units</h2>
  <div class="ulist">{''.join(row(x) for x in related)}</div>
  <p><a href="/inventory.html?cat={u['cat']}">All {catplural.lower()} in our inventory</a></p>
</div></section>
""" + footer() + "\n</body>\n</html>\n"


def inventory_page():
    n = len(UNITS)
    counts = {k: sum(1 for u in UNITS if u["cat"] == k) for k in CATS}
    makes = sorted({u["make"] or "Other" for u in UNITS})
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "LKS 360-SCHREINER LLC inventory",
          "numberOfItems": n, "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": SITE + u["url"], "name": u["name"]} for i, u in enumerate(UNITS)]}
    opts = "".join(f'<option value="{e(m)}">{e(m)}</option>' for m in makes)
    return head(f"Used Gas Turbines, Steam Turbines and Generator Sets for Sale | Inventory | LKS 360-SCHREINER LLC",
                f"{n} gas turbines, steam turbines and generator sets for sale: Siemens, GE, Solar, Mitsubishi, Caterpillar, Wärtsilä and more. 50 and 60 Hz. Offered on behalf of the owners.",
                "/inventory.html", f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="hero slim"><div class="wrap">
  <p class="kicker light">Inventory · updated {UPDATED}</p>
  <h1>Gas turbines, steam turbines and generator sets for sale</h1>
  <p>{n} units from owners in our network: {counts['gas']} gas turbines, {counts['steam']} steam turbines and {counts['genset']} generator sets. Each listing has a stock number. Prices on request.</p>
</div></div>
<section class="inv"><div class="wrap">
  <form class="filters" id="filters" onsubmit="return false">
    <input type="search" id="q" placeholder="Search model or stock no." aria-label="Search">
    <select id="fcat" aria-label="Type"><option value="">All types</option><option value="gas">Gas turbines ({counts['gas']})</option><option value="steam">Steam turbines ({counts['steam']})</option><option value="genset">Generator sets ({counts['genset']})</option></select>
    <select id="fmake" aria-label="Manufacturer"><option value="">All manufacturers</option>{opts}</select>
    <select id="fhz" aria-label="Frequency"><option value="">50 and 60 Hz</option><option value="50">50 Hz</option><option value="60">60 Hz</option></select>
    <select id="fmw" aria-label="Output"><option value="">Any output</option><option value="0-10">Up to 10 MW</option><option value="10-50">10 to 50 MW</option><option value="50-150">50 to 150 MW</option><option value="150-9999">Above 150 MW</option></select>
    <select id="fsort" aria-label="Sort"><option value="">Sort: stock no.</option><option value="desc">Output high to low</option><option value="asc">Output low to high</option></select>
  </form>
  <p class="count" id="count">{n} units</p>
  <div class="ulist" id="ulist">
{''.join(row(u) for u in UNITS)}
  </div>
  <p class="empty" id="empty" hidden>No unit matches. Send us your requirement and we match it with units offered by their owners: <a href="/contact.html">contact form</a>.</p>
  <p class="muted small">All units are offered on behalf of their owners and subject to prior sale. Serial numbers, unit location and full technical documents are released after receipt of a letter of intent.</p>
</div></section>
<div class="cta">
  <h2>Not on the list?</h2>
  <p>Send type, output, frequency and delivery country. We match it with units offered by their owners.</p>
  <a class="btn alt" href="/contact.html">Send your requirement</a>
</div>
""" + footer() + '\n<script src="/site.js"></script>\n</body>\n</html>\n'


def cat_block(cat):
    us = [u for u in UNITS if u["cat"] == cat]
    return (f'<!--UNITS-->\n<section class="soft"><div class="wrap">\n  <p class="kicker">Inventory · updated {UPDATED}</p>\n'
            f'  <h2>{len(us)} {CATS[cat][1].lower()} for sale</h2>\n  <div class="ulist">{"".join(row(u) for u in us)}</div>\n'
            f'  <p><a href="/inventory.html?cat={cat}">Filter all units in the inventory</a></p>\n</div></section>\n<!--/UNITS-->')


def featured_block():
    fs = [u for u in UNITS if u.get("featured")]
    counts = {k: sum(1 for u in UNITS if u["cat"] == k) for k in CATS}
    cards = "".join(f"""<a class="card fcard" href="{u['url']}"><div class="uicon {u['cat']}">{ICON[u['cat']]}</div><p class="ustock">LKS-{u['id']} {badge(u)}</p><h3>{e(u['name'])}</h3><p class="chips">{chips(u)}</p></a>""" for u in fs)
    return f"""<!--FEATURED-->
<section class="soft"><div class="wrap">
  <p class="kicker">Inventory</p>
  <h2>Selected units for sale</h2>
  <ul class="stats"><li><b>{len(UNITS)}</b>units listed</li><li><b>{counts['gas']}</b>gas turbines</li><li><b>{counts['steam']}</b>steam turbines</li><li><b>{counts['genset']}</b>generator sets</li></ul>
  <div class="grid3">{cards}</div>
  <p style="margin-top:28px"><a class="btn" href="/inventory.html">View full inventory</a></p>
</div></section>
<!--/FEATURED-->"""


MODELS = [
    ("siemens-sgt-800-for-sale", "Siemens SGT-800", r"SGT-800",
     "Siemens SGT-800 industrial gas turbines and combined cycle blocks, offered on behalf of their owners."),
    ("ge-tm2500-for-sale", "GE TM2500", r"TM2500",
     "GE TM2500 mobile aeroderivative gas turbine generators, offered on behalf of their owners."),
    ("ge-lm2500-for-sale", "GE LM2500", r"\bLM2500",
     "GE LM2500 aeroderivative gas turbines, including trailer-mounted packages, offered on behalf of their owners."),
]


def model_page(slugname, label, pattern, lead):
    us = [u for u in UNITS if re.search(pattern, u["model"] + " " + u["name"])]
    path = f"/{slugname}.html"
    n = len(us)
    plural = "s" if n != 1 else ""
    title = f"{label} for Sale | LKS 360-SCHREINER LLC"
    desc = (f"{label} for sale: {n} unit{plural} in our inventory with stock number, output, frequency and status. "
            "Price on request. Letter of intent, data and inspection, payment through escrow.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ItemList", "name": f"{label} for sale", "numberOfItems": n, "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + u["url"], "name": u["name"]} for i, u in enumerate(us)]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Gas turbines", "item": SITE + "/gas-turbines.html"},
            {"@type": "ListItem", "position": 3, "name": f"{label} for sale", "item": SITE + path}]}]}
    units_html = "".join(row(u) for u in us) or '<p class="empty">No unit of this model is listed at the moment.</p>'
    return head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/gas-turbines.html">Gas turbines</a> / {e(label)}</div>
<div class="hero slim"><div class="wrap">
  <p class="kicker light">Inventory · updated {UPDATED}</p>
  <h1>{e(label)} for sale</h1>
  <p>{e(lead)}</p>
</div></div>
<section><div class="wrap">
  <p class="kicker">Units in our inventory</p>
  <h2>{n} {e(label)} unit{plural} listed</h2>
  <div class="ulist">{units_html}</div>
  <p class="muted small">Each unit is offered on behalf of its owner and subject to prior sale. Serial numbers, unit location and full technical documents are released after receipt of a letter of intent.</p>
</div></section>
<section class="soft"><div class="wrap">
  <p class="kicker">How a purchase works</p>
  <h2>From letter of intent to contract</h2>
  <div class="steps">
    <div class="card"><div class="num">1</div><h3>Letter of intent</h3><p>You send a letter of intent with the stock number and the number of units.</p></div>
    <div class="card"><div class="num">2</div><h3>Data and inspection</h3><p>You receive the technical documents and can inspect the unit.</p></div>
    <div class="card"><div class="num">3</div><h3>Escrow</h3><p>Payment goes directly from buyer to owner, or through a third-party escrow agent agreed between them.</p></div>
    <div class="card"><div class="num">4</div><h3>Contract</h3><p>Buyer and owner sign the purchase contract.</p></div>
  </div>
</div></section>
<div class="cta">
  <h2>Looking for a {e(label)}?</h2>
  <p>Send output, frequency, number of units and delivery country.</p>
  <a class="btn alt" href="/contact.html">Send your requirement</a> <a class="btn wa" href="{WA}">WhatsApp</a>
</div>
""" + footer() + "\n</body>\n</html>\n"


POSTS = json.loads((ROOT / "_build" / "posts.json").read_text(encoding="utf-8"))
POSTS.sort(key=lambda p: -p["num"])
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}


def post_date(p):
    d = p["date"] or (re.search(r"(\d{1,2} [A-Z][a-z]+ 2026)", p["title"]) or [None, ""])[1]
    if not d:
        return "", ""
    day, mon, year = d.split()
    return f"{int(day)} {mon} {year}", f"{year}-{MONTHS[mon]:02d}-{int(day):02d}"


def post_page(p):
    shown, iso = post_date(p)
    plain = re.sub(r"<[^>]+>", " ", p["html"])
    desc = re.sub(r"\s+", " ", plain).strip()[:155]
    path = f"/news/{p['slug']}.html"
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"][:110], "url": SITE + path,
          "author": {"@type": "Person", "name": "Lothar Schreiner"},
          "publisher": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"}},
          **({"datePublished": iso} if iso else {})}
    return head(p["title"] + " | LKS 360-SCHREINER LLC", desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/news.html">News</a></div>
<section class="unitpage"><div class="wrap legal post">
  <p class="kicker">News{' · ' + shown if shown else ''}</p>
  <h1>{e(p['title'])}</h1>
  <div class="postbody">{p['html']}</div>
  <p class="note">Availability changes every week. All units are offered on behalf of their owners and subject to prior sale. Current units: <a href="/inventory.html">inventory</a>.</p>
  <p><a href="/news.html">All news</a></p>
</div></section>
""" + footer() + "\n</body>\n</html>\n"


def news_page():
    items = []
    for p in POSTS:
        shown, _ = post_date(p)
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", p["html"])).strip()
        items.append(f"""<article class="newsitem"><p class="ustock">{shown or 'News'}</p><h3><a href="/news/{p['slug']}.html">{e(p['title'])}</a></h3><p class="muted">{e(plain[:180])}...</p></article>""")
    return head("News: Gas Turbines, Steam Turbines and Gensets for Sale and Wanted | LKS 360-SCHREINER LLC",
                "Offers, wanted lists and market notes on used gas turbines, steam turbines and generator sets from LKS 360-SCHREINER LLC.",
                "/news.html") + header() + f"""
<div class="hero slim"><div class="wrap">
  <p class="kicker light">News</p>
  <h1>Offers, wanted lists and market notes</h1>
  <p>Our posts on gas turbines, steam turbines and generator sets, newest first. Current units are in the <a href="/inventory.html" style="color:#fff">inventory</a>.</p>
</div></div>
<section><div class="wrap"><div class="newslist">{''.join(items)}</div></div></section>
""" + footer() + "\n</body>\n</html>\n"


def patch_static(path):
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<header>.*?</header>", lambda m: header(), t, count=1, flags=re.S)
    t = re.sub(r"<footer>.*?</footer>", lambda m: footer(), t, count=1, flags=re.S)
    t = t.replace('href="style.css"', 'href="/style.css"').replace('href="favicon.svg"', 'href="/favicon.svg"')
    cat = {"gas-turbines.html": "gas", "steam-turbines.html": "steam", "generator-sets.html": "genset"}.get(path.name)
    if cat and "<!--UNITS-->" in t:
        t = re.sub(r"<!--UNITS-->.*?<!--/UNITS-->", lambda m: cat_block(cat), t, flags=re.S)
    if path.name == "index.html" and "<!--FEATURED-->" in t:
        t = re.sub(r"<!--FEATURED-->.*?<!--/FEATURED-->", lambda m: featured_block(), t, flags=re.S)
    path.write_text(t, encoding="utf-8", newline="\n")


STATIC = ["index.html", "inventory.html", "gas-turbines.html", "steam-turbines.html", "generator-sets.html",
          "sell.html", "news.html", "how-we-work.html", "contact.html", "compliance.html", "imprint.html", "privacy.html"]

(ROOT / "units").mkdir(exist_ok=True)
for old in (ROOT / "units").glob("*.html"):
    old.unlink()
for u in UNITS:
    (ROOT / "units" / f"{u['slug']}.html").write_text(unit_page(u), encoding="utf-8", newline="\n")
(ROOT / "inventory.html").write_text(inventory_page(), encoding="utf-8", newline="\n")
(ROOT / "news.html").write_text(news_page(), encoding="utf-8", newline="\n")
for m in MODELS:
    (ROOT / f"{m[0]}.html").write_text(model_page(*m), encoding="utf-8", newline="\n")
(ROOT / "news").mkdir(exist_ok=True)
for old in (ROOT / "news").glob("*.html"):
    old.unlink()
for p in POSTS:
    (ROOT / "news" / f"{p['slug']}.html").write_text(post_page(p), encoding="utf-8", newline="\n")
for name in STATIC:
    p = ROOT / name
    if p.exists() and name not in ("inventory.html", "news.html"):
        patch_static(p)
for name in ["404.html"]:
    patch_static(ROOT / name)

urls = [f"{SITE}/"] + [f"{SITE}/{n}" for n in STATIC[1:] if (ROOT / n).exists()] + [f"{SITE}/{m[0]}.html" for m in MODELS] + [SITE + u["url"] for u in UNITS] + [f"{SITE}/news/{p['slug']}.html" for p in POSTS]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                  + "".join(f"  <url><loc>{x}</loc><lastmod>{TODAY}</lastmod></url>\n" for x in urls)
                                  + "</urlset>\n", encoding="utf-8", newline="\n")

# llms.txt: keep the hand-written head, regenerate the unit and news lists so AI search finds every unit.
llms_path = ROOT / "llms.txt"
llms_head = llms_path.read_text(encoding="utf-8").split("\n## Units for sale")[0].rstrip() + "\n"
def llms_line(u):
    facts = ", ".join(x for x in [u["output"], u["hz"], str(u["year"] or ""), u["condition"], approx(u.get("hours"), "h"),
                                  "reserved" if u.get("status") == "reserved" else ""] if x)
    return f"- [LKS-{u['id']}: {u['name']}]({SITE}{u['url']}): {facts}. Price on request, subject to prior sale."
llms = (llms_head + f"\n## Units for sale (stock list, updated {TODAY})\n"
        + "\n".join(llms_line(u) for u in UNITS)
        + "\n\n## News\n" + "\n".join(f"- [{p['title']}]({SITE}/news/{p['slug']}.html)" for p in POSTS) + "\n")
llms_path.write_text(llms, encoding="utf-8", newline="\n")

print(len(UNITS), "unit pages,", len(POSTS), "posts,", len(urls), "sitemap URLs")
