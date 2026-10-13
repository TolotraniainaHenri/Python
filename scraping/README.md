# Web Scraper Playwright

Un modèle de scraper en Python basé sur [Playwright](https://playwright.dev/python/), capable de récupérer des données sur des sites statiques comme sur des sites rendus en JavaScript. Il suffit de modifier une section de configuration pour l'adapter à un nouveau site.

Ce projet fait partie du dépôt [TolotraniainaHenri/Python](https://github.com/TolotraniainaHenri/Python), dans le dossier `scraping/`.

## Fonctionnalités

- Gère les sites dynamiques (React, Vue, contenu chargé en JavaScript)
- Pagination automatique via un bouton « page suivante »
- Extraction de texte ou d'attributs (`href`, `src`, ...) via sélecteurs CSS
- Export en **CSV** (compatible Excel) et **JSON**
- Pauses aléatoires entre les pages et blocage des images pour aller plus vite
- Capture d'écran automatique en cas d'erreur

## Prérequis

- Python 3.9 ou supérieur
- Linux, macOS ou Windows

## Installation

```bash
git clone https://github.com/TolotraniainaHenri/Python.git
cd Python/scraping

python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

> Sur Debian/Ubuntu, si tu vois l'erreur `externally managed environment`, c'est que le `venv` n'est pas activé. Installe d'abord `python3-full` et `python3-venv` avec `sudo apt install python3-full python3-venv`.
>
> Si Chromium signale des bibliothèques manquantes : `sudo venv/bin/playwright install-deps chromium`

## Utilisation rapide

```bash
python scraper.py
```

Par défaut, le script scrape le site d'entraînement `https://quotes.toscrape.com/js/` et génère :

| Fichier | Contenu |
|---|---|
| `resultats.csv` | Données au format tableur |
| `resultats.json` | Données au format JSON |
| `erreur.png` | Capture d'écran, seulement si une erreur survient |

## Adapter le scraper à ton site

Modifie uniquement la section **CONFIGURATION** en haut de `scraper.py`.

```python
URL_DEPART = "https://monsite.com/produits"
SELECTEUR_ITEM = "div.produit"
CHAMPS = {
    "nom":   "h2.titre",
    "prix":  "span.prix",
    "image": "img@src",
    "lien":  "a@href",
}
SELECTEUR_PAGE_SUIVANTE = "a.next"
MAX_PAGES = 10
```

| Variable | Rôle |
|---|---|
| `URL_DEPART` | Page de départ |
| `SELECTEUR_ITEM` | Sélecteur CSS du bloc répété (une carte, une annonce) |
| `CHAMPS` | Données à extraire. `sélecteur@attribut` récupère un attribut |
| `SELECTEUR_PAGE_SUIVANTE` | Bouton « suivant » (`""` s'il n'y a pas de pagination) |
| `MAX_PAGES` | Nombre maximum de pages à parcourir |
| `HEADLESS` | `False` pour voir le navigateur pendant l'exécution |
| `PAUSE_MIN` / `PAUSE_MAX` | Pause aléatoire entre deux pages (secondes) |
| `TIMEOUT_MS` | Délai maximum d'attente (millisecondes) |
| `BLOQUER_IMAGES` | Bloque images, médias et polices pour accélérer |

Si un champ est absent d'un bloc, sa valeur est `None` et le script continue.

### Trouver les sélecteurs CSS

1. Ouvre le site dans Chrome, clic droit sur l'élément, puis **Inspecter**.
2. Repère la balise et sa classe, par exemple `<div class="produit">` donne `div.produit`.
3. Vérifie dans la console du navigateur :
   ```js
   document.querySelectorAll("div.produit").length
   ```
   Si le nombre correspond à ce que tu vois à l'écran, le sélecteur est bon.

## Cas particuliers

<details>
<summary>Scroll infini</summary>

```python
def scroller_jusqu_au_bout(page, pause=1.5, max_scrolls=30):
    hauteur = 0
    for _ in range(max_scrolls):
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(int(pause * 1000))
        nouvelle = page.evaluate("document.body.scrollHeight")
        if nouvelle == hauteur:
            break
        hauteur = nouvelle
```

Appelle cette fonction avant `extraire_page(page)`.
</details>

<details>
<summary>Bouton « Charger plus »</summary>

```python
while page.locator("button.load-more").count() > 0:
    page.click("button.load-more")
    page.wait_for_timeout(1500)
```
</details>

<details>
<summary>Pagination par numéro dans l'URL</summary>

```python
for n in range(1, 11):
    page.goto(f"https://monsite.com/produits?page={n}")
    page.wait_for_selector("div.produit")
    resultats.extend(extraire_page(page))
```
</details>

<details>
<summary>Connexion à un site</summary>

```python
page.goto("https://monsite.com/login")
page.fill("input[name='email']", "ton@email.com")
page.fill("input[name='password']", "motdepasse")
page.click("button[type='submit']")
page.wait_for_load_state("networkidle")
```

Ne mets jamais d'identifiants en clair dans le code publié sur GitHub. Utilise des variables d'environnement.
</details>

## Outils de débogage

```bash
# Enregistre tes clics et génère le code Playwright
playwright codegen https://monsite.com
```

- `HEADLESS = False` pour voir le navigateur travailler
- `launch(headless=False, slow_mo=500)` pour ralentir les actions
- `page.screenshot(path="page.png", full_page=True)` pour une capture

## Problèmes fréquents

| Problème | Solution |
|---|---|
| `externally managed environment` | Active le `venv` avant `pip install` |
| `TimeoutError` | Vérifie le sélecteur dans la console, augmente `TIMEOUT_MS` |
| Résultats vides | Le contenu n'est pas chargé : utilise `wait_for_selector` |
| Erreur 403 | Le site bloque les robots : ralentis, réduis le nombre de requêtes |
| Erreur 429 | Trop de requêtes : augmente `PAUSE_MIN` et `PAUSE_MAX` |
| `Executable doesn't exist` | Lance `playwright install chromium` |

## Bonnes pratiques et légalité

- Consulte le `robots.txt` du site et ses conditions d'utilisation avant de scraper.
- Garde des pauses entre les requêtes pour ne pas surcharger le serveur.
- Ne collecte pas de données personnelles sans base légale (RGPD et lois locales).
- Utilise l'API officielle du site si elle existe.
- Ne contourne pas les protections (CAPTCHA, paywall, authentification) qui ne t'appartiennent pas.

L'auteur de ce dépôt décline toute responsabilité pour l'usage qui en est fait.

## Structure du projet

```
Python/
└── scraping/
    ├── scraper.py          # Script principal
    ├── requirements.txt    # Dépendances Python
    ├── README.md           # Ce fichier
    └── .gitignore
```

## Auteur

[TolotraniainaHenri](https://github.com/TolotraniainaHenri)
