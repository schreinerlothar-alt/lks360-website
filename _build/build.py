# Builds inventory.html, units/*.html, sitemap.xml and the shared header/footer.
# Run from the repo root:  python _build/build.py
# Unit data: _build/units.json (source of each unit in field "src").
import json, re, html, datetime, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_images

ROOT = Path(__file__).resolve().parent.parent
ALL_UNITS = json.loads((ROOT / "_build" / "units.json").read_text(encoding="utf-8"))
# Sold units stay listed without any mark: they still bring inquiries (Lothar 02.11.2026). Only "hidden" units leave.
UNITS = [u for u in ALL_UNITS if u.get("status") != "hidden"]
OPEN_UNITS = UNITS
LISTED = "21 October 2026"
UPDATED = "8 November 2026"
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
  <div><p class="fh">Equipment</p><a href="/inventory.html">Inventory</a><a href="/gas-turbines.html">Gas turbines</a><a href="/steam-turbines.html">Steam turbines</a><a href="/generator-sets.html">Generator sets</a><a href="/sell.html">Sell equipment</a><a href="/used-60-hz-gas-turbines-generators-americas.html">60 Hz for the Americas</a></div>
  <div><p class="fh">Company</p><a href="/news.html">News</a><a href="/how-we-work.html">How we work</a><a href="/buying-used-gas-turbines.html">Buyer guide</a><a href="/gas-turbine-faq.html">Gas turbine FAQ</a><a href="/steam-turbine-faq.html">Steam turbine FAQ</a><a href="/generator-set-faq.html">Genset FAQ</a><a href="/power-generation-glossary.html">Glossary</a><a href="/power-generation-equipment-models-compared.html">Models compared</a><a href="/compliance.html">Compliance</a><a href="/imprint.html">Imprint</a><a href="/privacy.html">Privacy Policy</a><a href="https://www.linkedin.com/company/142908032">LinkedIn</a><a href="https://www.facebook.com/groups/606333518127054">Facebook</a><a href="https://www.pinterest.com/schreinerlothar/">Pinterest</a><a href="https://x.com/lothar81795958">X</a><a href="https://www.instagram.com/lotschrei/">Instagram</a><a href="https://www.youtube.com/channel/UCP2-Bw2a4iCVZOgQC1tMshQ">YouTube</a></div>
  <div><p class="fh">Contact</p><a href="mailto:{MAIL}">{MAIL}</a><a href="tel:+491704656619">{PHONE}</a><a href="/contact.html">Contact form</a></div>
</div><div class="wrap fbase">© 2026 LKS 360-SCHREINER LLC. Equipment is offered on behalf of its owners and subject to prior sale. Manufacturer names describe the equipment; we are not affiliated with any manufacturer.</div></footer>
<a class="wafloat" href="{WA}" aria-label="WhatsApp +49 170 4656619"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.6 14.6 0 0 0 5.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.2-.3-.3-.6-.4z"/></svg></a>"""


def head(title, desc, path, extra="", img="/img/gas-turbine-rotor.jpg"):
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
<meta property="og:image" content="{SITE}{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}{img}">
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
  <a class="uthumb" href="{u['url']}"><img src="/img/cards/lks-{u['id'].lower()}.jpg" width="1200" height="630" alt="{e(u['name'])}, stock number LKS-{u['id']}" loading="lazy"></a>
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
            ("Location", u.get("continent", "")), ("Status", {"reserved": "Reserved", "sold": ""}.get(u.get("status"), "Available")),
            ("Price", "On request"), ("Last confirmed", long_date(u["confirmed"]) if u.get("confirmed") else LISTED)]
    return "\n".join(f"<tr><th>{k}</th><td>{e(v) if v else '<span class=muted>On request</span>'}</td></tr>" for k, v in rows)


def unit_card(u):
    # Share card with public listing data only (no price, location by continent).
    img = f"/img/cards/lks-{u['id'].lower()}.jpg"
    facts = [x for x in [u["output"], u["hz"], u["year"] and f"Year {u['year']}", u["condition"],
                         approx(u.get("hours"), "h"), u.get("continent", "")] if x]
    note = "Reserved" if u.get("status") == "reserved" else "Price on request"
    make_images.card(str(ROOT / img.lstrip("/")), f"{CATS[u['cat']][0]} for sale · Stock No. LKS-{u['id']}",
                     u["name"], facts[:6], note)
    return img


def product_ld(u, desc, img):
    # Product facts only. No offers (prices on request) and no ratings (none collected yet).
    p = {"@type": "Product", "name": u["name"], "sku": f"LKS-{u['id']}", "mpn": f"LKS-{u['id']}",
         "description": desc, "image": SITE + img, "category": CATS[u["cat"]][0],
         "url": SITE + u["url"]}
    if u.get("make"):
        p["brand"] = {"@type": "Brand", "name": u["make"]}
        p["manufacturer"] = {"@type": "Organization", "name": u["make"]}
    if u.get("model"):
        p["model"] = u["model"]
    if u.get("year") and re.fullmatch(r"\d{4}", str(u["year"])):
        p["productionDate"] = str(u["year"])
    cond = (u.get("condition") or "").lower()
    if cond.startswith(("new", "unused")):
        p["itemCondition"] = "https://schema.org/NewCondition"
    elif "overhaul" in cond or "rebuilt" in cond:
        p["itemCondition"] = "https://schema.org/RefurbishedCondition"
    props = [(k, v) for k, v in [("Output", u["output"]), ("Frequency", u["hz"]), ("Fuel", u["fuel"]),
             ("Year", u["year"]), ("Condition", u["condition"]), ("Operating hours", approx(u.get("hours"), "h")),
             ("Location", u.get("continent", ""))] if v]
    if props:
        p["additionalProperty"] = [{"@type": "PropertyValue", "name": k, "value": v} for k, v in props]
    p["isRelatedTo"] = {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "url": SITE + "/"}
    return p


def unit_page(u):
    catname, catplural, catpath = CATS[u["cat"]]
    title = f"{u['name']}{', ' + u['output'] if u['output'] and u['output'] not in u['name'] else ''} | LKS-{u['id']}"
    desc = (f"{u['name']}" + (f", {u['output']}" if u['output'] else "") + (f", {u['hz']}" if u['hz'] else "")
            + (f", year {u['year']}" if u['year'] else "") + (f", {u['condition'].lower()}" if u['condition'] else "")
            + ". Offered on behalf of the owner by LKS 360-SCHREINER LLC. Price on request.")
    img = unit_card(u)
    props = [{"@type": "PropertyValue", "name": k, "value": v} for k, v in
             [("Output", u["output"]), ("Frequency", u["hz"]), ("Fuel", u["fuel"]), ("Year", u["year"]),
              ("Condition", u["condition"]), ("Operating hours", approx(u.get("hours"), "h")),
              ("Location", u.get("continent", ""))] if v]
    ld = {"@context": "https://schema.org", "@graph": [
        # ItemPage, not Product: Google requires offers/price for Product snippets, and prices stay on request.
        {"@type": "ItemPage", "name": u["name"], "url": SITE + u["url"], "description": desc,
         "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + img, "width": 1200, "height": 630,
                                "creditText": "LKS 360-SCHREINER LLC", "copyrightNotice": "LKS 360-SCHREINER LLC",
                                "creator": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC"},
                                "license": SITE + "/imprint.html#image-use", "acquireLicensePage": SITE + "/contact.html"},
         "about": product_ld(u, desc, img)},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Inventory", "item": SITE + "/inventory.html"},
            {"@type": "ListItem", "position": 3, "name": u["name"], "item": SITE + u["url"]}]}]}
    exhtml, exobj = example_for_unit(u)
    if exobj:
        ld["@graph"][0]["about"]["image"] = [SITE + img, exobj]
    related = [x for x in UNITS if x["cat"] == u["cat"] and x["id"] != u["id"]][:3]
    scope = f"<h2>Scope</h2><p>{e(u['scope'])}</p>" if u["scope"] else ""
    return head(title, desc, u["url"], f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n', img) + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/inventory.html">Inventory</a> / <a href="{catpath}">{catplural}</a> / LKS-{u['id']}</div>
<section class="unitpage"><div class="wrap two">
  <div>
    <p class="kicker">{catname} · Stock No. LKS-{u['id']} {badge(u)}</p>
    <h1>{e(u['name'])}</h1>
    <img class="ucard" src="{img}" width="1200" height="630" alt="{e(u['name'])}, stock number LKS-{u['id']}, {e(catname.lower())} for sale">
    <p class="chips big">{chips(u)}</p>
    {exhtml}
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
    n = len(OPEN_UNITS)
    counts = {k: sum(1 for u in OPEN_UNITS if u["cat"] == k) for k in CATS}
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
    fs = [u for u in OPEN_UNITS if u.get("featured")]
    counts = {k: sum(1 for u in OPEN_UNITS if u["cat"] == k) for k in CATS}
    cards = "".join(f"""<a class="card fcard" href="{u['url']}"><img class="fimg" src="/img/cards/lks-{u['id'].lower()}.jpg" width="1200" height="630" alt="{e(u['name'])}, stock number LKS-{u['id']}" loading="lazy"><p class="ustock">LKS-{u['id']} {badge(u)}</p><h3>{e(u['name'])}</h3><p class="chips">{chips(u)}</p></a>""" for u in fs)
    return f"""<!--FEATURED-->
<section class="soft"><div class="wrap">
  <p class="kicker">Inventory</p>
  <h2>Selected units for sale</h2>
  <ul class="stats"><li><b>{len(OPEN_UNITS)}</b>units listed</li><li><b>{counts['gas']}</b>gas turbines</li><li><b>{counts['steam']}</b>steam turbines</li><li><b>{counts['genset']}</b>generator sets</li></ul>
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
    ("ge-lm6000-for-sale", "GE LM6000", r"LM6000",
     "GE LM6000 aeroderivative gas turbines, offered on behalf of their owners."),
    ("ge-lm5000-for-sale", "GE LM5000", r"LM5000",
     "GE LM5000 aeroderivative gas turbine units, offered on behalf of their owners."),
    ("ge-frame-6b-for-sale", "GE Frame 6B", r"Frame 6B",
     "GE Frame 6B heavy duty gas turbines, offered on behalf of their owners."),
    ("ge-7ea-for-sale", "GE 7EA", r"\b7EA",
     "GE 7EA heavy duty gas turbines, offered on behalf of their owners."),
    ("ge-frame-5-for-sale", "GE Frame 5 (MS5001)", r"Frame 5|MS5001",
     "GE Frame 5 (MS5001) gas turbines, including power barge units, offered on behalf of their owners."),
    ("ge-9ha-for-sale", "GE 9HA", r"9HA",
     "GE 9HA heavy duty gas turbines, offered on behalf of their owners."),
    ("siemens-sgt-600-for-sale", "Siemens SGT-600", r"SGT-600|GT10B",
     "Siemens SGT-600 (GT10B) industrial gas turbines, offered on behalf of their owners."),
    ("siemens-sgt-700-for-sale", "Siemens SGT-700", r"SGT-700",
     "Siemens SGT-700 industrial gas turbines and combined cycle units, offered on behalf of their owners."),
    ("siemens-sgt-400-for-sale", "Siemens SGT-400", r"SGT-400",
     "Siemens SGT-400 industrial gas turbines, offered on behalf of their owners."),
    ("siemens-sgt-300-for-sale", "Siemens SGT-300", r"SGT-300",
     "Siemens SGT-300 industrial gas turbines, offered on behalf of their owners."),
    ("siemens-sgt-100-for-sale", "Siemens SGT-100", r"SGT-100",
     "Siemens SGT-100 industrial gas turbine generator sets, offered on behalf of their owners."),
    ("ge-frame-9e-for-sale", "GE Frame 9E", r"Frame 9E|9171E",
     "GE Frame 9E heavy duty gas turbines, offered on behalf of their owners."),
    ("siemens-westinghouse-w701-w501-for-sale", "Siemens Westinghouse W701 and W501", r"W701|W501|\b701D",
     "Siemens Westinghouse W701 and W501 heavy duty gas turbines, offered on behalf of their owners."),
    ("solar-titan-for-sale", "Solar Titan", r"Titan",
     "Solar Turbines Titan 130 and Titan 250 gas turbines, offered on behalf of their owners."),
    ("solar-centaur-40-for-sale", "Solar Centaur 40", r"Centaur",
     "Solar Turbines Centaur 40 gas turbine generator sets, offered on behalf of their owners."),
    ("mitsubishi-mf111-for-sale", "Mitsubishi MF111", r"MF111",
     "Mitsubishi MF111 gas turbine generator sets, offered on behalf of their owners."),
    ("siemens-sgt5-2000e-for-sale", "Siemens SGT5-2000E", r"SGT5-2000E",
     "Siemens SGT5-2000E heavy duty gas turbines and combined cycle modules, offered on behalf of their owners."),
    ("ge-7fa-for-sale", "GE 7FA (7F)", r"\b7FA|\b7F\.0",
     "GE 7FA and 7F heavy duty gas turbines, offered on behalf of their owners."),
    ("siemens-sgt-750-for-sale", "Siemens SGT-750", r"SGT-750",
     "Siemens SGT-750 industrial gas turbines, offered on behalf of their owners."),
    ("siemens-sst-400-for-sale", "Siemens SST-400", r"SST-400",
     "Siemens SST-400 steam turbine generator sets, offered on behalf of their owners.", "steam"),
    ("siemens-sst-300-for-sale", "Siemens SST-300", r"SST-300",
     "Siemens SST-300 steam turbine generators, offered on behalf of their owners.", "steam"),
    ("caterpillar-g20cm34-for-sale", "Caterpillar G20CM34", r"G20CM34",
     "Caterpillar G20CM34 gas generator sets, offered on behalf of their owners.", "genset"),
    ("caterpillar-3516-for-sale", "Caterpillar 3516", r"3516",
     "Caterpillar 3516B and 3516C generator sets, offered on behalf of their owners.", "genset"),
    ("wartsila-34sg-for-sale", "Wärtsilä 34SG", r"34SG",
     "Wärtsilä 34SG gas engine power plants, offered on behalf of their owners.", "genset"),
    ("man-32-40-for-sale", "MAN 32/40", r"32/40",
     "MAN B&W 32/40 diesel generator sets, offered on behalf of their owners.", "genset"),
    ("mtu-16v4000-for-sale", "MTU 16V4000", r"16V4000",
     "MTU 16V4000 diesel generator sets, offered on behalf of their owners.", "genset"),
    ("jenbacher-j620-for-sale", "Jenbacher J620", r"J620|Jenbacher",
     "INNIO Jenbacher J620 gas engine generator sets, offered on behalf of their owners.", "genset"),
    ("cummins-generator-sets-for-sale", "Cummins genset", r"Cummins",
     "Cummins gas and diesel generator sets, offered on behalf of their owners.", "genset"),
]


# Example photos of the model type from Wikimedia Commons (free licences). Not the unit offered; credited on the page.
EXAMPLES = {
    "ge-lm2500-for-sale": ("ge-lm2500.jpg", "GE LM2500 aeroderivative gas turbine", "Europepress", "CC0",
                           "https://creativecommons.org/publicdomain/zero/1.0/", "https://commons.wikimedia.org/wiki/File:Lm2500.jpg"),
    "ge-tm2500-for-sale": ("ge-lm2500.jpg", "GE LM2500 gas turbine, the engine of the TM2500 package", "Europepress", "CC0",
                           "https://creativecommons.org/publicdomain/zero/1.0/", "https://commons.wikimedia.org/wiki/File:Lm2500.jpg"),
    "ge-lm6000-for-sale": ("ge-lm6000.jpg", "GE LM6000 gas turbine in operation", "Pro-Per Energy Services", "CC BY-SA 4.0",
                           "https://creativecommons.org/licenses/by-sa/4.0/", "https://commons.wikimedia.org/wiki/File:Gas_Turbine_4.jpg"),
    "ge-frame-6b-for-sale": ("ge-frame-6b-ms6001b.jpg", "GE MS6001B (Frame 6B) gas turbines at a power plant", "Jochen Burgstaller", "CC BY-SA 3.0",
                             "https://creativecommons.org/licenses/by-sa/3.0/", "https://commons.wikimedia.org/wiki/File:GTKWTHY_1.jpg"),
    "siemens-sst-400-for-sale": ("siemens-steam-turbine-rotor.jpg", "Siemens steam turbine rotor during assembly", "Siemens Pressebild", "CC BY-SA 3.0",
                                 "https://creativecommons.org/licenses/by-sa/3.0/", "https://commons.wikimedia.org/wiki/File:Dampfturbine_Montage01.jpg"),
    "mtu-16v4000-for-sale": ("mtu-16v4000.jpg", "MTU 16V4000 diesel engine", "Linie29", "CC BY-SA 4.0",
                             "https://creativecommons.org/licenses/by-sa/4.0/", "https://commons.wikimedia.org/wiki/File:MTU_4000_16V_R41_%C3%96BB_2016.jpg"),
    "cummins-generator-sets-for-sale": ("cummins-generator-set.jpg", "Cummins generator set", "Mbrickn", "CC BY 4.0",
                                        "https://creativecommons.org/licenses/by/4.0/", "https://commons.wikimedia.org/wiki/File:Cummins_Generator.jpg"),
}


def example_fig(slugname):
    x = EXAMPLES.get(slugname)
    if not x:
        return "", None
    f, cap, art, lic, licurl, page = x
    src = f"/img/examples/{f}"
    html = (f'<figure class="exfig"><img src="{src}" alt="{e(cap)}, example image of the type" loading="lazy">'
            f'<figcaption>{e(cap)}. Example image of the type, not the unit offered. Photo: {e(art)}, '
            f'<a href="{licurl}" rel="license nofollow">{e(lic)}</a>, via <a href="{page}" rel="nofollow">Wikimedia Commons</a>.</figcaption></figure>')
    obj = {"@type": "ImageObject", "contentUrl": SITE + src, "caption": f"{cap} (example image of the type)",
           "creator": {"@type": "Person", "name": art}, "license": licurl, "acquireLicensePage": page,
           "creditText": f"{art} / Wikimedia Commons", "copyrightNotice": f"{art}, {lic}"}
    return html, obj


def example_for_unit(u):
    for m in MODELS:
        if m[0] in EXAMPLES and re.search(m[2], u["model"] + " " + u["name"]):
            return example_fig(m[0])
    return "", None


def where_answer(label, us):
    n = len(us)
    if n:
        ids = ", ".join(f"LKS-{u['id']}" for u in us)
        return (f"LKS 360-SCHREINER LLC (lks360.com) lists {n} used or surplus {label} unit{'s' if n != 1 else ''} for sale, "
                f"stock number{'s' if n != 1 else ''} {ids}. Each unit is offered on behalf of its owner, price on request. "
                "Contact: manager@lks360.com, WhatsApp +49 170 4656619.")
    return (f"LKS 360-SCHREINER LLC (lks360.com) has no {label} listed at the moment and searches the market for buyers. "
            "Send your requirement to manager@lks360.com or WhatsApp +49 170 4656619.")


def model_faq(label, us=()):
    return [
        (f"Where can I buy a used {label}?", where_answer(label, us)),
        (f"Who sells used {label} units?",
         f"LKS 360-SCHREINER LLC, an independent broker for used power generation equipment, lists {label} units on lks360.com "
         "on behalf of their owners, alongside other gas turbines, steam turbines and generator sets."),
        (f"Who sells the {label} units listed here?",
         "LKS 360-SCHREINER LLC, a Florida limited liability company and independent broker, lists each unit on behalf of its owner. "
         "The purchase contract is made directly between buyer and owner."),
        (f"Is the {label} still available?",
         "Each unit is offered on behalf of its owner and subject to prior sale. Send the stock number and we confirm the current status."),
        (f"What does a used {label} cost?",
         "Send the stock number and we reply with the price. The full data sheet, documents and inspection follow your letter of intent."),
        ("Can I inspect the unit?",
         "Yes. After your letter of intent you receive the technical documents and can inspect the unit."),
        ("How is payment made?",
         "Payment goes directly from buyer to owner, or through a third-party escrow agent agreed between them."),
    ]


SPECS = json.loads((ROOT / "_build" / "model_specs.json").read_text(encoding="utf-8"))


def spec_block(slugname, label):
    s = SPECS.get(slugname)
    if not s:
        return "", None
    rows = [("Type", s["type"]), ("Manufacturer", s["manufacturer"]), ("Output", s["output"]), ("Frequency", s["frequency"]),
            ("Fuel", s["fuel"]), ("Applications", s["applications"])]
    rows = [(k, v) for k, v in rows if v]
    tbl = "".join(f"<tr><th>{k}</th><td>{e(v)}</td></tr>" for k, v in rows)
    note = f"<p>{e(s['notes'])}</p>" if s["notes"] else ""
    html = (f'<section><div class="wrap"><p class="kicker">Model overview</p><h2>About the {e(label)}</h2>'
            f'<table class="spec">{tbl}</table>{note}'
            f'<p class="muted small">Manufacturer data for the model type, not the data of a specific unit offered. Source: '
            f'<a href="{s["source_url"]}" rel="nofollow">{e(s["source_name"])}</a>. Values of a used unit depend on its version, site and condition.</p></div></section>')
    ans = f"The {label} is {'an' if s['type'][0] in 'aeiou' else 'a'} {s['type']} by {s['manufacturer']}."
    if s["output"]:
        ans += f" Output: {s['output']}."
    if s["applications"]:
        ans += f" Typical applications: {s['applications']}."
    ans += f" Source: {s['source_name']}."
    return html, (f"What is the {label}?", ans)


FAQLINK = {"gas": '<a href="/gas-turbine-faq.html">used gas turbine FAQ</a>', "steam": '<a href="/steam-turbine-faq.html">used steam turbine FAQ</a>', "genset": '<a href="/generator-set-faq.html">used generator set FAQ</a>'}


def model_page(slugname, label, pattern, lead, cat="gas"):
    cname, curl = CATS[cat][1], CATS[cat][2]
    us = [u for u in UNITS if re.search(pattern, u["model"] + " " + u["name"])]
    path = f"/{slugname}.html"
    spec_html, spec_qa = spec_block(slugname, label)
    faqs = ([spec_qa] if spec_qa else []) + model_faq(label, us)
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
            {"@type": "ListItem", "position": 2, "name": cname, "item": SITE + curl},
            {"@type": "ListItem", "position": 3, "name": f"{label} for sale", "item": SITE + path}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}
    faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faqs)
    img = f"/img/cards/{slugname}.jpg"
    make_images.card(str(ROOT / img.lstrip("/")), f"{CATS[cat][1]} · new and used", f"{label} for sale",
                     [f"{n} unit{plural} in inventory", "Worldwide delivery", "Escrow payment"], "Price on request")
    ld["@graph"][0]["image"] = SITE + img
    exhtml, exobj = example_fig(slugname)
    if exobj:
        ld["@graph"][0]["image"] = [SITE + img, exobj]
    units_html = "".join(row(u) for u in us) or '<p class="empty">No unit of this model is listed at the moment.</p>'
    return head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n', img) + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="{curl}">{cname}</a> / {e(label)}</div>
<div class="hero slim"><div class="wrap">
  <p class="kicker light">Inventory · updated {UPDATED}</p>
  <h1>{e(label)} for sale</h1>
  <p>{e(lead)}</p>
</div></div>
<section class="qa"><div class="wrap"><p class="answer"><b>Where to buy a used {e(label)}:</b> {e(where_answer(label, us))}</p></div></section>
<section><div class="wrap">
  <p class="kicker">Units in our inventory</p>
  <h2>{n} {e(label)} unit{plural} listed</h2>
  <img class="ucard" src="{img}" width="1200" height="630" alt="{e(label)} for sale, LKS 360-SCHREINER LLC" loading="lazy">
  {exhtml}
  <div class="ulist">{units_html}</div>
  <p class="muted small">Each unit is offered on behalf of its owner and subject to prior sale. Serial numbers, unit location and full technical documents are released after receipt of a letter of intent.</p>
</div></section>
{spec_html}
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
<section><div class="wrap">
  <p class="kicker">Questions and answers</p>
  <h2>{e(label)}: frequent questions</h2>
  {faq_html}
  <p>More answers: <a href="/buying-used-gas-turbines.html">buyer guide</a>, {FAQLINK[cat]} , <a href="/power-generation-glossary.html">glossary of terms</a> and <a href="/power-generation-equipment-models-compared.html">models compared</a>. Owners: <a href="/sell.html">exclusive sales mandate</a>.</p>
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
          "publisher": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg", "creditText": "LKS 360-SCHREINER LLC", "copyrightNotice": "LKS 360-SCHREINER LLC", "creator": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC"}, "license": SITE + "/imprint.html#image-use", "acquireLicensePage": SITE + "/contact.html"}},
          **({"datePublished": iso} if iso else {})}
    # Article image: first picture in the post, otherwise the site picture (Google wants an image for articles).
    m = re.search(r'src="(/img/[^"]+)"', p["html"])
    img = m.group(1) if m else "/img/gas-turbine-rotor.jpg"
    ld["image"] = SITE + img
    return head(p["title"] + " | LKS 360-SCHREINER LLC", desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n', img) + header() + f"""
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
    t = re.sub(r'\s*<a class="wafloat".*?</a>', "", t, flags=re.S)
    t = re.sub(r"<footer>.*?</footer>", lambda m: footer(), t, count=1, flags=re.S)
    t = t.replace('href="style.css"', 'href="/style.css"').replace('href="favicon.svg"', 'href="/favicon.svg"')
    cat = {"gas-turbines.html": "gas", "steam-turbines.html": "steam", "generator-sets.html": "genset"}.get(path.name)
    if cat and "<!--UNITS-->" in t:
        t = re.sub(r"<!--UNITS-->.*?<!--/UNITS-->", lambda m: cat_block(cat), t, flags=re.S)
    if path.name == "index.html" and "<!--FEATURED-->" in t:
        t = re.sub(r"<!--FEATURED-->.*?<!--/FEATURED-->", lambda m: featured_block(), t, flags=re.S)
    path.write_text(t, encoding="utf-8", newline="\n")


HZ_SLUG = "used-60-hz-gas-turbines-generators-americas"


def hz_page():
    us = [u for u in UNITS if "60" in (u.get("hz") or "")]
    am = [u for u in us if u.get("continent") == "Americas"]
    path = f"/{HZ_SLUG}.html"
    n = len(us)
    title = "Used 60 Hz Gas Turbines, Steam Turbines and Generator Sets for the USA and the Americas | LKS 360-SCHREINER LLC"
    desc = (f"{n} used and surplus 60 Hz units for the United States, Canada, Mexico and Latin America: gas turbines, steam turbines "
            "and generator sets with stock number. Price on request. Florida LLC, letter of intent, inspection, escrow.")
    faqs = [
        ("Where can I buy a used 60 Hz gas turbine in the USA?",
         f"LKS 360-SCHREINER LLC, a Florida limited liability company, lists {n} used or surplus 60 Hz units on lks360.com, "
         f"{len(am)} of them located in the Americas. Each unit is offered on behalf of its owner. Send the stock number to manager@lks360.com "
         "and we reply with the price."),
        ("Can a 50 Hz unit be used in the United States?",
         "The US grid runs at 60 Hz. A 50 Hz unit usually needs a different gearbox or generator, so buyers in the Americas normally look for "
         "60 Hz units or units specified for both frequencies. See the used gas turbine FAQ for details."),
        ("Who is the contracting party for buyers in the Americas?",
         "LKS 360-SCHREINER LLC, 7901 4th St N, Ste 300, St. Petersburg, FL 33702, acts as independent broker. The purchase contract is made "
         "directly between buyer and owner, and payment runs through escrow or a letter of credit."),
        ("What does a buyer need to receive full data and inspection?",
         "A letter of intent with the stock number, buyer company, end user and site. Full documents, serial numbers and inspection follow the LOI."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Used 60 Hz power generation equipment for the Americas", "url": SITE + path,
         "about": "Used 60 Hz gas turbines, steam turbines and generator sets", "areaServed": ["United States", "Canada", "Mexico", "Latin America"],
         "provider": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "url": SITE + "/"}},
        {"@type": "ItemList", "name": "60 Hz units for sale", "numberOfItems": n, "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + u["url"], "name": u["name"]} for i, u in enumerate(us)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}
    faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faqs)
    units_html = "".join(row(u) for u in us)
    return head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/inventory.html">Inventory</a> / 60 Hz for the Americas</div>
<div class="hero slim"><div class="wrap">
  <p class="kicker light">USA · Canada · Mexico · Latin America · updated {UPDATED}</p>
  <h1>Used 60 Hz gas turbines, steam turbines and generator sets</h1>
  <p>Units for 60 Hz grids, offered on behalf of their owners by LKS 360-SCHREINER LLC, a Florida limited liability company.</p>
</div></div>
<section class="qa"><div class="wrap"><p class="answer"><b>Short answer:</b> {e(faqs[0][1])}</p></div></section>
<section><div class="wrap">
  <p class="kicker">60 Hz units in our inventory</p>
  <h2>{n} units listed, {len(am)} located in the Americas</h2>
  <div class="ulist">{units_html}</div>
  <p class="muted small">Each unit is offered on behalf of its owner and subject to prior sale. Location is shown by continent only. Serial numbers and full documents follow a letter of intent.</p>
</div></section>
<section class="soft"><div class="wrap">
  <p class="kicker">Questions and answers</p>
  <h2>Buying 60 Hz equipment in the Americas</h2>
  {faq_html}
  <p>More answers: <a href="/gas-turbine-faq.html">used gas turbine FAQ</a>, <a href="/buying-used-gas-turbines.html">buyer guide</a>, <a href="/generator-set-faq.html">generator set FAQ</a>. Owners in the Americas: <a href="/sell.html">exclusive sales mandate</a>.</p>
</div></section>
<div class="cta">
  <h2>Looking for a 60 Hz unit?</h2>
  <p>Send output, fuel, number of units and delivery country.</p>
  <a class="btn alt" href="/contact.html">Send your requirement</a> <a class="btn wa" href="{WA}">WhatsApp</a>
</div>
""" + footer() + "\n</body>\n</html>\n"


COMPARE = [
    ("ge-lm6000-vs-lm2500", "ge-lm6000-for-sale", "ge-lm2500-for-sale"),
    ("ge-lm2500-vs-tm2500", "ge-lm2500-for-sale", "ge-tm2500-for-sale"),
    ("siemens-sgt-800-vs-sgt-700", "siemens-sgt-800-for-sale", "siemens-sgt-700-for-sale"),
    ("siemens-sgt-400-vs-sgt-300", "siemens-sgt-400-for-sale", "siemens-sgt-300-for-sale"),
    ("ge-frame-9e-vs-7ea", "ge-frame-9e-for-sale", "ge-7ea-for-sale"),
    ("wartsila-34sg-vs-jenbacher-j620", "wartsila-34sg-for-sale", "jenbacher-j620-for-sale"),
]
CMP_SLUG = "power-generation-equipment-models-compared"
_MINFO = {m[0]: (m[1], m[2], m[4] if len(m) > 4 else "gas") for m in MODELS}
_FIELDS = [("Type", "type"), ("Manufacturer", "manufacturer"), ("Output", "output"), ("Frequency", "frequency"),
           ("Fuel", "fuel"), ("Applications", "applications")]


def _units_of(slugname):
    pat = _MINFO[slugname][1]
    return [u for u in UNITS if re.search(pat, u["model"] + " " + u["name"])]


def _src(s):
    return f'<a href="{s["source_url"]}" rel="nofollow">{e(s["source_name"])}</a>'


def compare_overview():
    path = f"/{CMP_SLUG}.html"
    title = "Gas Turbine, Steam Turbine and Generator Set Models Compared | Output, Frequency, Fuel | LKS 360-SCHREINER LLC"
    desc = (f"Comparison table of {len(SPECS)} power generation models: GE LM2500, LM6000, Frame 9E, 7FA, Siemens SGT-800, "
            "SGT-700, SGT-400, steam turbines and gas engines with output, frequency, fuel and manufacturer source.")
    groups = [("gas", "Gas turbines"), ("steam", "Steam turbines"), ("genset", "Generator sets and engines")]
    body, items = "", []
    for cat, name in groups:
        rows = ""
        for slugname, s in SPECS.items():
            if slugname not in _MINFO or _MINFO[slugname][2] != cat:
                continue
            label = _MINFO[slugname][0]
            n = len(_units_of(slugname))
            items.append((label, slugname))
            rows += (f'<tr><th><a href="/{slugname}.html">{e(label)}</a></th><td>{e(s["type"])}</td><td>{e(s["output"])}</td>'
                     f'<td>{e(s["frequency"]) or "<span class=muted>see source</span>"}</td><td>{n}</td><td>{_src(s)}</td></tr>')
        if rows:
            body += (f'<h2>{name}</h2><div class="tablewrap"><table class="spec cmp"><thead><tr><th>Model</th><th>Type</th><th>Output</th>'
                     f'<th>Frequency</th><th>Units listed</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div>')
    pairs = "".join(f'<li><a href="/{c[0]}.html">{e(_MINFO[c[1]][0])} vs {e(_MINFO[c[2]][0])}</a></li>' for c in COMPARE)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": "Power generation equipment models compared", "url": SITE + path,
         "publisher": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "url": SITE + "/"}},
        {"@type": "ItemList", "name": "Models compared", "numberOfItems": len(items), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": l, "url": f"{SITE}/{sl}.html"} for i, (l, sl) in enumerate(items)]}]}
    return head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/inventory.html">Inventory</a> / Models compared</div>
<div class="hero slim"><div class="wrap">
  <p class="kicker light">Knowledge · updated {UPDATED}</p>
  <h1>Gas turbine, steam turbine and generator set models compared</h1>
  <p>Manufacturer data for the model types we trade, side by side, each value with its source. The last column shows how many used or surplus units of the model are listed on lks360.com.</p>
</div></div>
<section><div class="wrap">
  {body}
  <p class="muted small">Manufacturer data for the model type, not the data of a specific unit offered. Values of a used unit depend on its version, site and condition. Prices on request with the stock number.</p>
  <h2>Direct comparisons</h2><ul>{pairs}</ul>
  <p>More answers: <a href="/gas-turbine-faq.html">gas turbine FAQ</a>, <a href="/steam-turbine-faq.html">steam turbine FAQ</a>, <a href="/generator-set-faq.html">generator set FAQ</a>, <a href="/power-generation-glossary.html">glossary</a>. Owners: <a href="/sell.html">exclusive sales mandate</a>.</p>
</div></section>
""" + footer() + "\n</body>\n</html>\n"


def compare_page(slug, a, b):
    sa, sb = SPECS[a], SPECS[b]
    la, lb = _MINFO[a][0], _MINFO[b][0]
    ua, ub = _units_of(a), _units_of(b)
    path = f"/{slug}.html"
    title = f"{la} vs {lb}: Output, Frequency, Fuel and Used Units for Sale | LKS 360-SCHREINER LLC"
    desc = f"{la} compared with {lb}: type, output, frequency, fuel and applications from manufacturer data, plus used units listed for sale."
    rows = "".join(f"<tr><th>{k}</th><td>{e(sa[f]) or '<span class=muted>not stated</span>'}</td><td>{e(sb[f]) or '<span class=muted>not stated</span>'}</td></tr>" for k, f in _FIELDS)
    rows += f"<tr><th>Units listed on lks360.com</th><td>{len(ua)}</td><td>{len(ub)}</td></tr>"
    rows += f"<tr><th>Source</th><td>{_src(sa)}</td><td>{_src(sb)}</td></tr>"
    diff = (f"The {la} is {'an' if sa['type'][0] in 'aeiou' else 'a'} {sa['type']} by {sa['manufacturer']} with an output of {sa['output']}. "
            f"The {lb} is {'an' if sb['type'][0] in 'aeiou' else 'a'} {sb['type']} by {sb['manufacturer']} with an output of {sb['output']}.")
    if sa["frequency"] and sb["frequency"]:
        diff += f" Frequency: {la} {sa['frequency']}, {lb} {sb['frequency']}."
    diff += f" Sources: {sa['source_name']}; {sb['source_name']}."
    have = (f"LKS 360-SCHREINER LLC lists {len(ua)} used or surplus {la} unit{'s' if len(ua) != 1 else ''} and {len(ub)} {lb} "
            f"unit{'s' if len(ub) != 1 else ''} on lks360.com, each offered on behalf of its owner. Send the stock number to manager@lks360.com and we reply with the price.")
    faqs = [(f"What is the difference between the {la} and the {lb}?", diff),
            (f"Where can I buy a used {la} or {lb}?", have),
            ("Which one fits my project?",
             "That depends on the output you need, grid frequency, fuel, emission limits and whether the plant runs base load, peaking or combined cycle. Send these values and we propose matching units from the market.")]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": f"{la} vs {lb}", "url": SITE + path,
         "about": [{"@type": "Product", "name": la, "url": f"{SITE}/{a}.html"}, {"@type": "Product", "name": lb, "url": f"{SITE}/{b}.html"}],
         "publisher": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "url": SITE + "/"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in faqs]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Models compared", "item": f"{SITE}/{CMP_SLUG}.html"},
            {"@type": "ListItem", "position": 3, "name": f"{la} vs {lb}", "item": SITE + path}]}]}
    faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(x)}</p>" for q, x in faqs)
    units_html = "".join(row(u) for u in ua + ub) or '<p class="empty">No unit of these models is listed at the moment.</p>'
    return head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + header() + f"""
<div class="crumbs wrap"><a href="/">Home</a> / <a href="/{CMP_SLUG}.html">Models compared</a> / {e(la)} vs {e(lb)}</div>
<div class="hero slim"><div class="wrap">
  <p class="kicker light">Comparison · updated {UPDATED}</p>
  <h1>{e(la)} vs {e(lb)}</h1>
  <p>Manufacturer data side by side, with the used units of both models listed on lks360.com.</p>
</div></div>
<section class="qa"><div class="wrap"><p class="answer"><b>Short answer:</b> {e(diff)}</p></div></section>
<section><div class="wrap">
  <div class="tablewrap"><table class="spec cmp"><thead><tr><th></th><th><a href="/{a}.html">{e(la)}</a></th><th><a href="/{b}.html">{e(lb)}</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="muted small">Manufacturer data for the model types, not the data of a specific unit offered.</p>
</div></section>
<section class="soft"><div class="wrap">
  <p class="kicker">Units in our inventory</p>
  <div class="ulist">{units_html}</div>
</div></section>
<section><div class="wrap">
  <p class="kicker">Questions and answers</p>
  {faq_html}
  <p>All models: <a href="/{CMP_SLUG}.html">models compared</a>. More answers: <a href="/gas-turbine-faq.html">gas turbine FAQ</a>, <a href="/buying-used-gas-turbines.html">buyer guide</a>. Owners: <a href="/sell.html">exclusive sales mandate</a>.</p>
</div></section>
<div class="cta">
  <h2>Looking for one of these models?</h2>
  <p>Send output, frequency, fuel and delivery country.</p>
  <a class="btn alt" href="/contact.html">Send your requirement</a> <a class="btn wa" href="{WA}">WhatsApp</a>
</div>
""" + footer() + "\n</body>\n</html>\n"


STATIC = ["index.html", "inventory.html", "gas-turbines.html", "steam-turbines.html", "generator-sets.html",
          "sell.html", "news.html", "how-we-work.html", "buying-used-gas-turbines.html", "gas-turbine-faq.html", "steam-turbine-faq.html", "generator-set-faq.html", "power-generation-glossary.html", "contact.html", "compliance.html", "imprint.html", "privacy.html"]

(ROOT / "units").mkdir(exist_ok=True)
for old in (ROOT / "units").glob("*.html"):
    old.unlink()
for u in UNITS:
    (ROOT / "units" / f"{u['slug']}.html").write_text(unit_page(u), encoding="utf-8", newline="\n")
(ROOT / "inventory.html").write_text(inventory_page(), encoding="utf-8", newline="\n")
(ROOT / "news.html").write_text(news_page(), encoding="utf-8", newline="\n")
# keep the model link line on each category page in step with MODELS
for _cat, (_s, _pl, _url) in CATS.items():
    _ms = [m for m in MODELS if (m[4] if len(m) > 4 else "gas") == _cat]
    if not _ms:
        continue
    _f = ROOT / _url.lstrip("/")
    _line = '<p class="modellinks">Model pages: ' + " · ".join(f'<a href="/{m[0]}.html">{m[1]} for sale</a>' for m in _ms) + "</p>"
    _tx = _f.read_text(encoding="utf-8")
    if '<p class="modellinks">' in _tx:
        _tx = re.sub(r'<p class="modellinks">.*?</p>', lambda _m: _line, _tx, count=1, flags=re.S)
    else:
        _tx = re.sub(r'(<h2>[^<]*</h2>\s*<p class="lead">.*?</p>)', lambda _m: _m.group(1) + "\n  " + _line, _tx, count=1, flags=re.S)
    _f.write_text(_tx, encoding="utf-8", newline="\n")
for m in MODELS:
    (ROOT / f"{m[0]}.html").write_text(model_page(*m), encoding="utf-8", newline="\n")
(ROOT / f"{HZ_SLUG}.html").write_text(hz_page(), encoding="utf-8", newline="\n")
(ROOT / f"{CMP_SLUG}.html").write_text(compare_overview(), encoding="utf-8", newline="\n")
for _c in COMPARE:
    (ROOT / f"{_c[0]}.html").write_text(compare_page(*_c), encoding="utf-8", newline="\n")
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

urls = [f"{SITE}/"] + [f"{SITE}/{n}" for n in STATIC[1:] if (ROOT / n).exists()] + [f"{SITE}/{m[0]}.html" for m in MODELS] + [f"{SITE}/{HZ_SLUG}.html"] + [f"{SITE}/{CMP_SLUG}.html"] + [f"{SITE}/{_c[0]}.html" for _c in COMPARE] + [SITE + u["url"] for u in UNITS] + [f"{SITE}/news/{p['slug']}.html" for p in POSTS]
IMGS = {**{f"{SITE}/{m[0]}.html": f"{SITE}/img/cards/{m[0]}.jpg" for m in MODELS},
        **{SITE + u["url"]: f"{SITE}/img/cards/lks-{u['id'].lower()}.jpg" for u in UNITS}}
def sm_img(x):
    return f"<image:image><image:loc>{IMGS[x]}</image:loc></image:image>" if x in IMGS else ""
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
                                  + "".join(f"  <url><loc>{x}</loc><lastmod>{TODAY}</lastmod>{sm_img(x)}</url>\n" for x in urls)
                                  + "</urlset>\n", encoding="utf-8", newline="\n")

# llms.txt: keep the hand-written head, regenerate the unit and news lists so AI search finds every unit.
llms_path = ROOT / "llms.txt"
llms_head = llms_path.read_text(encoding="utf-8").split("\n## Units for sale")[0].rstrip() + "\n"
_cnt = {c: sum(1 for u in UNITS if u["cat"] == c) for c in ("gas", "steam", "genset")}
llms_head = re.sub(r"^- \[Inventory\].*$", lambda m: f"- [Inventory]({SITE}/inventory.html): {len(UNITS)} listed units with stock numbers ({_cnt['gas']} gas turbines, {_cnt['steam']} steam turbines, {_cnt['genset']} generator sets), each with its own page under {SITE}/units/, filter by type, manufacturer, frequency and output. Prices on request.", llms_head, flags=re.M)
llms_head = re.sub(r"^- \[News\].*$", lambda m: f"- [News]({SITE}/news.html): {len(POSTS)} posts with offers, wanted lists and market notes on gas turbines, steam turbines and gensets", llms_head, flags=re.M)
llms_head = re.sub(r"^- \[Siemens SGT-800 for sale\].*model pages with listed units$", lambda m: f"- Model pages: {len(MODELS)} pages, one per turbine or engine model, see Model pages below", llms_head, flags=re.M)
def llms_line(u):
    facts = ", ".join(x for x in [u["output"], u["hz"], str(u["year"] or ""), u["condition"], approx(u.get("hours"), "h"),
                                  "reserved" if u.get("status") == "reserved" else ""] if x)
    return f"- [LKS-{u['id']}: {u['name']}]({SITE}{u['url']}): {facts}. Price on request, subject to prior sale."
llms = (llms_head + f"\n## Units for sale (stock list, updated {TODAY})\n"
        + "\n".join(llms_line(u) for u in UNITS)
        + "\n\n## Model pages\n" + "\n".join(f"- [{m[1]} for sale]({SITE}/{m[0]}.html)" for m in MODELS) + f"\n- [Used 60 Hz gas turbines, steam turbines and generator sets for the USA and the Americas]({SITE}/{HZ_SLUG}.html)" + f"\n- [Power generation equipment models compared (output, frequency, fuel, sources)]({SITE}/{CMP_SLUG}.html)" + "".join(f"\n- [{_MINFO[_c[1]][0]} vs {_MINFO[_c[2]][0]}]({SITE}/{_c[0]}.html)" for _c in COMPARE)
        + "\n\n## News\n" + "\n".join(f"- [{p['title']}]({SITE}/news/{p['slug']}.html)" for p in POSTS) + "\n")
llms_path.write_text(llms, encoding="utf-8", newline="\n")

# llms-full.txt: everything an AI assistant needs in one plain text file (no prices, no sellers, regions only by continent).
def _plain(name):
    import html as _h
    s = (ROOT / name).read_text(encoding="utf-8")
    s = re.sub(r"<(script|style|header|footer|nav)\b.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<(h[1-3])[^>]*>(.*?)</\1>", lambda m: "\n\n### " + re.sub(r"<[^>]+>", "", m.group(2)) + "\n", s, flags=re.S)
    s = re.sub(r"<(p|li|div)[^>]*>", "\n", s)
    s = _h.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()
def _unit_full(u):
    rows = [("Stock number", "LKS-" + u["id"]), ("Manufacturer", u.get("make")), ("Model", u.get("model")), ("Output", u.get("output")),
            ("Frequency", u.get("hz")), ("Fuel", u.get("fuel")), ("Year", str(u.get("year") or "")), ("Condition", u.get("condition")),
            ("Operating hours", approx(u.get("hours"), "h")), ("Quantity", str(u.get("qty") or "")), ("Scope", u.get("scope")),
            ("Region", u.get("continent")), ("Status", "reserved" if u.get("status") == "reserved" else "offered, subject to prior sale"),
            ("Price", "on request"), ("Page", SITE + u["url"])]
    return f"### {u['name']}\n" + "\n".join(f"- {k}: {v}" for k, v in rows if v)
_full = [llms_head.strip(), f"## Units for sale, full data (updated {TODAY})"] + [_unit_full(u) for u in UNITS]
_full.append("## Questions and answers per model")
for m in MODELS:
    _us = [u for u in UNITS if re.search(m[2], u["model"] + " " + u["name"])]
    _full.append(f"### {m[1]} ({SITE}/{m[0]}.html)\n" + "\n".join(f"Q: {q}\nA: {a}" for q, a in ([spec_block(m[0], m[1])[1]] if m[0] in SPECS else []) + model_faq(m[1], _us)))
for _n in ("how-we-work.html", "buying-used-gas-turbines.html", "gas-turbine-faq.html", "steam-turbine-faq.html", "generator-set-faq.html", "power-generation-glossary.html", "compliance.html", "sell.html"):
    if (ROOT / _n).exists():
        _full.append(f"## Page: {SITE}/{_n}\n\n" + _plain(_n))
(ROOT / "llms-full.txt").write_text("\n\n".join(_full) + "\n", encoding="utf-8", newline="\n")

print(len(UNITS), "unit pages,", len(POSTS), "posts,", len(urls), "sitemap URLs")
