# Guide d'utilisation – fb_scraper.py

Script Playwright (Python) qui exporte les données de **votre propre** compte Facebook
en imitant un utilisateur humain (scroll progressif, pauses aléatoires, souris).

## 1. Installation

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install playwright
playwright install chromium
```

## 2. Première connexion (une seule fois)

```bash
python fb_scraper.py --login
```

- Une fenêtre Chromium s'ouvre : connectez-vous **à la main** (mot de passe, 2FA, etc.).
- Revenez au terminal et appuyez sur **Entrée**.
- La session est stockée dans le dossier `fb_profile/`. Votre mot de passe n'est jamais écrit dans le code.

## 3. Lancer l'extraction

```bash
python fb_scraper.py                              # tout : about, posts, friends, photos
python fb_scraper.py --only about                 # uniquement les infos du profil
python fb_scraper.py --only posts --max-scrolls 80
python fb_scraper.py --out mes_donnees
```

| Option | Rôle |
|---|---|
| `--login` | Connexion manuelle, sauvegarde de la session |
| `--only` | Sections : `about,posts,friends,photos` |
| `--max-scrolls` | Nombre max de défilements par section (défaut 40) |
| `--out` | Dossier de sortie (défaut `export_facebook`) |
| `--headless` | Sans fenêtre (déconseillé, plus facile à détecter) |

## 4. Résultats

Dans le dossier de sortie :
- `about.json` : aperçu, travail/études, lieux, contact, famille, détails, événements
- `posts.json` / `posts.csv` : vos publications (texte + liens)
- `friends.csv` : nom + URL de vos amis
- `photos.json` : URLs des photos
- `tout.json` : tout regroupé

## 5. Comment le comportement « humain » est simulé

- Défilement par la molette, par paliers aléatoires (350–950 px)
- Pauses aléatoires (1–3 s) + longues pauses de « lecture » (4–9 s)
- Retours en arrière occasionnels
- Mouvements de souris progressifs
- Navigateur visible, profil persistant, langue et fuseau cohérents
- Pauses entre chaque section

## 6. Conseils pour limiter les risques

1. **Ne lancez pas souvent** : une fois par semaine maximum. Évitez les `--max-scrolls` énormes.
2. Faites-le depuis votre IP habituelle (pas de VPN/serveur distant), avec le même compte.
3. Si Facebook demande une vérification (checkpoint), faites-la à la main dans la fenêtre, puis relancez plus tard.
4. Commencez avec `--only about` ou `--max-scrolls 10` pour tester.

## 7. Dépannage

- **Sélecteurs qui ne marchent plus** : Facebook change souvent son HTML. Ajustez `JS_ARTICLES`, `JS_LINKS`, `JS_PHOTOS` en inspectant la page (F12).
- **Peu de résultats** : augmentez `--max-scrolls`.
- **Amis en trop/manquants** : adaptez l'expression `SKIP` dans le script.
- **Interface en anglais/autre langue** : les textes de boutons de `dismiss_popups` sont déjà FR/EN ; ajoutez les vôtres si besoin.

## 8. Important

- Facebook interdit le scraping automatisé dans ses conditions d'utilisation : votre compte peut être limité ou suspendu. Aucun script ne garantit de rester indétectable.
- **Alternative officielle et sans risque** : *Paramètres → Vos informations Facebook → Télécharger vos informations* (export complet en JSON/HTML, avec messages, photos, etc.).
- Utilisez ce script uniquement sur **votre propre compte**. Ne l'utilisez pas pour collecter des données d'autres personnes (liste d'amis incluse : respectez leur vie privée et ne la republiez pas).
