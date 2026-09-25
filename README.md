# Reinmarc.nl

Website van schoonmaakbedrijf Reinmarc uit Hardegarijp.

- `nieuw/`: de nieuwe vormgeving (nog niet live). Voorbeeld: https://fakesniff.github.io/reinmarc/
- `site/`: de huidige live versie op reinmarc.nl (de oude look, zonder WordPress).

## Aanpassen

De pagina's worden gemaakt met een klein Python-script:

```sh
python3 build_nieuw.py   # maakt nieuw/
python3 build.py         # maakt site/
```

Lokaal bekijken:

```sh
cd nieuw && python3 -m http.server 8766
```

Open daarna http://localhost:8766/

## Live zetten

Upload de inhoud van `nieuw/` (inclusief `.htaccess`) naar `domains/reinmarc.nl/public_html` via het bestandsbeheer van Flexwebhosting.
