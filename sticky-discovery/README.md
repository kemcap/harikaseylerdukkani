# Harika Şeyler Dükkanı — Sticky Discovery

Vorschau: https://kemcap.github.io/harikaseylerdukkani/sticky-discovery/

Die Vorschau ist für Suchmaschinen gesperrt. Für die Veröffentlichung auf Turhost die Datei harika-dosemealti-turhost.zip im Repository herunterladen und in public_html/dosemealti/ entpacken. Das Paket enthält freigegebene Indexierung, die endgültige Canonical-Adresse, lokale Unternehmensdaten, türkische WebP-Bildnamen und sitemap.xml.

## Globales Layout / Publikation

Header und Footer für die veröffentlichte Döşemealtı-Homepage werden beim Turhost-Deployment aus `dosemealti/components/header.html` und `dosemealti/components/footer.html` eingefügt. Die GitHub-Pages-Prototypdatei `sticky-discovery/index.html` enthält einen Fallback-Snapshot für die statische Vorschau; neue Menüpunkte bitte nur in den Komponenten ändern. Das GitHub-Actions-Workflow `update-homepage-links.yml` lädt die echte Homepage herunter, legt ein Backup an, erhält die Story-Animationen und rendert die globalen Komponenten vor dem FTPS-Upload. Der separate Kategorie-/Blog-Workflow verarbeitet dieselben Komponenten. Vor Livegang: Pull Request und automatischen Shell-Test prüfen.
