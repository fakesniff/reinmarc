import os

SITE = "/Users/emielveenstra/AI-projecten/Website-papa/site"
U = "/wp-content/uploads"

MENU = [
    ("/", "Home", []),
    ("/osmose-glasbewassing/", "Osmose glasbewassing", []),
    ("/portfolio/", "Portfolio", []),
    ("/contact/", "Over ons", [("/contact/27-2/", "Contact")]),
]


def menu_html(current):
    out = []
    for href, label, children in MENU:
        cls = ["page_item"]
        if children:
            cls.append("page_item_has_children")
        if href == current:
            cls.append("current_page_item")
        aria = ' aria-current="page"' if href == current else ""
        li = f'<li class="{" ".join(cls)}"><a href="{href}"{aria}>{label}</a>'
        if children:
            sub = []
            for ch, cl in children:
                c = "page_item current_page_item" if ch == current else "page_item"
                a = ' aria-current="page"' if ch == current else ""
                sub.append(f'\t<li class="{c}"><a href="{ch}"{a}>{cl}</a></li>')
            li += "\n<ul class=\"children\">\n" + "\n".join(sub) + "\n</ul>\n"
        li += "</li>"
        out.append(li)
    return "\n".join(out)


def page(path, title, description, h1, body, home=False, out_file=None):
    body_cls = "home template-front-page" if home else "page"
    sidebar = ""
    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://reinmarc.nl{path}">
<meta property="og:locale" content="nl_NL">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://reinmarc.nl{path}">
<meta property="og:site_name" content="Schoonmaakbedrijf Reinmarc uit Hardegarijp">
<meta property="og:image" content="https://reinmarc.nl{U}/2013/02/contact_button.jpeg">
<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="/css/extra.css">
</head>

<body class="{body_cls} custom-background custom-font-enabled single-author">
<div id="page" class="hfeed site">
	<header id="masthead" class="site-header">
		<div class="site-branding">
			<p class="site-title"><a href="/" title="Schoonmaakbedrijf Reinmarc uit Hardegarijp" rel="home">Schoonmaakbedrijf Reinmarc uit Hardegarijp</a></p>
			<p class="site-description">Schoonmaken en meer….</p>
		</div>

		<nav id="site-navigation" class="main-navigation" aria-label="Hoofdmenu">
			<button class="menu-toggle" aria-expanded="false">Menu</button>
			<a class="assistive-text" href="#content">Spring naar inhoud</a>
			<div class="nav-menu"><ul class="nav-menu">
{menu_html(path)}
</ul></div>
		</nav>

		<a href="/"><img src="{U}/2013/06/cropped-header.png" class="header-image" width="1000" height="239" alt="Schoonmaakbedrijf Reinmarc uit Hardegarijp"></a>
	</header>

	<div id="main" class="wrapper">
	<div id="primary" class="site-content">
		<main id="content">
	<article class="page type-page hentry">
		<header class="entry-header">
			<h1 class="entry-title">{h1}</h1>
		</header>

		<div class="entry-content">
{body}
		</div>
	</article>
		</main>
	</div>
{sidebar}	</div>
	<footer id="colophon">
		<div class="site-info">
			&copy; Reinmarc &middot; Hardegarijp &middot; <a href="tel:+31611757767">06-11757767</a>
		</div>
	</footer>
</div>

<script src="/js/navigation.js"></script>
</body>
</html>
"""
    if out_file:
        html = html.replace(f'<link rel="canonical" href="https://reinmarc.nl{path}">', '<meta name="robots" content="noindex">')
    out = os.path.join(SITE, out_file or os.path.join(path.strip("/"), "index.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out)


# ---------- Home ----------
page(
    "/",
    "Schoonmaken en meer... Reinmarc uit Hardegarijp!",
    "Schoonmaken en meer... Bij schoonmaakbedrijf Reinmarc kunt u terecht voor diverse schoonmaakwerkzaamheden.",
    "Welkom bij Reinmarc",
    f"""<h2 class="lead"><strong>Schoonmaken en meer….</strong></h2>
<p>Hieronder een selectie van onze werkzaamheden:</p>
<ul>
<li>Complete schoonmaak van uw woning buitenom.</li>
<li>Reinigen van dakgoten</li>
<li>Schoonmaken van schilderwerk/kunststof</li>
<li>Schoonmaken van dakkapellen</li>
</ul>
<p>Bovenstaande werkzaamheden kunnen wij bij u thuis uitvoeren maar ook als u een winkel of kantoorpand heeft kunt u bij ons terecht.</p>
<p>Zoals u ziet is er van alles mogelijk.</p>
<p><a href="/contact/27-2/"><img class="aligncenter" title="Klik hier om direct contact op te nemen!" src="{U}/2013/02/contact_button.jpeg" alt="Neem contact op" width="199" height="149"></a></p>""",
    home=True,
)

# ---------- Osmose ----------
page(
    "/osmose-glasbewassing/",
    "Osmose glasbewassing - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Streeploos schone ramen met osmose glasbewassing en het telewash systeem van Reinmarc uit Hardegarijp.",
    "Osmose glasbewassing",
    f"""<p>De methode van Osmose glasbewassing maakt gebruik van puur osmosewater voor een streeploos oppervlak. Osmose is een proces waarbij een vloeistof, waarin stoffen zijn opgelost, door een zogenaamd halfdoorlatend membraam stroomt, dat wel de vloeistof doorlaat maar niet de opgeloste stoffen. Hierdoor krijg je een zuivere vloeistof. Bij de verdamping van gewoon leidingwater blijven de opgeloste zouten achter waardoor je strepen krijgt. Omdat deze in osmosewater niet meer aanwezig zijn krijg je een streeploos resultaat. Osmosewater heeft een bijzonder reinigend vermogen waardoor gebruik van schoonmaakmiddelen (dus niet milieubelastend) niet nodig is. Dit maakt telescoop glasbewassing geschikt voor het gebruik op alle oppervlakten. Dit osmosewater wordt door onszelf gefilterd en is dus altijd op voorraad.</p>
<p>Wij gebruiken een telewash systeem die het mogelijk maakt om hoge en moeilijk bereikbaar glaswerk te reinigen. Ook is dit systeem uitermate geschikt voor het reinigen van gevelbeplating, schilderwerk enzovoort. Het water is op locatie te verwarmen, immers warm water reinigt nu eenmaal beter dan koud water.</p>
<p class="gallery"><img src="{U}/2015/03/fotos-marcel-26-08-2013-450-225x300.jpg" alt="Glasbewassing met het telewash systeem" width="225" height="300" loading="lazy"> <a href="{U}/2015/03/stp-Hardegarijp3.jpg"><img src="{U}/2015/03/stp-Hardegarijp3-300x225.jpg" alt="Osmose glasbewassing in Hardegarijp" width="300" height="225" loading="lazy"></a></p>""",
)

# ---------- Portfolio ----------
# (bestandsnaam zonder .jpg, breedte, hoogte van de thumbnail, heeft grote versie)
PHOTOS = [
    ("20130918_122827_1", 300, 225, True),
    ("20130919_135325", 300, 225, True),
    ("20131002_153401", 300, 225, True),
    ("20131002_153406", 300, 225, True),
    ("20131107_114012", 300, 225, True),
    ("20140115_122947", 300, 225, True),
    ("20140115_130623", 300, 225, True),
    ("20140314_094442", 225, 300, True),
    ("20140319_121735", 300, 225, True),
    ("20140319_132018", 225, 300, True),
    ("20140121_104608", 300, 225, True),
    ("20140121_104616", 300, 225, True),
    ("20140326_144034", 300, 225, True),
    ("20140326_153401", 300, 225, True),
    ("20140514_094347", 225, 300, True),
    ("20140515_135720", 225, 300, True),
    ("20140616_122140", 225, 300, True),
    ("20140617_133257", 300, 225, True),
    ("20140703_121429", 225, 300, True),
    ("20140703_1147410", 225, 300, True),
    ("IMG_0012", 300, 225, True),
    ("IMG_0249", 300, 225, True),
    ("IMG_0250", 300, 225, True),
    ("IMG_0251", 300, 225, True),
    ("IMG_0255", 225, 300, True),
    ("IMG_0188", 300, 224, True),
    ("marcels-fotos-S2-217", 225, 300, True),
    ("stp-Hardegarijp4", 300, 225, False),
    ("stp-Hardegarijp3", 300, 225, True),
    ("fotos-marcel-26-08-2013-450", 225, 300, False),
    ("fotos-marcel-26-08-2013-449", 225, 300, True),
]

items = []
for i, (name, w, h, big) in enumerate(PHOTOS, 1):
    thumb = f"{U}/2015/03/{name}-{w}x{h}.jpg"
    assert os.path.exists(SITE + thumb), thumb
    img = f'<img src="{thumb}" alt="Foto van ons werk {i}" width="{w}" height="{h}" loading="lazy">'
    if big:
        full = f"{U}/2015/03/{name}.jpg"
        assert os.path.exists(SITE + full), full
        img = f'<a href="{full}">{img}</a>'
    items.append(img)

page(
    "/portfolio/",
    "Portfolio - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Foto's van schoonmaakwerk door Reinmarc uit Hardegarijp.",
    "Portfolio",
    '<p class="gallery">\n' + "\n".join(items) + "\n</p>",
)

# ---------- Over ons ----------
page(
    "/contact/",
    "Over ons - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Reinmarc is in 2013 opgericht door Marcel Veenstra en staat voor kwaliteit en betrouwbaarheid.",
    "Over ons",
    """<h4><strong>Reinmarc is een jong bedrijf dat op 1 februari 2013 is opgericht door Marcel Veenstra. Reinmarc staat voor kwaliteit, betrouwbaarheid.</strong></h4>
<p><strong>Hoe ga ik te werk:</strong><br>
Als u ons belt kom ik langs en gaan u en ik samen kijken wat er moet gebeuren.<br>
Ik maak thuis een offerte en ik kom dan bij u langs om deze samen door te nemen, bij het akkoord gaan van deze offerte plan ik de werkzaamheden voor u in op een dag en tijdstip die u het best uitkomt.<br>
Ook is het voor mij een uitdaging om een netwerk op te bouwen en deze te onderhouden door middel van goede afspraken maken en een marktconform tarief te vragen.</p>
<p>Mijn motto: <strong>Afspraak is Afspraak of het nu gaat om een kleine of een grote klus.</strong></p>
<p>Op de pagina <a href="/portfolio/">Portfolio</a> vindt u een klein overzicht door middel van foto’s die genomen zijn voor en na de klus.</p>
<p>Mocht u enthousiast zijn geworden na het lezen van mijn site en heeft u een klus voor me, <a href="/contact/27-2/">neem dan contact met me op</a>.</p>
<p>Met vriendelijke groet,</p>
<p><strong>Reinmarc.nl</strong></p>
<p><strong>Marcel Veenstra<br>
Kobbeflecht 70<br>
9254AH Hardegarijp<br>
Tel: <a href="tel:+31611757767">06-11757767</a><br>
Email: <a href="mailto:info@reinmarc.nl">info@reinmarc.nl</a></strong></p>""",
)

# ---------- Contact ----------
page(
    "/contact/27-2/",
    "Contact - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Neem contact op met Reinmarc: bel of WhatsApp 06-11757767 of mail naar info@reinmarc.nl.",
    "Contact",
    """<p>Stuur uw gegevens naar info@reinmarc.nl of bel of WhatsApp ons op 06-11757767.</p>
<ul class="contact-options">
<li><a href="tel:+31611757767">Bel 06-11757767</a></li>
<li><a href="https://wa.me/31611757767">WhatsApp ons</a></li>
<li><a href="mailto:info@reinmarc.nl">Mail info@reinmarc.nl</a></li>
</ul>
<p><strong>Reinmarc</strong><br>
Marcel Veenstra<br>
Kobbeflecht 70<br>
9254AH Hardegarijp</p>""",
)

# ---------- Niet gevonden (404) ----------
page(
    "/404.html",
    "Pagina niet gevonden - Schoonmaakbedrijf Reinmarc uit Hardegarijp",
    "Deze pagina bestaat niet (meer).",
    "Pagina niet gevonden",
    """<p>Deze pagina bestaat niet (meer). Ga naar de <a href="/">homepage</a> of <a href="/contact/27-2/">neem contact op</a>.</p>""",
    out_file="404.html",
)
