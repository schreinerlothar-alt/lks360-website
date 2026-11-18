# Spanish pages for the 60 Hz markets of Latin America (Lothar 18.11.2026, proposal 8).
# Called from build.py with its globals. Unit pages stay in English; Spanish pages link to them.
# Facts only from units.json and model_specs.json sources; no prices, location by continent only.
import json, re

ES_MODELS = {
    # es slug: (en slug, label, unit pattern, data)
    "ge-tm2500-en-venta": ("ge-tm2500-for-sale", "GE TM2500", r"TM2500", {
        "noun": "turbina de gas móvil",
        "intro": "La GE TM2500 es un grupo generador con turbina de gas montado sobre remolques, construido alrededor de la turbina aeroderivada LM2500. Se traslada por carretera y se instala con rapidez donde se necesita energía.",
        "uses": ["Energía de emergencia y temporal", "Respaldo de la red durante paradas de planta", "Energía rápida para proyectos industriales"],
        "checks": ["Número de remolques y permisos de circulación", "Versión del motor y horas desde la última revisión general", "Equipos auxiliares para la instalación: suministro de combustible, transformador elevador, control"],
        "faq": [["¿Qué diferencia hay entre la TM2500 y la LM2500?", "La TM2500 es un paquete móvil sobre remolques con un motor de la familia LM2500. La LM2500 se instala normalmente como paquete fijo sobre cimentación."],
                ["¿Qué significa TM2500+?", "Según GE (comunicado del 2 de diciembre de 2008), la TM2500+ va montada en un sistema de dos remolques y entrega hasta 34 MW, con un 30 por ciento más de potencia que su predecesora en una superficie un 75 por ciento menor."]],
        "spec": {"Tipo": "Turbina de gas aeroderivada móvil", "Fabricante": "GE Vernova", "Potencia": "34.5 MW netos (DLE) y 34.6 MW netos (SAC) a 50 Hz",
                 "Combustible": "Gas, GLP y/o combustible líquido destilado", "Aplicaciones": "Puente hacia energía permanente, energía de emergencia y respaldo, ubicaciones aisladas"}}),
    "ge-lm6000-en-venta": ("ge-lm6000-for-sale", "GE LM6000", r"LM6000", {
        "noun": "turbina de gas",
        "intro": "La GE LM6000 es una turbina de gas aeroderivada de dos ejes, derivada del motor de avión CF6-80C2. Se emplea mucho en plantas de punta, cogeneración y centrales de arranque rápido.",
        "uses": ["Plantas de punta con arranques frecuentes", "Cogeneración y ciclo combinado", "Barcazas de energía y proyectos rápidos"],
        "checks": ["Versión PA, PC, PD o PF y si tiene SPRINT", "Tipo de cámara de combustión: SAC, DLE o inyección de agua", "Registros del motor, horas y ciclos desde la última revisión general"],
        "faq": [["¿Qué significa SPRINT en una LM6000?", "SPRINT es el enfriamiento por aspersión: se rocía agua en el compresor para enfriar el aire, lo que aumenta la potencia, sobre todo en días calurosos."],
                ["¿Qué diferencia hay entre SAC y DLE?", "SAC es la cámara de combustión anular simple, que GE Vernova describe con inyección de agua; DLE es la combustión seca de bajas emisiones. La hoja de datos de cada unidad indica cuál tiene."]],
        "spec": {"Tipo": "Turbina de gas aeroderivada", "Fabricante": "GE Vernova", "Potencia": "Aprox. 57 MW en ciclo simple (51.1 MW PC Sprint, 56.9 MW PF+ Sprint netos)",
                 "Frecuencia": "50 Hz y 60 Hz", "Combustible": "Gas natural, GLP, etanol, diésel, gas de coquería; apta para 100 % hidrógeno",
                 "Aplicaciones": "Arranque rápido y soporte de red, energía de respaldo, generación flexible y cogeneración"}}),
    "ge-lm2500-en-venta": ("ge-lm2500-for-sale", "GE LM2500", r"\bLM2500", {
        "noun": "turbina de gas",
        "intro": "La GE LM2500 es una turbina de gas aeroderivada usada en generación eléctrica, plataformas marinas y accionamiento mecánico. La familia incluye la LM2500 básica, la LM2500+ y la LM2500+G4.",
        "uses": ["Generación eléctrica de punta y respaldo", "Cogeneración industrial", "Plataformas y buques"],
        "checks": ["Versión: LM2500, LM2500+ o LM2500+G4", "Horas y ciclos desde la última revisión general del motor", "Paquete fijo o montado sobre remolque"],
        "faq": [["¿Qué diferencia hay entre la LM2500, la LM2500+ y la LM2500+G4?", "Son versiones de la misma familia; las versiones posteriores entregan más potencia. La hoja de datos de cada unidad indica la versión."],
                ["¿Qué potencia tiene una GE LM2500?", "GE Vernova indica aprox. 37 MW en ciclo simple para la LM2500 actual, con 34.5 MW (G4) y 36.3 MW (G5) netos a 50 Hz para el paquete LM2500XPRESS+. Las unidades más antiguas tienen menos potencia."]],
        "spec": {"Tipo": "Turbina de gas aeroderivada", "Fabricante": "GE Vernova", "Potencia": "Aprox. 37 MW en ciclo simple (LM2500XPRESS+ G4 34.5 MW, G5 36.3 MW netos, 50 Hz)",
                 "Frecuencia": "Opciones de 50 Hz y 60 Hz", "Combustible": "Combustible dual gas y diésel; también nafta, GLP, etano, etanol, biodiésel, mezclas con hidrógeno",
                 "Aplicaciones": "Potencia rápida y ciclos frecuentes, soporte de red, centros de datos, reserva, cogeneración, industria"}}),
    "ge-frame-6b-en-venta": ("ge-frame-6b-for-sale", "GE Frame 6B", r"Frame 6B", {
        "noun": "turbina de gas",
        "intro": "La GE Frame 6B (MS6001B) es una turbina de gas industrial de servicio pesado, conocida por su flexibilidad de combustible. Es una opción frecuente en refinerías, cogeneración y plantas industriales.",
        "uses": ["Cogeneración en refinerías y plantas químicas", "Energía industrial y operación en isla", "Plantas con combustibles líquidos"],
        "checks": ["Potencia en la placa y mejoras realizadas", "Fecha y alcance de la última inspección de ruta de gases calientes o revisión mayor", "Sistema de combustible: gas, líquido o dual"],
        "faq": [["¿La Frame 6B es lo mismo que la MS6001B?", "Sí. MS6001B es la designación de modelo de GE para la Frame 6B."],
                ["¿Qué potencia tiene una GE Frame 6B?", "GE Vernova indica 45 MW en ciclo simple, condiciones ISO y gas natural. Las unidades usadas suelen tener potencias menores según versión y estado."]],
        "spec": {"Tipo": "Turbina de gas industrial de servicio pesado", "Fabricante": "GE Vernova", "Potencia": "45 MW (ciclo simple, ISO, gas natural)",
                 "Frecuencia": "50 Hz y 60 Hz", "Combustible": "Amplia gama de gases o líquidos destilados, aceites pesados, nafta; apta para hidrógeno",
                 "Aplicaciones": "Refinerías, GNL, cogeneración, energía industrial, operación en isla y sitios remotos", "Flota": "Más de 1,200 unidades instaladas desde 1978"}}),
    "ge-7ea-en-venta": ("ge-7ea-for-sale", "GE 7EA", r"\b7EA", {
        "noun": "turbina de gas",
        "intro": "La GE 7EA es la turbina de gas de clase E para redes de 60 Hz; la Frame 9E es su equivalente de 50 Hz. 7EA es el nombre anterior de la GE Vernova 7E.",
        "uses": ["Generación de punta, cíclica y de base en redes de 60 Hz", "Cogeneración", "Ciclo combinado"],
        "checks": ["Potencia y mejoras realizadas", "Horas, arranques y última inspección mayor", "Sistema de combustible dual o solo gas"],
        "faq": [["¿Qué diferencia hay entre la 7EA y la 9E?", "La 7EA es el modelo de clase E para 60 Hz y la 9E el modelo de clase E para 50 Hz."],
                ["¿Qué potencia tiene una GE 7EA?", "GE Vernova indica 90 MW en ciclo simple para la 7E.03 actual a 60 Hz. Las unidades 7EA más antiguas tienen potencias menores."]],
        "spec": {"Tipo": "Turbina de gas industrial de servicio pesado", "Fabricante": "GE Vernova", "Potencia": "90 MW (7E.03, ciclo simple, ISO, gas natural)",
                 "Frecuencia": "60 Hz", "Combustible": "Gas natural como base, opciones multicombustible; hasta 100 % hidrógeno",
                 "Aplicaciones": "Picos, operación cíclica y de base, accionamiento mecánico, cogeneración, GNL"}}),
    "siemens-westinghouse-w501-en-venta": ("siemens-westinghouse-w701-w501-for-sale", "Siemens Westinghouse W501", r"W501", {
        "noun": "turbina de gas",
        "intro": "La W501 es la serie de turbinas de gas de servicio pesado de diseño Westinghouse para redes de 60 Hz, hoy en la gama de Siemens Energy. La W701 es su versión de 50 Hz.",
        "uses": ["Centrales eléctricas de 60 Hz", "Ciclo combinado", "Generación de base y de punta"],
        "checks": ["Generación de la unidad (letra después del número)", "Horas, arranques y estado tras la última revisión", "Disponibilidad de repuestos y servicio para la generación concreta"],
        "faq": [["¿Qué diferencia hay entre la W501 y la W701?", "La W501 es la serie de 60 Hz y la W701 la serie de 50 Hz; según Wikipedia, la W701 es una versión a escala de 50 Hz de la W501."],
                ["¿Qué potencia tiene una W501?", "Según Wikipedia, la serie W501 va desde aprox. 40 MW (W501A, 1968) hasta aprox. 120 MW en generaciones posteriores; la 501F pertenece a la clase de aprox. 150 MW."]],
        "spec": {"Tipo": "Turbina de gas industrial de servicio pesado", "Fabricante": "Siemens Energy (diseño Westinghouse)",
                 "Potencia": "W501: de aprox. 40 MW (W501A, 1968) a aprox. 120 MW en generaciones posteriores; 501F clase de aprox. 150 MW",
                 "Frecuencia": "W501: 60 Hz; W701: 50 Hz", "Nota": "Siemens vendió más tarde la 501F como SGT6-5000F"}}),
    "siemens-sgt-800-en-venta": ("siemens-sgt-800-for-sale", "Siemens SGT-800", r"SGT-800", {
        "noun": "turbina de gas",
        "intro": "La Siemens SGT-800 es la turbina de gas industrial más grande de la gama industrial de Siemens Energy. Se instala con frecuencia en ciclo combinado y cogeneración.",
        "uses": ["Centrales de ciclo combinado", "Cogeneración industrial y calefacción urbana", "Generación en ciclo simple para la industria"],
        "checks": ["Potencia nominal de la unidad y año de mejora, si la hay", "Si la turbina de vapor y la caldera de recuperación vienen incluidas", "Horas, arranques y fecha de la última inspección"],
        "faq": [["¿Cómo se llamaba antes la SGT-800?", "La SGT-800 proviene de la turbina de gas GTX100, desarrollada por ABB y luego Alstom, hoy parte de Siemens Energy."],
                ["¿Qué potencia tiene una Siemens SGT-800?", "Siemens Energy indica potencias de 45 a 62 MW en ciclo simple, para 50 Hz y 60 Hz."]],
        "spec": {"Tipo": "Turbina de gas industrial", "Fabricante": "Siemens Energy", "Potencia": "Hasta 62 MW (ciclo simple, potencias de 45 a 62 MW)",
                 "Frecuencia": "50 Hz y 60 Hz", "Combustible": "Gas natural, diésel No. 2 o combustible dual; DLE hasta 75 % vol. de hidrógeno",
                 "Aplicaciones": "Generación industrial, petróleo y gas, ciclo combinado y cogeneración"}}),
}
ES_STATIC = {"index.html": "/", "turbinas-de-gas.html": "/gas-turbines.html", "como-comprar-una-turbina-de-gas-usada.html": "/buying-used-gas-turbines.html"}
COND = {"new": "Nueva", "used": "Usada", "unused": "Sin uso"}
CONT = {"Asia": "Asia", "Europe": "Europa", "Americas": "América", "Africa": "África", "Middle East": "Oriente Medio", "Oceania": "Oceanía"}


def es_alt_map():
    # en path -> es path, for hreflang on both sides
    m = {v: "/es/" + ("" if k == "index.html" else k) for k, v in ES_STATIC.items()}
    for k, (en, *_r) in ES_MODELS.items():
        m[f"/{en}.html"] = f"/es/{k}.html"
    return m


def hreflang(site, en, es):
    return (f'<link rel="alternate" hreflang="en" href="{site}{en}">\n<link rel="alternate" hreflang="es" href="{site}{es}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{site}{en}">\n')


def build_es(g):
    e, SITE, UNITS, SPECS, ROOT, WA, MAIL, PHONE = g["e"], g["SITE"], g["UNITS"], g["SPECS"], g["ROOT"], g["WA"], g["MAIL"], g["PHONE"]
    out_dir = ROOT / "es"
    out_dir.mkdir(exist_ok=True)

    def head(title, desc, path, en_path, ld):
        return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
{hreflang(SITE, en_path, path)}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_419">
<meta property="og:site_name" content="LKS 360-SCHREINER LLC">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/img/gas-turbine-rotor.jpg">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><div class="wrap nav">
  <a class="brand" href="/es/">LKS <span>360</span>-SCHREINER LLC</a>
  <input type="checkbox" id="menu" class="menu-toggle"><label for="menu" class="menu-btn" aria-label="Abrir menú"><span></span><span></span><span></span></label>
  <nav><a href="/es/turbinas-de-gas.html">Turbinas de gas</a><a href="/es/como-comprar-una-turbina-de-gas-usada.html">Cómo comprar</a><a href="/inventory.html">Inventario (EN)</a><a href="{en_path}" hreflang="en">English</a><a class="btn" href="/contact.html">Contacto</a></nav>
</div></header>
"""

    def foot():
        return f"""<footer><div class="wrap fcols">
  <div><p class="fbrand">LKS <span>360</span>-SCHREINER LLC</p><p>Sociedad de responsabilidad limitada de Florida<br>Document No. L26000221347<br>7901 4th St N, Ste 300<br>St. Petersburg, FL 33702, EE. UU.</p></div>
  <div><p class="fh">Equipos</p><a href="/es/turbinas-de-gas.html">Turbinas de gas</a>{''.join(f'<a href="/es/{k}.html">{e(v[1])}</a>' for k, v in ES_MODELS.items())}</div>
  <div><p class="fh">Empresa</p><a href="/es/como-comprar-una-turbina-de-gas-usada.html">Cómo comprar</a><a href="/how-we-work.html">How we work (EN)</a><a href="/used-60-hz-gas-turbines-generators-americas.html">60 Hz for the Americas (EN)</a><a href="/imprint.html">Aviso legal (EN)</a><a href="/privacy.html">Privacidad (EN)</a></div>
  <div><p class="fh">Contacto</p><a href="mailto:{MAIL}">{MAIL}</a><a href="tel:+491704656619">{PHONE}</a><a href="{WA}">WhatsApp</a></div>
</div><div class="wrap fbase">© 2026 LKS 360-SCHREINER LLC. Los equipos se ofrecen en nombre de sus dueños y sujetos a venta previa. Los nombres de los fabricantes describen los equipos; no estamos vinculados a ningún fabricante.</div></footer>
</body>
</html>
"""

    def row(u):
        cond = COND.get((u.get("condition") or "").lower(), u.get("condition") or "")
        chips = [u.get("output"), u.get("hz"), u.get("year") and f"Año {u['year']}", cond, CONT.get(u.get("continent") or "", u.get("continent") or "")]
        ch = "".join(f"<span>{e(x)}</span>" for x in chips if x)
        st = " · Reservada" if u.get("status") == "reserved" else ""
        return f"""<article class="unit"><a class="uthumb" href="{u['url']}"><img src="/img/cards/lks-{u['id'].lower()}.jpg" width="1200" height="630" alt="{e(u['name'])}, número de stock LKS-{u['id']}" loading="lazy"></a>
  <div class="ubody"><p class="ustock">Stock No. LKS-{u['id']}{st}</p><h3><a href="{u['url']}">{e(u['name'])}</a></h3><p class="chips">{ch}</p></div>
  <div class="uact"><p class="price">Precio a consultar</p><a class="btn sm" href="{u['url']}">Detalles (EN)</a><a class="btn sm wa" href="{WA}">WhatsApp</a></div></article>"""

    def faq_ld(faqs):
        return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

    def faq_html(faqs):
        return "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faqs)

    def crumbs(items):
        return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}

    written = []
    gas = [u for u in UNITS if u["cat"] == "gas"]
    g60 = [u for u in gas if "60" in (u.get("hz") or "")]
    gas_sorted = g60 + [u for u in gas if u not in g60]

    # --- model pages
    for slug, (en, label, pat, d) in ES_MODELS.items():
        us = [u for u in UNITS if re.search(pat, u["model"] + " " + u["name"])]
        n = len(us)
        offer = [u for u in us if u.get("status") != "sold"]
        path, en_path = f"/es/{slug}.html", f"/{en}.html"
        if offer:
            k = len(offer)
            ids = ", ".join(f"LKS-{u['id']}" for u in offer)
            ans = (f"LKS 360-SCHREINER LLC (lks360.com), corredor independiente con sede en Florida, ofrece {k} {label} usada{'s' if k != 1 else ''} o excedente{'s' if k != 1 else ''} "
                   f"con número de stock {ids}, en nombre de sus dueños y sujetas a venta previa. El precio se envía a consulta; los datos completos y la inspección siguen a una carta de intención.")
        else:
            ans = (f"LKS 360-SCHREINER LLC (lks360.com), corredor independiente con sede en Florida, no tiene ninguna {label} publicada en este momento y busca en el mercado a pedido. "
                   f"Envíe potencia, frecuencia, combustible y país de destino a {MAIL} o por WhatsApp.")
        q0 = f"¿Dónde comprar una {label} usada?"
        sp = SPECS.get(en)
        spec = "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in d["spec"].items())
        src = f'<a href="{sp["source_url"]}" rel="nofollow">{e(sp["source_name"])}</a>' if sp else ""
        faqs = [(q0, ans)] + [tuple(x) for x in d["faq"]] + [
            (f"¿Cuánto cuesta una {label} usada?", f"LKS 360-SCHREINER LLC envía el precio de cada {label} publicada a consulta, con el número de stock. Depende de la versión, las horas y ciclos desde la última revisión, el estado, el alcance de suministro, la frecuencia y la ubicación."),
            ("¿Cómo se paga una turbina de gas usada?", "El comprador paga directamente al dueño mediante escrow o una carta de crédito irrevocable acordada entre ambos. Los pagos de compra nunca pasan por las cuentas de LKS 360-SCHREINER LLC.")]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "ItemList", "name": f"{label} usada en venta", "numberOfItems": n, "inLanguage": "es",
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + u["url"], "name": u["name"]} for i, u in enumerate(us)]},
            crumbs([("Inicio", "/es/"), ("Turbinas de gas", "/es/turbinas-de-gas.html"), (f"{label} en venta", path)]), faq_ld(faqs)]}
        title = f"{label} usada en venta: {d['noun']}, usos y qué revisar | LKS 360"
        desc = f"{label} usada en venta: {n} unidad{'es' if n != 1 else ''} con número de stock. Usos, datos del fabricante con fuente y qué revisar. Precio a consulta."
        units_html = "".join(row(u) for u in us) or '<p class="empty">No hay ninguna unidad de este modelo publicada en este momento.</p>'
        html = head(title, desc, path, en_path, ld) + f"""
<div class="crumbs wrap"><a href="/es/">Inicio</a> / <a href="/es/turbinas-de-gas.html">Turbinas de gas</a> / {e(label)}</div>
<div class="hero slim"><div class="wrap"><p class="kicker light">Inventario</p><h1>{e(label)} usada en venta</h1><p>{e(d['intro'].split('. ')[0])}.</p></div></div>
<section class="qa"><div class="wrap"><h2>{e(q0)}</h2><p class="answer">{e(ans)}</p></div></section>
<section><div class="wrap"><p class="kicker">Unidades en inventario</p><h2>{n} {e(label)} publicada{'s' if n != 1 else ''}</h2><div class="ulist">{units_html}</div>
<p class="muted small">Las fichas de las unidades están en inglés. Números de serie, ubicación exacta y documentos técnicos completos se entregan tras recibir una carta de intención.</p></div></section>
<section><div class="wrap"><p class="kicker">Guía del modelo</p><h2>Para qué se emplea la {e(label)}</h2><p>{e(d['intro'])}</p><ul>{''.join(f'<li>{e(x)}</li>' for x in d['uses'])}</ul>
<h2>Qué revisar al comprar una {e(label)} usada</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in d['checks'])}</ul></div></section>
<section class="soft"><div class="wrap"><p class="kicker">Datos del fabricante</p><h2>Datos de la {e(label)}</h2><table class="spec">{spec}</table>
<p class="muted small">Datos del fabricante para el tipo de modelo, no los datos de una unidad concreta. Fuente: {src}. Los valores de una unidad usada dependen de su versión, sitio y estado.</p></div></section>
<section><div class="wrap"><p class="kicker">Preguntas frecuentes</p><h2>{e(label)}: preguntas frecuentes</h2>{faq_html(faqs)}
<p>Más: <a href="/es/como-comprar-una-turbina-de-gas-usada.html">cómo comprar una turbina de gas usada</a>, <a href="/es/turbinas-de-gas.html">todas las turbinas de gas</a>, <a href="{en_path}" hreflang="en">página en inglés</a>.</p></div></section>
<div class="cta"><h2>¿Busca una {e(label)}?</h2><p>Envíe potencia, frecuencia, número de unidades y país de destino.</p><a class="btn alt" href="mailto:{MAIL}">Enviar requerimiento</a> <a class="btn wa" href="{WA}">WhatsApp</a></div>
""" + foot()
        (out_dir / f"{slug}.html").write_text(html, encoding="utf-8", newline="\n")
        written.append(path)

    links = " · ".join(f'<a href="/es/{k}.html">{e(v[1])} en venta</a>' for k, v in ES_MODELS.items())

    # --- gas turbine overview
    path = "/es/turbinas-de-gas.html"
    q0 = "¿Dónde comprar una turbina de gas usada de 60 Hz?"
    ans = (f"LKS 360-SCHREINER LLC (lks360.com), corredor independiente con sede en Florida, ofrece {len(gas)} turbinas de gas usadas o excedentes, "
           f"{len(g60)} de ellas para 60 Hz o para 50 y 60 Hz, de Siemens, GE, Solar Turbines, Mitsubishi y Siemens Westinghouse. "
           "Cada unidad tiene número de stock y se ofrece en nombre de su dueño; el precio se envía a consulta.")
    faqs = [(q0, ans),
            ("¿Puede usarse una turbina de 50 Hz en una red de 60 Hz?", "Según Wikipedia (Mains electricity by country), la mayoría de las redes de Norteamérica, Centroamérica y del norte de Sudamérica funcionan a 60 Hz. Una unidad de 50 Hz suele necesitar otro reductor u otro generador, por eso los compradores en redes de 60 Hz buscan unidades de 60 Hz o especificadas para ambas frecuencias."),
            ("¿Quién es la contraparte para compradores de América Latina?", "LKS 360-SCHREINER LLC, 7901 4th St N, Ste 300, St. Petersburg, FL 33702, EE. UU., actúa como corredor independiente. El contrato de compra se firma directamente entre comprador y dueño.")]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Turbinas de gas usadas en venta", "url": SITE + path, "inLanguage": "es"},
        crumbs([("Inicio", "/es/"), ("Turbinas de gas", path)]), faq_ld(faqs)]}
    html = head("Turbinas de gas usadas en venta, 60 Hz para América Latina | LKS 360",
                f"{len(gas)} turbinas de gas usadas y excedentes con número de stock, {len(g60)} para 60 Hz. Siemens, GE, Solar, Mitsubishi. Precio a consulta, carta de intención, inspección, escrow.",
                path, "/gas-turbines.html", ld) + f"""
<div class="crumbs wrap"><a href="/es/">Inicio</a> / Turbinas de gas</div>
<div class="hero slim"><div class="wrap"><p class="kicker light">Inventario</p><h1>Turbinas de gas usadas en venta</h1><p>Unidades de 60 Hz primero, para las redes de 60 Hz de América.</p></div></div>
<section class="qa"><div class="wrap"><h2>{e(q0)}</h2><p class="answer">{e(ans)}</p></div></section>
<section><div class="wrap"><p class="kicker">Modelos</p><p class="modellinks">{links}</p><div class="ulist">{''.join(row(u) for u in gas_sorted)}</div>
<p class="muted small">Las fichas de las unidades están en inglés. Cada unidad se ofrece en nombre de su dueño y sujeta a venta previa.</p></div></section>
<section class="soft"><div class="wrap"><p class="kicker">Preguntas frecuentes</p>{faq_html(faqs)}
<p>Guía: <a href="/es/como-comprar-una-turbina-de-gas-usada.html">cómo comprar una turbina de gas usada</a>.</p></div></section>
""" + foot()
    (out_dir / "turbinas-de-gas.html").write_text(html, encoding="utf-8", newline="\n")
    written.append(path)

    # --- buyer guide
    path = "/es/como-comprar-una-turbina-de-gas-usada.html"
    q0 = "¿Cómo comprar una turbina de gas usada de forma segura?"
    ans = ("Envíe su requerimiento (potencia, frecuencia, combustible, sitio y plazo), compare ofertas por número de stock y firme una carta de intención para recibir los datos completos e inspeccionar la unidad. "
           "Firme el contrato de compra directamente con el dueño y pague mediante escrow o carta de crédito, nunca por adelantado a un intermediario.")
    steps = [("Requerimiento", "Potencia, frecuencia (50 o 60 Hz), combustible, emisiones permitidas en el sitio, ciclo simple o combinado, plazo y país de destino."),
             ("Oferta", "Recibe una oferta con número de stock y las condiciones del dueño. El precio se envía a consulta."),
             ("Carta de intención (LOI)", "Una declaración firmada y no vinculante con el número de stock, la empresa compradora, el usuario final y el sitio. Abre el acceso a documentos completos e inspección."),
             ("Documentos e inspección", "Hoja de datos, registros de horas y arranques, informes de revisión, alcance de suministro; inspección en sitio por el ingeniero del comprador."),
             ("Contrato y pago", "Contrato de compra directo entre comprador y dueño. Pago mediante escrow o carta de crédito irrevocable acordada entre ambos.")]
    checks = ["Horas equivalentes, arranques y fecha y alcance de la última inspección mayor", "Registros de revisión del fabricante o de un taller autorizado",
              "Frecuencia y tensión del generador frente a la red del sitio", "Sistema de combustión (DLE, inyección de agua) frente a los límites de emisión",
              "Alcance: generador, control, cabina, sistema de combustible, transformador, repuestos", "Desmontaje, transporte de cargas pesadas y aranceles de importación"]
    faqs = [(q0, ans),
            ("¿Qué es una carta de intención (LOI) al comprar una turbina de gas usada?", "Es una declaración firmada y no vinculante en la que el comprador indica el número de stock, la empresa compradora, el usuario final y el sitio, y declara su intención de comprar en las condiciones indicadas. Abre los documentos completos y la inspección; el contrato vinculante viene después, directamente entre comprador y dueño."),
            ("¿Cómo se paga?", "El comprador paga directamente al dueño mediante escrow o una carta de crédito irrevocable acordada entre ambos. Los pagos de compra nunca pasan por las cuentas de LKS 360-SCHREINER LLC."),
            ("¿Qué frecuencia necesito en América Latina?", "La red de su país decide. Según Wikipedia (Mains electricity by country), la mayoría de las redes de Norteamérica, Centroamérica y del norte de Sudamérica funcionan a 60 Hz, mientras que gran parte del sur de Sudamérica funciona a 50 Hz. La hoja de datos de cada unidad indica su frecuencia.")]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": "Cómo comprar una turbina de gas usada", "url": SITE + path, "inLanguage": "es",
         "author": {"@type": "Person", "name": "Lothar Schreiner"}, "publisher": {"@type": "Organization", "name": "LKS 360-SCHREINER LLC"}},
        {"@type": "HowTo", "name": "Cómo comprar una turbina de gas usada", "inLanguage": "es",
         "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(steps)]},
        crumbs([("Inicio", "/es/"), ("Cómo comprar una turbina de gas usada", path)]), faq_ld(faqs)]}
    html = head("Cómo comprar una turbina de gas usada: pasos, carta de intención, pago | LKS 360",
                "Cómo comprar una turbina de gas usada de forma segura: requerimiento, oferta, carta de intención, documentos e inspección, contrato directo con el dueño y pago por escrow o carta de crédito.",
                path, "/buying-used-gas-turbines.html", ld) + f"""
<div class="crumbs wrap"><a href="/es/">Inicio</a> / Cómo comprar</div>
<div class="hero slim"><div class="wrap"><p class="kicker light">Guía</p><h1>Cómo comprar una turbina de gas usada</h1><p>Pasos, documentos y controles que protegen al comprador.</p></div></div>
<section class="qa"><div class="wrap"><h2>{e(q0)}</h2><p class="answer">{e(ans)}</p></div></section>
<section><div class="wrap legal"><h2>Paso a paso</h2><ol>{''.join(f'<li><b>{e(n)}:</b> {e(t)}</li>' for n, t in steps)}</ol>
<h2>Qué revisar antes de comprar</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in checks)}</ul>
<h2>Preguntas frecuentes</h2>{faq_html(faqs[1:])}
<p>Modelos de 60 Hz y doble frecuencia: {links}.</p></div></section>
<div class="cta"><h2>¿Busca una turbina de gas?</h2><p>Envíe potencia, frecuencia, combustible y país de destino.</p><a class="btn alt" href="mailto:{MAIL}">Enviar requerimiento</a> <a class="btn wa" href="{WA}">WhatsApp</a></div>
""" + foot()
    (out_dir / "como-comprar-una-turbina-de-gas-usada.html").write_text(html, encoding="utf-8", newline="\n")
    written.append(path)

    # --- home
    path = "/es/"
    q0 = "¿Qué es LKS 360-SCHREINER LLC?"
    ans = (f"LKS 360-SCHREINER LLC es un corredor independiente de turbinas de gas, turbinas de vapor y grupos electrógenos usados y excedentes, constituido como sociedad de responsabilidad limitada en St. Petersburg, Florida. "
           f"Publica {len(UNITS)} unidades en nombre de sus dueños en lks360.com, filtra a los compradores con carta de intención y el contrato se firma directamente entre comprador y dueño.")
    faqs = [(q0, ans), faqs[1], ("¿En qué idioma están las fichas de las unidades?", "Las fichas de las unidades están en inglés; las guías y las páginas de modelos de 60 Hz están también en español. Puede escribirnos en español.")]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": "LKS 360-SCHREINER LLC: turbinas de gas usadas para América Latina", "url": SITE + path, "inLanguage": "es"},
        {"@type": "Organization", "name": "LKS 360-SCHREINER LLC", "url": SITE + "/"}, faq_ld(faqs)]}
    html = head("Turbinas de gas usadas para América Latina: 60 Hz, corredor independiente | LKS 360",
                f"Corredor independiente con sede en Florida: {len(UNITS)} turbinas de gas, turbinas de vapor y grupos electrógenos usados con número de stock. Unidades de 60 Hz para las redes de 60 Hz de América.",
                path, "/", ld) + f"""
<div class="hero"><div class="wrap"><p class="kicker light">Corredor independiente · Florida, EE. UU.</p><h1>Turbinas de gas usadas para América Latina</h1>
<p>Turbinas de gas, turbinas de vapor y grupos electrógenos usados y excedentes, ofrecidos en nombre de sus dueños. Unidades de 60 Hz para las redes de 60 Hz de América.</p>
<p><a class="btn" href="/es/turbinas-de-gas.html">Ver turbinas de gas</a> <a class="btn wa" href="{WA}">WhatsApp</a></p></div></div>
<section class="qa"><div class="wrap"><h2>{e(q0)}</h2><p class="answer">{e(ans)}</p></div></section>
<section><div class="wrap"><p class="kicker">Modelos</p><h2>Modelos con relevancia para 60 Hz</h2><p class="modellinks">{links}</p>
<h2>Cómo trabajamos</h2><ol><li>Envíe su requerimiento: potencia, frecuencia, combustible y país.</li><li>Recibe una oferta con número de stock y las condiciones del dueño.</li><li>Con su carta de intención: datos completos e inspección.</li><li>Contrato de compra directo con el dueño; pago por escrow o carta de crédito.</li></ol>
<p>Guía: <a href="/es/como-comprar-una-turbina-de-gas-usada.html">cómo comprar una turbina de gas usada</a>. Inventario completo (inglés): <a href="/inventory.html">inventory</a>.</p></div></section>
<section class="soft"><div class="wrap"><p class="kicker">Preguntas frecuentes</p>{faq_html(faqs)}</div></section>
""" + foot()
    (out_dir / "index.html").write_text(html, encoding="utf-8", newline="\n")
    written.append(path)
    return written
