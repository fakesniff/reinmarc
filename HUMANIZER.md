# Humanizer

Aparte review-pass voor zichtbare output. Doel: tekst en ontwerp voelen menselijk en passend bij dit project, niet generiek AI-generated.

Dit bestand heeft twee delen: universele regels (voor elk project) en onderaan de projectcontext (alleen voor dit project). Bij conflict gaat de projectcontext voor.

## Wanneer

Verplicht als een wijziging zichtbare gebruikersoutput raakt: websites, apps, UI/layout, styling, copy, buttons, formulieren, foutmeldingen, empty states, onboarding, navigatie, dashboards, publieke documentatie, e-mails/templates die bij het product horen.

Niet nodig bij puur technische wijzigingen zonder zichtbare output.

## Werkwijze

Humanization gebeurt NA de functionele implementatie. **Functionaliteit mag tijdens de pass niet onbedoeld veranderen.**

1. Bouw de functioneel correcte versie.
2. Bepaal de projectidentiteit (product, doelgroep, tone of voice, kleuren, typografie, designrichting). Begin bij de projectcontext onderaan en het betreffende scherm; lees `docs/PROJECT.md`, README, brand assets of andere schermen alleen als dat nodig is. Ontbreekt duidelijke context? Volg de bestaande stijl en maak geen grote creatieve aannames.
3. Bekijk de daadwerkelijke output. Als screenshot/browsertesting beschikbaar is, beoordeel de gerenderde interface, niet alleen de broncode.
4. Controleer tekst en ontwerp met de regels hieronder.
5. Verwijder elementen zonder functie of duidelijke ontwerpreden en corrigeer AI-patronen.
6. Controleer opnieuw dat de functionaliteit werkt.

## Tekst

Let op:
- onnatuurlijke of voorspelbare AI-zinsconstructies (bijv. "It's not just X, it's Y", "Whether you're...", "Unlock/Discover/Elevate...", "Seamless", "Next level")
- overdreven marketingtaal, corporate/SaaS-copy zonder reden, clichés
- overuitleg, onnatuurlijke herhaling, geforceerd enthousiasme
- elke tekst met dezelfde zinsbouw
- tekst die grammaticaal klopt maar niet klinkt zoals een mens hem zou schrijven

Voorkeur: natuurlijk, helder, concreet, passend bij de doelgroep, passende zinslengte, normale interpunctie.

Vermijd onnodige em dashes (—) en en dashes (–) als stijlmiddel; meestal werkt een punt, komma, dubbele punt of haakjes beter. Een gewoon koppelteken (-) in woorden mag.

Maak tekst niet kunstmatig informeel of foutief om menselijk te lijken.

## Ontwerp

Let op generieke AI-designpatronen, tenzij er een bewuste reden voor is:
- standaard paarse/blauwe gradients, overmatig glassmorphism
- overal rounded cards, pills, shadows of containers
- generieke SaaS-dashboards, standaard hero-secties zonder inhoudelijke reden
- decoratieve iconen zonder functie, willekeurige accentkleuren
- alles automatisch gecentreerd, onnatuurlijk perfecte symmetrie
- overmatige animaties
- ontwerpen die technisch netjes zijn maar geen eigen identiteit hebben

Deze regels leggen geen stijl op. Wat "passend" is, bepaalt de projectidentiteit.

## Efficiëntie

- Richt de pass op de relevante diff en zichtbare output, niet op de hele app.
- Klein (lokale copy of styling binnen één component/scherm): Claude doet de pass zelf.
- Groot (nieuwe schermen, gewijzigde layout/navigatie of meerdere componenten): Codex mag aanvullend controleren. Geen dubbele reviews zonder duidelijke meerwaarde.

## Definition of Done (bij user-facing wijzigingen)

Niet-toepasselijke punten mogen worden overgeslagen.

- [ ] Humanizer-pass uitgevoerd
- [ ] Tekst klinkt natuurlijk, geen onbedoelde AI-patronen of onnodige em/en dashes
- [ ] Visuele keuzes hebben een bewuste reden, geen generieke AI/SaaS-styling zonder reden
- [ ] Consistent met de projectidentiteit
- [ ] Functionaliteit na humanization opnieuw gecontroleerd

## Projectcontext

Projectspecifieke aanvullingen. Vul in zodra het project een duidelijke identiteit heeft; laat leeg zolang die er niet is.

- Product en doelgroep:
- Tone of voice:
- Visuele richting (kleuren, typografie, stijl):
- Brand assets / referenties:
- Extra do's en don'ts:
