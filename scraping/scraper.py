"""
Scraper Playwright - modèle réutilisable
Lancement : python scraper.py

Site de démonstration : https://quotes.toscrape.com/js/ (fait pour s'entraîner).
Pour scraper un autre site, modifie uniquement la section CONFIGURATION.
"""
import csv
import json
import random
import time

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ============================ CONFIGURATION ============================
URL_DEPART = "https://quotes.toscrape.com/js/"

# Sélecteur CSS d'un "bloc" répété sur la page (une carte produit, une citation...)
SELECTEUR_ITEM = "div.quote"

# Champs à extraire dans chaque bloc : "nom_colonne": "sélecteur CSS"
# Pour récupérer un attribut (ex: lien), utilise "sélecteur@attribut"
CHAMPS = {
    "texte": "span.text",
    "auteur": "small.author",
    "lien_auteur": "span a@href",
}

# Bouton / lien "page suivante" (laisse "" si le site n'a pas de pagination)
SELECTEUR_PAGE_SUIVANTE = "li.next > a"

MAX_PAGES = 5            # limite de sécurité
HEADLESS = True          # False = tu vois le navigateur (utile pour déboguer)
PAUSE_MIN, PAUSE_MAX = 1.0, 3.0   # pause aléatoire entre les pages (secondes)
TIMEOUT_MS = 15000       # délai max d'attente (millisecondes)
BLOQUER_IMAGES = True    # accélère le scraping

FICHIER_CSV = "resultats.csv"
FICHIER_JSON = "resultats.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
# =======================================================================


def lire_champ(item, selecteur):
    """Retourne le texte (ou l'attribut) d'un élément, ou None s'il n'existe pas."""
    attribut = None
    if "@" in selecteur:
        selecteur, attribut = selecteur.rsplit("@", 1)

    cible = item.locator(selecteur)
    if cible.count() == 0:
        return None

    premier = cible.first
    if attribut:
        return premier.get_attribute(attribut)
    return premier.inner_text().strip()


def extraire_page(page):
    """Extrait tous les blocs de la page courante."""
    lignes = []
    items = page.locator(SELECTEUR_ITEM)
    for i in range(items.count()):
        item = items.nth(i)
        lignes.append({nom: lire_champ(item, sel) for nom, sel in CHAMPS.items()})
    return lignes


def page_suivante(page):
    """Clique sur 'page suivante'. Retourne False s'il n'y en a plus."""
    if not SELECTEUR_PAGE_SUIVANTE:
        return False
    bouton = page.locator(SELECTEUR_PAGE_SUIVANTE)
    if bouton.count() == 0:
        return False
    bouton.first.click()
    page.wait_for_load_state("domcontentloaded")
    return True


def exporter(resultats):
    if not resultats:
        print("Aucun résultat à exporter.")
        return

    with open(FICHIER_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(CHAMPS.keys()))
        w.writeheader()
        w.writerows(resultats)

    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"{len(resultats)} lignes exportées -> {FICHIER_CSV} et {FICHIER_JSON}")


def main():
    resultats = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(user_agent=USER_AGENT, locale="fr-FR")
        context.set_default_timeout(TIMEOUT_MS)

        if BLOQUER_IMAGES:
            context.route(
                "**/*",
                lambda route: route.abort()
                if route.request.resource_type in ("image", "media", "font")
                else route.continue_(),
            )

        page = context.new_page()

        try:
            page.goto(URL_DEPART, wait_until="domcontentloaded")

            for numero in range(1, MAX_PAGES + 1):
                try:
                    page.wait_for_selector(SELECTEUR_ITEM)
                except PWTimeout:
                    print(f"Page {numero} : aucun élément '{SELECTEUR_ITEM}' trouvé.")
                    break

                donnees = extraire_page(page)
                resultats.extend(donnees)
                print(f"Page {numero} : {len(donnees)} éléments (total {len(resultats)})")

                if not page_suivante(page):
                    print("Fin de la pagination.")
                    break

                time.sleep(random.uniform(PAUSE_MIN, PAUSE_MAX))

        except Exception as e:
            print(f"Erreur : {e}")
            page.screenshot(path="erreur.png")  # capture pour comprendre le problème
        finally:
            browser.close()

    exporter(resultats)


if __name__ == "__main__":
    main()