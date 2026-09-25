"""Maakt de nieuwe versie van reinmarc.nl in de map nieuw/.

Gebruik: python3 build_nieuw.py
Teksten, foto's en contactgegevens zijn gelijk aan de oude site; alleen de vormgeving is nieuw.
"""
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nieuw")
W = "/img/werk"
FULL = "/wp-content/uploads/2015/03"

PHONE = "06-11757767"
PHONE_LINK = "tel:+31611757767"
WA_LINK = "https://wa.me/31611757767"
EMAIL = "info@reinmarc.nl"

NAV = [
    ("/", "Home"),
    ("/osmose-glasbewassing/", "Osmose glasbewassing"),
    ("/portfolio/", "Portfolio"),
    ("/contact/", "Over ons"),
    ("/contact/27-2/", "Contact"),
]

# ---------- Iconen ----------

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.7 17.8L0 24l6.3-1.7A11.8 11.8 0 0 0 24 12c0-3.2-1.2-6.1-3.6-8.4z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
    "arrow": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "swipe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11V5.5a1.5 1.5 0 0 1 3 0V10m0 0V8.5a1.5 1.5 0 0 1 3 0V11m0-1a1.5 1.5 0 0 1 3 0v3.5a6.5 6.5 0 0 1-6.5 6.5h-.8a6 6 0 0 1-4.6-2.2L4.3 15a1.6 1.6 0 0 1 2.4-2.1L9 15"/></svg>',
    "copy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
    "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
    "next": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
}

# Logo: ramenwisser in een druppel
BRAND_MARK = """<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
<circle cx="20" cy="20" r="20" fill="#1d64a8"/>
<rect x="9" y="11" width="22" height="5" rx="1.5" fill="#dfeef5"/>
<rect x="9" y="15.5" width="22" height="2.4" rx="1" fill="#0f2a3d"/>
<rect x="17.5" y="17" width="5" height="14" rx="2.5" fill="#ffc83d"/>
</svg>"""

# Ramenwisser (trekker) voor de animatie; rubber staat rechts.
SQUEEGEE = """<svg class="squeegee" viewBox="0 0 62 100" aria-hidden="true">
<rect x="2" y="44" width="34" height="12" rx="6" fill="#ffc83d"/>
<rect x="2" y="44" width="34" height="4" rx="2" fill="#ffe08a"/>
<rect x="29" y="41" width="7" height="18" rx="2" fill="#e8ac12"/>
<rect x="36" y="2" width="10" height="96" rx="3" fill="#9fb3bf"/>
<rect x="38" y="2" width="2.5" height="96" fill="#dce7ed"/>
<rect x="46" y="4" width="4" height="92" rx="2" fill="#1b2a33"/>
</svg>"""


# Uitzicht door het raam op de homepage: Fries weiland met boerderij.
def cow(x, y, s=1.0, flip=False):
    f = -1 if flip else 1
    return f"""<g transform="translate({x} {y}) scale({s * f} {s})">
<rect x="-3" y="10" width="2" height="8" fill="#2b2b2b"/><rect x="2" y="10" width="2" height="8" fill="#2b2b2b"/>
<rect x="15" y="10" width="2" height="8" fill="#2b2b2b"/><rect x="20" y="10" width="2" height="8" fill="#2b2b2b"/>
<rect x="-5" y="0" width="29" height="13" rx="5" fill="#fbfbf7"/>
<path d="M2 0h9l-2 8H1z" fill="#1f1f1f"/><ellipse cx="17" cy="5" rx="4" ry="3.5" fill="#1f1f1f"/>
<rect x="22" y="-4" width="9" height="9" rx="3" fill="#1f1f1f"/><rect x="27" y="1" width="5" height="4" rx="2" fill="#e9b8a8"/>
</g>"""


VIEW_SVG = f"""<svg class="view" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs>
<linearGradient id="v-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb2e3"/><stop offset="1" stop-color="#cfeaf7"/></linearGradient>
<linearGradient id="v-grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8dc85a"/><stop offset="1" stop-color="#4f9a37"/></linearGradient>
<radialGradient id="v-sun"><stop offset="0" stop-color="#fff6c7"/><stop offset=".45" stop-color="#ffe27a"/><stop offset="1" stop-color="#ffe27a" stop-opacity="0"/></radialGradient>
</defs>
<rect width="400" height="300" fill="url(#v-sky)"/>
<circle cx="330" cy="58" r="46" fill="url(#v-sun)"/>
<g class="cloud c1" fill="#fff"><ellipse cx="70" cy="60" rx="34" ry="13"/><ellipse cx="92" cy="50" rx="22" ry="15"/><ellipse cx="55" cy="52" rx="16" ry="11"/></g>
<g class="cloud c2" fill="#fff" opacity=".9"><ellipse cx="230" cy="36" rx="28" ry="10"/><ellipse cx="246" cy="28" rx="17" ry="12"/></g>
<g class="cloud c3" fill="#fff" opacity=".8"><ellipse cx="160" cy="98" rx="22" ry="7"/><ellipse cx="172" cy="92" rx="13" ry="8"/></g>
<path d="M0 182 q10-14 22-6 q8-16 22-6 q12-10 20 2 q14-8 22 4 L400 180 q-12-14-26-4 q-10-12-24-2 q-12-8-20 4 L400 200 H0z" fill="#3e7a45"/>
<g fill="#2f6a3b"><circle cx="118" cy="166" r="17"/><circle cx="134" cy="158" r="20"/><circle cx="352" cy="166" r="18"/><circle cx="368" cy="158" r="14"/></g>
<rect x="131" y="170" width="4" height="18" fill="#4b3a2a"/>
<rect x="0" y="186" width="400" height="114" fill="url(#v-grass)"/>
<g>
<polygon points="190,180 262,118 334,180" fill="#4d535c"/>
<polygon points="262,118 334,180 318,180" fill="#3c4148"/>
<rect x="196" y="178" width="132" height="34" fill="#a8472f"/>
<rect x="244" y="188" width="26" height="24" fill="#2f6b4a"/>
<path d="M244 188 L270 212 M270 188 L244 212" stroke="#fff" stroke-width="2"/>
<rect x="150" y="168" width="48" height="44" fill="#b4523a"/>
<polygon points="145,170 174,140 203,170" fill="#7d2e22"/>
<g fill="#fff"><rect x="158" y="182" width="12" height="14"/><rect x="178" y="182" width="12" height="14"/><rect x="290" y="190" width="10" height="10"/><rect x="306" y="190" width="10" height="10"/></g>
<g fill="#9fcbe0"><rect x="160" y="184" width="8" height="10"/><rect x="180" y="184" width="8" height="10"/><rect x="292" y="192" width="6" height="6"/><rect x="308" y="192" width="6" height="6"/></g>
</g>
<path d="M0 240 q60-8 120 0 t120 0 t160 -2 v14 q-80 6-160 2 t-120 0 t-120 0z" fill="#5aa9d6"/>
<path d="M20 243 q40-4 80 0 M170 244 q40-4 80 0 M290 242 q40-4 80 0" stroke="#bfe3f5" stroke-width="2" fill="none" stroke-linecap="round"/>
<g stroke="#6b5139" stroke-width="2"><path d="M0 222 H400" stroke-width="1.2"/><path d="M20 214v14M70 214v14M120 214v14M170 214v14M220 214v14M270 214v14M320 214v14M370 214v14"/></g>
{cow(60, 206, 1.0)}
{cow(104, 212, 0.9, True)}
{cow(318, 262, 1.3)}
{cow(250, 270, 1.15, True)}
</svg>"""

def brand(tag="Schoonmaken en meer…"):
    return f"""{BRAND_MARK}
			<span><span class="brand-name">Reinmarc</span><span class="brand-tag">{tag}</span></span>"""


def nav_html(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'\t\t\t\t<li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(items)


def contact_cards():
    return f"""<div class="cta-options">
				<a class="contact-card" href="{PHONE_LINK}">
					<span class="icon">{ICON["phone"]}</span>
					<span><strong>Bel {PHONE}</strong><span>Direct contact</span></span>
					{ICON["arrow"]}
				</a>
				<a class="contact-card is-whatsapp" href="{WA_LINK}">
					<span class="icon">{ICON["whatsapp"]}</span>
					<span><strong>WhatsApp ons</strong><span>{PHONE}</span></span>
					{ICON["arrow"]}
				</a>
				<a class="contact-card" href="mailto:{EMAIL}">
					<span class="icon">{ICON["mail"]}</span>
					<span><strong>Mail {EMAIL}</strong><span>Stuur uw gegevens</span></span>
					{ICON["arrow"]}
				</a>
			</div>"""


def cta_section(sky=True):
    cls = "section section-sky" if sky else "section"
    return f"""
	<section class="{cls}" aria-labelledby="cta-title">
		<div class="wrap cta">
			<div data-reveal>
				<h2 id="cta-title">Neem contact op</h2>
				<p>Stuur uw gegevens naar {EMAIL} of bel of WhatsApp ons op {PHONE}.</p>
				<p>Als u ons belt kom ik langs en gaan u en ik samen kijken wat er moet gebeuren.</p>
			</div>
			<div data-reveal data-reveal-delay="1">
			{contact_cards()}
			</div>
		</div>
	</section>"""


BA_PAIRS = [
    ("IMG_0249", "IMG_0250", "Overkapping"),
    ("20140326_144034", "20140326_153401", "Ramen"),
    ("20140115_122947", "20140115_130623", "Overstek"),
]


def before_after(sky=False):
    items = []
    for i, (before, after, what) in enumerate(BA_PAIRS):
        items.append(f"""			<figure class="ba" data-reveal data-reveal-delay="{i}">
				<div class="ba-frame">
					<span class="ba-label" aria-live="polite">Voor</span>
					<img src="{W}/{before}.jpg" alt="{what} voor het schoonmaken" width="900" height="675" loading="lazy">
					<img class="ba-after" src="{W}/{after}.jpg" alt="{what} na het schoonmaken" width="900" height="675" loading="lazy">
				</div>
				<div class="ba-switch" role="group" aria-label="{what}: voor of na">
					<button type="button" aria-pressed="true">Voor</button>
					<button type="button" aria-pressed="false">Na</button>
				</div>
			</figure>""")
    cls = "section section-sky" if sky else "section"
    return f"""
	<section class="{cls}" aria-labelledby="ba-title">
		<div class="wrap">
			<div class="section-head" data-reveal>
				<h2 id="ba-title">Voor en na</h2>
				<p>Foto’s die genomen zijn voor en na de klus. Klik op de foto of de knoppen om het verschil te zien.</p>
			</div>
			<div class="ba-grid">
{chr(10).join(items)}
			</div>
		</div>
	</section>"""


def motto():
    return """
	<section class="motto" aria-label="Motto">
		<div class="wrap" data-reveal>
			<blockquote>
				<p><span class="wipe-word">Afspraak is Afspraak</span> of het nu gaat om een kleine of een grote klus.</p>
			</blockquote>
			<cite>Marcel Veenstra, Reinmarc</cite>
		</div>
	</section>"""


def page(path, title, description, main, out_file=None):
    canonical = (
        '<meta name="robots" content="noindex">'
        if out_file
        else f'<link rel="canonical" href="https://reinmarc.nl{path}">'
    )
    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{canonical}
<meta name="theme-color" content="#1d64a8">
<meta property="og:locale" content="nl_NL">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://reinmarc.nl{path}">
<meta property="og:site_name" content="Schoonmaakbedrijf Reinmarc uit Hardegarijp">
<meta property="og:image" content="https://reinmarc.nl{W}/fotos-marcel-26-08-2013-449.jpg">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
<a class="skip" href="#inhoud">Naar de inhoud</a>

<header class="site-header">
	<div class="wrap header-inner">
		<a class="brand" href="/" aria-label="Reinmarc, naar de homepage">
			{brand()}
		</a>
		<nav class="main-nav" id="main-nav" aria-label="Hoofdmenu">
			<ul>
{nav_html(path)}
			</ul>
		</nav>
		<a class="btn btn-primary header-call" href="{PHONE_LINK}">{ICON["phone"]} {PHONE}</a>
		<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Menu openen"><span></span></button>
	</div>
</header>

<main id="inhoud">
{main}
</main>

<footer class="site-footer">
	<div class="wrap">
		<div class="footer-grid">
			<div>
				<a class="brand" href="/">
					{brand("Schoonmaakbedrijf uit Hardegarijp")}
				</a>
				<p>Reinmarc staat voor kwaliteit, betrouwbaarheid.</p>
			</div>
			<div>
				<h2>Pagina’s</h2>
				<ul>
{chr(10).join(f'					<li><a href="{h}">{l}</a></li>' for h, l in NAV)}
				</ul>
			</div>
			<div>
				<h2>Contact</h2>
				<address>
					Marcel Veenstra<br>
					Kobbeflecht 70<br>
					9254AH Hardegarijp<br>
					<a href="{PHONE_LINK}">{PHONE}</a><br>
					<a href="mailto:{EMAIL}">{EMAIL}</a>
				</address>
			</div>
		</div>
		<p class="footer-bottom">&copy; Reinmarc.nl</p>
	</div>
</footer>

<div class="mobile-bar">
	<a class="btn btn-primary" href="{PHONE_LINK}">{ICON["phone"]} Bellen</a>
	<a class="btn btn-wa" href="{WA_LINK}">{ICON["whatsapp"]} WhatsApp</a>
</div>

<script src="/js/site.js" defer></script>
</body>
</html>
"""
    # Relatieve links, zodat de site ook in een submap werkt (bijv. de GitHub-voorbeeldlink).
    # De 404-pagina houdt vaste paden: die kan vanaf elke diepte getoond worden.
    if not out_file:
        depth = len([p for p in path.split("/") if p])
        prefix = "../" * depth or "./"
        html = re.sub(r'(href|src)="/', r'\1="' + prefix, html)
    out = os.path.join(OUT, out_file or os.path.join(path.strip("/"), "index.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("geschreven:", os.path.relpath(out, OUT))


# ---------- Home ----------

SERVICES = [
    ("Complete schoonmaak van uw woning buitenom.", "fotos-marcel-26-08-2013-449"),
    ("Reinigen van dakgoten", "20140616_122140"),
    ("Schoonmaken van schilderwerk/kunststof", "20140121_104616"),
    ("Schoonmaken van dakkapellen", "20131002_153401"),
]

services_html = "\n".join(
    f"""				<li class="service" data-reveal data-reveal-delay="{i}">
					<div class="service-img"><img src="{W}/{img}.jpg" alt="" width="900" height="675" loading="lazy"></div>
					<h3>{name}</h3>
				</li>"""
    for i, (name, img) in enumerate(SERVICES)
)

page(
    "/",
    "Schoonmaken en meer... Reinmarc uit Hardegarijp!",
    "Schoonmaken en meer... Bij schoonmaakbedrijf Reinmarc kunt u terecht voor diverse schoonmaakwerkzaamheden.",
    f"""
	<section class="hero">
		<div class="bubbles" aria-hidden="true"></div>
		<div class="wrap hero-grid">
			<div>
				<span class="eyebrow">Welkom bij Reinmarc</span>
				<h1>Schoonmaken en <span class="shine">meer….</span></h1>
				<p class="hero-lead">Bij schoonmaakbedrijf Reinmarc uit Hardegarijp kunt u terecht voor diverse schoonmaakwerkzaamheden.</p>
				<div class="hero-actions">
					<a class="btn btn-primary" href="/contact/27-2/">{ICON["phone"]} Neem contact op</a>
					<a class="btn btn-ghost" href="/portfolio/">Bekijk ons werk</a>
				</div>
			</div>
			<div>
				<div class="window" data-window>
					<div class="window-pane">
						{VIEW_SVG}
						<canvas aria-hidden="true"></canvas>
					</div>
					{SQUEEGEE}
				</div>
				<div class="window-bar">
					<span class="window-hint" aria-live="polite">{ICON["swipe"]}<span></span></span>
					<button type="button" class="link-btn" data-clean>Laat de ramenwisser het doen</button>
					<button type="button" class="link-btn" data-soap hidden>Opnieuw inzepen</button>
				</div>
			</div>
		</div>
	</section>

	<section class="section" aria-labelledby="werk-title">
		<div class="wrap">
			<div class="section-head" data-reveal>
				<h2 id="werk-title">Onze werkzaamheden</h2>
				<p>Hieronder een selectie van onze werkzaamheden:</p>
			</div>
			<ul class="services">
{services_html}
			</ul>
			<div class="services-note" data-reveal>
				<div>
					<p>Bovenstaande werkzaamheden kunnen wij bij u thuis uitvoeren maar ook als u een winkel of kantoorpand heeft kunt u bij ons terecht.</p>
					<p>Zoals u ziet is er van alles mogelijk.</p>
				</div>
				<a class="btn btn-primary" href="/contact/27-2/">Neem contact op</a>
			</div>
		</div>
	</section>
{before_after(sky=True)}
{motto()}
{cta_section(sky=False)}
""",
)

# ---------- Osmose glasbewassing ----------

page(
    "/osmose-glasbewassing/",
    "Osmose glasbewassing - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Streeploos schone ramen met osmose glasbewassing en het telewash systeem van Reinmarc uit Hardegarijp.",
    f"""
	<section class="page-hero">
		<div class="wrap" data-reveal>
			<h1>Osmose glasbewassing</h1>
			<p>De methode van Osmose glasbewassing maakt gebruik van puur osmosewater voor een streeploos oppervlak.</p>
		</div>
	</section>

	<section class="section" aria-labelledby="hoe-title">
		<div class="wrap two-col">
			<div class="prose" data-reveal>
				<h2 id="hoe-title">Wat is osmose?</h2>
				<p>Osmose is een proces waarbij een vloeistof, waarin stoffen zijn opgelost, door een zogenaamd halfdoorlatend membraam stroomt, dat wel de vloeistof doorlaat maar niet de opgeloste stoffen. Hierdoor krijg je een zuivere vloeistof.</p>
				<p>Bij de verdamping van gewoon leidingwater blijven de opgeloste zouten achter waardoor je strepen krijgt. Omdat deze in osmosewater niet meer aanwezig zijn krijg je een streeploos resultaat.</p>
				<p>Osmosewater heeft een bijzonder reinigend vermogen waardoor gebruik van schoonmaakmiddelen (dus niet milieubelastend) niet nodig is. Dit maakt telescoop glasbewassing geschikt voor het gebruik op alle oppervlakten. Dit osmosewater wordt door onszelf gefilterd en is dus altijd op voorraad.</p>
			</div>
			<div class="demo" data-demo data-reveal data-reveal-delay="1">
				<h3>Probeer het zelf</h3>
				<div class="demo-tabs" role="group" aria-label="Kies het water">
					<button type="button" aria-pressed="true">Leidingwater</button>
					<button type="button" aria-pressed="false">Osmosewater</button>
				</div>
				<div class="demo-stage">
					<div class="demo-glass" aria-hidden="true">
						<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice">
							<defs>
								<linearGradient id="d-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f9fd1"/><stop offset="1" stop-color="#a9d6ee"/></linearGradient>
								<linearGradient id="d-grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f8f3a"/><stop offset="1" stop-color="#2f6a2c"/></linearGradient>
								<radialGradient id="d-drop" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".65" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#0a3250" stop-opacity=".38"/></radialGradient>
								<linearGradient id="d-shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
								<filter id="d-soft"><feGaussianBlur stdDeviation=".45"/></filter>
							</defs>
							<rect width="400" height="260" fill="url(#d-sky)"/>
							<path d="M0 150 q14-22 30-8 q12-24 32-8 q16-18 30 0 q18-20 34 2 q14-16 30 0 q16-22 34-4 q14-18 30 2 q16-20 34 0 q18-16 32 4 q14-20 30-2 q16-14 26 6 q12-12 28 4 V260 H0z" fill="#2c5f34"/>
							<rect y="186" width="400" height="74" fill="url(#d-grass)"/>
							<rect class="d-haze" width="400" height="260" fill="#fff" fill-opacity=".14" opacity="0"/>
							<g class="d-trails"></g>
							<g class="d-residue" filter="url(#d-soft)"></g>
							<g class="d-drops"></g>
							<rect class="d-shine" x="-160" y="-40" width="120" height="340" fill="url(#d-shine)" transform="rotate(18)"/>
						</svg>
					</div>
					<div class="demo-lens" aria-hidden="true">
						<svg viewBox="0 0 120 120">
							<defs><clipPath id="d-lens"><circle cx="60" cy="60" r="54"/></clipPath></defs>
							<g clip-path="url(#d-lens)">
								<rect class="lens-bg" width="120" height="120"/>
								<g class="lens-water"></g>
								<g class="lens-salt"></g>
							</g>
							<circle cx="60" cy="60" r="54" fill="none" stroke="#fff" stroke-width="6"/>
						</svg>
						<span>Druppel onder de loep</span>
					</div>
				</div>
				<ul class="demo-legend" aria-hidden="true">
					<li><span class="dot is-water"></span>Water</li>
					<li class="legend-salt"><span class="dot is-salt"></span>Opgeloste zouten</li>
				</ul>
				<div class="demo-foot">
					<p class="demo-result" aria-live="polite"></p>
					<button type="button" class="btn btn-primary" data-dry>Laat het raam drogen</button>
				</div>
			</div>
		</div>
	</section>

	<section class="section section-sky" aria-labelledby="tele-title">
		<div class="wrap two-col">
			<div class="photo-pair" data-reveal>
				<img src="{W}/fotos-marcel-26-08-2013-450.jpg" alt="Glasbewassing met het telewash systeem" width="225" height="300" loading="lazy">
				<a href="{FULL}/stp-Hardegarijp3.jpg"><img class="rounded" src="{W}/stp-Hardegarijp3.jpg" alt="Osmose glasbewassing in Hardegarijp" width="900" height="675" loading="lazy"></a>
			</div>
			<div class="prose" data-reveal data-reveal-delay="1">
				<h2 id="tele-title">Het telewash systeem</h2>
				<p>Wij gebruiken een telewash systeem die het mogelijk maakt om hoge en moeilijk bereikbaar glaswerk te reinigen. Ook is dit systeem uitermate geschikt voor het reinigen van gevelbeplating, schilderwerk enzovoort.</p>
				<p>Het water is op locatie te verwarmen, immers warm water reinigt nu eenmaal beter dan koud water.</p>
			</div>
		</div>
	</section>
{cta_section(sky=False)}
""",
)

# ---------- Portfolio ----------

PHOTOS = [
    ("20130918_122827_1", 900, 675), ("20130919_135325", 900, 675),
    ("20131002_153401", 900, 675), ("20131002_153406", 900, 675),
    ("20131107_114012", 900, 675), ("20140115_122947", 900, 675),
    ("20140115_130623", 900, 675), ("20140314_094442", 675, 900),
    ("20140319_121735", 900, 675), ("20140319_132018", 675, 900),
    ("20140121_104608", 900, 675), ("20140121_104616", 900, 675),
    ("20140326_144034", 900, 675), ("20140326_153401", 900, 675),
    ("20140514_094347", 675, 900), ("20140515_135720", 675, 900),
    ("20140616_122140", 675, 900), ("20140617_133257", 900, 675),
    ("20140703_121429", 675, 900), ("20140703_1147410", 675, 900),
    ("IMG_0012", 900, 675), ("IMG_0249", 900, 675), ("IMG_0250", 900, 675),
    ("IMG_0251", 900, 675), ("IMG_0255", 675, 900), ("IMG_0188", 900, 672),
    ("marcels-fotos-S2-217", 675, 900), ("stp-Hardegarijp4", 300, 225),
    ("stp-Hardegarijp3", 900, 675), ("fotos-marcel-26-08-2013-450", 225, 300),
    ("fotos-marcel-26-08-2013-449", 675, 900),
]

gallery = []
for i, (name, w, h) in enumerate(PHOTOS, 1):
    src = f"{W}/{name}.jpg"
    full = f"{FULL}/{name}.jpg"
    assert os.path.exists(OUT + src), src
    if not os.path.exists(OUT + full):
        full = src
    gallery.append(
        f'\t\t\t\t<a href="{full}"><img src="{src}" alt="Foto van ons werk {i}" width="{w}" height="{h}" loading="lazy"></a>'
    )

page(
    "/portfolio/",
    "Portfolio - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Foto's van schoonmaakwerk door Reinmarc uit Hardegarijp.",
    f"""
	<section class="page-hero">
		<div class="wrap" data-reveal>
			<h1>Portfolio</h1>
			<p>Een klein overzicht door middel van foto’s die genomen zijn voor en na de klus. Klik op een foto om hem groot te bekijken.</p>
		</div>
	</section>
{before_after(sky=False)}
	<section class="section section-sky" aria-labelledby="fotos-title">
		<div class="wrap">
			<div class="section-head" data-reveal>
				<h2 id="fotos-title">Alle foto’s</h2>
			</div>
			<div class="gallery">
{chr(10).join(gallery)}
			</div>
		</div>
	</section>

	<dialog class="lightbox" aria-label="Foto bekijken">
		<figure>
			<img src="" alt="">
			<figcaption></figcaption>
		</figure>
		<button type="button" class="lb-btn lb-close" aria-label="Sluiten">{ICON["close"]}</button>
		<button type="button" class="lb-btn lb-prev" aria-label="Vorige foto">{ICON["prev"]}</button>
		<button type="button" class="lb-btn lb-next" aria-label="Volgende foto">{ICON["next"]}</button>
	</dialog>
{cta_section(sky=False)}
""",
)

# ---------- Over ons ----------

page(
    "/contact/",
    "Over ons - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Reinmarc is in 2013 opgericht door Marcel Veenstra en staat voor kwaliteit en betrouwbaarheid.",
    f"""
	<section class="page-hero">
		<div class="wrap" data-reveal>
			<h1>Over ons</h1>
			<p>Reinmarc is een jong bedrijf dat op 1 februari 2013 is opgericht door Marcel Veenstra. Reinmarc staat voor kwaliteit, betrouwbaarheid.</p>
		</div>
	</section>

	<section class="section" aria-labelledby="werkwijze-title">
		<div class="wrap">
			<div class="section-head" data-reveal>
				<h2 id="werkwijze-title">Hoe ga ik te werk</h2>
			</div>
			<ol class="steps">
				<li data-reveal>
					<h3>U belt</h3>
					<p>Als u ons belt kom ik langs en gaan u en ik samen kijken wat er moet gebeuren.</p>
				</li>
				<li data-reveal data-reveal-delay="1">
					<h3>Offerte</h3>
					<p>Ik maak thuis een offerte en ik kom dan bij u langs om deze samen door te nemen.</p>
				</li>
				<li data-reveal data-reveal-delay="2">
					<h3>Inplannen</h3>
					<p>Bij het akkoord gaan van deze offerte plan ik de werkzaamheden voor u in op een dag en tijdstip die u het best uitkomt.</p>
				</li>
			</ol>
			<p class="prose" style="margin-top:32px" data-reveal>Ook is het voor mij een uitdaging om een netwerk op te bouwen en deze te onderhouden door middel van goede afspraken maken en een marktconform tarief te vragen.</p>
		</div>
	</section>
{motto()}
	<section class="section" aria-labelledby="groet-title">
		<div class="wrap two-col">
			<div class="prose" data-reveal>
				<h2 id="groet-title">Een klus voor me?</h2>
				<p>Op de pagina <a href="/portfolio/">Portfolio</a> vindt u een klein overzicht door middel van foto’s die genomen zijn voor en na de klus.</p>
				<p>Mocht u enthousiast zijn geworden na het lezen van mijn site en heeft u een klus voor me, <a href="/contact/27-2/">neem dan contact met me op</a>.</p>
				<p><a class="btn btn-primary" href="/contact/27-2/">Neem contact op</a></p>
			</div>
			<div class="signature" data-reveal data-reveal-delay="1">
				<span class="avatar" aria-hidden="true">MV</span>
				<div>
					<p>Met vriendelijke groet,</p>
					<address>
						<strong>Marcel Veenstra</strong><br>
						Reinmarc.nl<br>
						Kobbeflecht 70<br>
						9254AH Hardegarijp<br>
						Tel: <a href="{PHONE_LINK}">{PHONE}</a><br>
						Email: <a href="mailto:{EMAIL}">{EMAIL}</a>
					</address>
				</div>
			</div>
		</div>
	</section>
""",
)

# ---------- Contact ----------

page(
    "/contact/27-2/",
    "Contact - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Neem contact op met Reinmarc: bel of WhatsApp 06-11757767 of mail naar info@reinmarc.nl.",
    f"""
	<section class="page-hero">
		<div class="wrap" data-reveal>
			<h1>Contact</h1>
			<p>Stuur uw gegevens naar {EMAIL} of bel of WhatsApp ons op {PHONE}.</p>
		</div>
	</section>

	<section class="section" aria-label="Contactmogelijkheden">
		<div class="wrap two-col">
			<div data-reveal>
				{contact_cards()}
				<div class="copy-row">
					<button type="button" class="link-btn" data-copy="{EMAIL}">Kopieer e-mailadres</button>
					<span class="copy-msg" role="status">Gekopieerd</span>
				</div>
			</div>
			<div class="address-card" data-reveal data-reveal-delay="1">
				<h2>Reinmarc</h2>
				<address>
					Marcel Veenstra<br>
					Kobbeflecht 70<br>
					9254AH Hardegarijp
				</address>
			</div>
		</div>
	</section>
""",
)

# ---------- Niet gevonden ----------

page(
    "/404.html",
    "Pagina niet gevonden - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Deze pagina bestaat niet (meer).",
    """
	<section class="page-hero">
		<div class="wrap">
			<h1>Pagina niet gevonden</h1>
			<p>Deze pagina bestaat niet (meer). Ga naar de <a href="/">homepage</a> of <a href="/contact/27-2/">neem contact op</a>.</p>
		</div>
	</section>
""",
    out_file="404.html",
)
