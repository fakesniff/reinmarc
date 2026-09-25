# Website-papa

## Doel
Nieuwe versie van reinmarc.nl (schoonmaakbedrijf Reinmarc, Hardegarijp) als statische website, ter vervanging van de kapotte WordPress-site. Hosting blijft bij Flexwebhosting (DirectAdmin).

## Huidige status
- Oude site (WordPress 5.8, thema Twenty Twelve) gaf sinds 25-09-2026 een "kritieke fout" (HTTP 500).
- Nieuwe statische site staat in `site/` en ziet er hetzelfde uit als de oude. Online sinds 25-09-2026 (geüpload als zip via DirectAdmin-bestandsbeheer, uploadlimiet 10 MB).
- Grote foto's verkleind naar max. 1280 px (JPEG-kwaliteit 72) om onder de uploadlimiet te blijven.

## Opbouw
- `build.py` maakt de HTML-pagina's in `site/`. Teksten aanpassen: in `build.py`, daarna `python3 build.py`.
- `site/css/style.css`: ongewijzigd Twenty Twelve-thema. `site/css/extra.css`: aanvullingen.
- `site/wp-content/uploads/`: originele foto's (zelfde paden als vroeger, zodat oude links blijven werken).
- `site/.htaccess`: https, oude `?page_id=`-links doorsturen, 404-pagina.
- Lokaal bekijken: `cd site && python3 -m http.server 8765` en open http://localhost:8765/

## Nieuwe vormgeving (in ontwikkeling)
- Map `nieuw/`, gemaakt met `build_nieuw.py`. Zelfde pagina's, URL's, teksten, foto's en contactgegevens; nieuwe look.
- Interactief: ramenwisser die het raam schoonveegt (zelf verder vegen kan ook), zeepbellen, voor/na-knoppen, osmose-proefje (leidingwater vs osmosewater), fotoviewer, vaste bel/WhatsApp-balk op mobiel. Respecteert "minder beweging".
- Lokaal bekijken: `cd nieuw && python3 -m http.server 8766` en open http://localhost:8766/
- Nog niet live. Live zetten = inhoud van `nieuw/` uploaden naar `public_html` (zip moet < 10 MB).

## Belangrijke beslissingen
- Geen WordPress meer: geen updates of onderhoud nodig, veiliger.
- Uiterlijk en teksten 1-op-1 overgenomen (wens eigenaar). Smalle inhoudskolom op binnenpagina's is bewust gelijk gehouden aan het origineel.
- Contactformulier werkte al niet meer; vervangen door knoppen voor bellen, WhatsApp en mail.
- Lettertype Open Sans lokaal meegeleverd (geen Google Fonts, i.v.m. privacy).
- 5 portfoliofoto's (IMG_0253, IMG_0254, marcels-fotos-S2-049/076/079) bestonden niet meer op de server of in het archief en zijn weggelaten.

## Volgende stappen
1. Back-up van de oude WordPress-site (in map `backups` op de server) ook lokaal bewaren.
2. Bij wijzigingen: `python3 build.py`, daarna gewijzigde bestanden uploaden naar `domains/reinmarc.nl/public_html`.
