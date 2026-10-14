#!/usr/bin/env python3
"""
fb_scraper.py - Exporte les informations de VOTRE PROPRE compte Facebook
avec Playwright (Python), en imitant un comportement humain (scroll
progressif, pauses aléatoires, mouvements de souris).

Usage :
    python fb_scraper.py --login                 # 1ère fois : connexion manuelle
    python fb_scraper.py                         # extraction complète
    python fb_scraper.py --only about,posts      # seulement certaines sections
    python fb_scraper.py --max-scrolls 60 --out mes_donnees
"""
import argparse
import csv
import hashlib
import json
import random
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE_DIR = Path("fb_profile")  # session persistante (cookies, etc.)
FB = "https://www.facebook.com"

ABOUT_SECTIONS = {
    "overview": "about",
    "work_education": "about_work_and_education",
    "places": "about_places",
    "contact_basic": "about_contact_and_basic_info",
    "family": "about_family_and_relationships",
    "details": "about_details",
    "life_events": "about_life_events",
}

# ----------------------------------------------------------------------
# Comportement "humain"
# ----------------------------------------------------------------------
def pause(a=0.8, b=2.6):
    time.sleep(random.uniform(a, b))


def long_pause():
    """Petite 'distraction' : l'utilisateur lit un post."""
    time.sleep(random.uniform(4, 9))


def wander_mouse(page):
    vp = page.viewport_size or {"width": 1280, "height": 800}
    x = random.randint(int(vp["width"] * 0.2), int(vp["width"] * 0.8))
    y = random.randint(int(vp["height"] * 0.2), int(vp["height"] * 0.8))
    page.mouse.move(x, y, steps=random.randint(8, 25))


def human_scroll(page, on_step=None, max_scrolls=40, stable_limit=5):
    """
    Fait défiler la page comme un humain.
    on_step() est appelé après chaque défilement pour collecter le contenu
    (Facebook retire du DOM les éléments hors écran).
    """
    stable = 0
    last_height = 0
    for i in range(1, max_scrolls + 1):
        wander_mouse(page)
        page.mouse.wheel(0, random.randint(350, 950))
        pause(1.0, 3.0)

        # parfois on remonte un peu
        if random.random() < 0.15:
            page.mouse.wheel(0, -random.randint(100, 350))
            pause(0.6, 1.5)

        # parfois on s'arrête pour "lire"
        if i % random.randint(5, 9) == 0:
            long_pause()

        if on_step:
            on_step()

        height = page.evaluate("document.body.scrollHeight")
        if height == last_height:
            stable += 1
            if stable >= stable_limit:
                break
        else:
            stable = 0
            last_height = height
        print(f"  scroll {i}/{max_scrolls}", end="\r")
    print()


# ----------------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------------
def build_url(base, section):
    """Construit l'URL d'une section selon le format du profil."""
    if "profile.php" in base:
        sep = "&" if "?" in base else "?"
        return f"{base}{sep}sk={section.replace('about_', 'about_')}" if section != "about" \
            else f"{base}&sk=about"
    return f"{base.rstrip('/')}/{section}"


def clean_base_url(url):
    url = url.split("#")[0]
    m = re.match(r"(https://www\.facebook\.com/profile\.php\?id=\d+)", url)
    if m:
        return m.group(1)
    return url.split("?")[0].rstrip("/")


def main_text(page):
    try:
        return page.inner_text('div[role="main"]', timeout=8000)
    except Exception:
        return page.inner_text("body")


def dismiss_popups(page):
    for label in ["Refuser les cookies optionnels", "Decline optional cookies",
                  "Fermer", "Close", "Pas maintenant", "Not now"]:
        try:
            btn = page.get_by_role("button", name=label)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=1500)
                pause(0.5, 1.2)
        except Exception:
            pass


# ----------------------------------------------------------------------
# Extractions
# ----------------------------------------------------------------------
def scrape_about(page, base):
    data = {}
    for key, section in ABOUT_SECTIONS.items():
        print(f"[À propos] {key}")
        page.goto(build_url(base, section), wait_until="domcontentloaded")
        pause(2.5, 5)
        dismiss_popups(page)
        # petit scroll pour charger le contenu
        for _ in range(random.randint(1, 3)):
            wander_mouse(page)
            page.mouse.wheel(0, random.randint(300, 700))
            pause(1, 2.2)
        data[key] = main_text(page)
        pause(2, 4)
    return data


JS_ARTICLES = """
() => Array.from(document.querySelectorAll('div[role="article"]'))
  .filter(e => !e.parentElement.closest('[role="article"]'))   // exclut les commentaires
  .map(e => ({
     text: e.innerText,
     links: Array.from(e.querySelectorAll('a[href]'))
        .map(a => a.href)
        .filter(h => /\\/posts\\/|story_fbid|permalink|\\/videos\\/|\\/photo/.test(h))
  }))
"""


def scrape_posts(page, base, max_scrolls):
    print("[Publications] chargement du profil")
    page.goto(base, wait_until="domcontentloaded")
    pause(3, 5)
    dismiss_popups(page)

    posts = {}

    def collect():
        try:
            for item in page.evaluate(JS_ARTICLES):
                text = (item["text"] or "").strip()
                if len(text) < 15:
                    continue
                h = hashlib.md5(text.encode()).hexdigest()
                if h not in posts:
                    posts[h] = {
                        "text": text,
                        "links": sorted(set(item["links"]))[:5],
                    }
        except Exception:
            pass

    collect()
    human_scroll(page, on_step=collect, max_scrolls=max_scrolls)
    collect()
    print(f"  -> {len(posts)} publications collectées")
    return list(posts.values())


JS_LINKS = """
() => Array.from(document.querySelectorAll('div[role="main"] a[href]'))
  .map(a => ({name: (a.innerText || '').trim().split('\\n')[0], url: a.href}))
  .filter(x => x.name && x.name.length > 1)
"""

SKIP = re.compile(
    r"(sk=|/friends|/photos|/videos|/about|/likes|/following|/groups|"
    r"/watch|/marketplace|/reel|/stories|/hashtag|/posts/|/settings)", re.I)


def scrape_friends(page, base, max_scrolls):
    print("[Amis] chargement")
    url = f"{base}&sk=friends" if "profile.php" in base else f"{base}/friends"
    page.goto(url, wait_until="domcontentloaded")
    pause(3, 5)
    dismiss_popups(page)

    friends = {}

    def collect():
        try:
            for x in page.evaluate(JS_LINKS):
                u = x["url"].split("&__tn__")[0].split("?__cft__")[0]
                if "facebook.com" not in u or SKIP.search(u):
                    continue
                friends.setdefault(u, x["name"])
        except Exception:
            pass

    collect()
    human_scroll(page, on_step=collect, max_scrolls=max_scrolls)
    collect()
    result = [{"name": n, "url": u} for u, n in friends.items()]
    print(f"  -> {len(result)} amis collectés")
    return result


JS_PHOTOS = """
() => Array.from(document.querySelectorAll('a[href*="/photo"] img'))
  .map(i => ({alt: i.alt || '', src: i.src}))
"""


def scrape_photos(page, base, max_scrolls):
    print("[Photos] chargement")
    url = f"{base}&sk=photos" if "profile.php" in base else f"{base}/photos"
    page.goto(url, wait_until="domcontentloaded")
    pause(3, 5)
    dismiss_popups(page)

    photos = {}

    def collect():
        try:
            for x in page.evaluate(JS_PHOTOS):
                photos.setdefault(x["src"], x["alt"])
        except Exception:
            pass

    collect()
    human_scroll(page, on_step=collect, max_scrolls=max_scrolls)
    collect()
    print(f"  -> {len(photos)} photos (URLs) collectées")
    return [{"src": s, "alt": a} for s, a in photos.items()]


# ----------------------------------------------------------------------
# Programme principal
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Export de MON compte Facebook")
    ap.add_argument("--login", action="store_true",
                    help="Ouvre le navigateur pour vous connecter manuellement")
    ap.add_argument("--only", default="about,posts,friends,photos",
                    help="Sections : about,posts,friends,photos")
    ap.add_argument("--max-scrolls", type=int, default=40,
                    help="Nombre max de défilements par section")
    ap.add_argument("--out", default="export_facebook",
                    help="Dossier de sortie")
    ap.add_argument("--headless", action="store_true",
                    help="Sans fenêtre (déconseillé : plus détectable)")
    args = ap.parse_args()

    sections = {s.strip() for s in args.only.split(",")}
    out = Path(args.out)
    out.mkdir(exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            headless=args.headless,
            viewport={"width": 1366, "height": 850},
            locale="fr-FR",
            timezone_id="Indian/Antananarivo",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        if args.login:
            page.goto(FB)
            input("\n>>> Connectez-vous dans la fenêtre (2FA inclus), "
                  "puis appuyez sur Entrée ici... ")
            print("Session enregistrée dans ./fb_profile")
            ctx.close()
            return

        page.goto(f"{FB}/me", wait_until="domcontentloaded")
        pause(3, 5)
        if "login" in page.url or "checkpoint" in page.url:
            print("Non connecté (ou vérification demandée). "
                  "Lancez d'abord : python fb_scraper.py --login")
            ctx.close()
            return

        dismiss_popups(page)
        base = clean_base_url(page.url)
        print(f"Profil détecté : {base}\n")

        result = {"profile_url": base}

        if "about" in sections:
            result["about"] = scrape_about(page, base)
            (out / "about.json").write_text(
                json.dumps(result["about"], ensure_ascii=False, indent=2),
                encoding="utf-8")

        if "posts" in sections:
            posts = scrape_posts(page, base, args.max_scrolls)
            result["posts"] = posts
            (out / "posts.json").write_text(
                json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
            with open(out / "posts.csv", "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["text", "links"])
                for x in posts:
                    w.writerow([x["text"], " | ".join(x["links"])])
            pause(4, 8)

        if "friends" in sections:
            friends = scrape_friends(page, base, args.max_scrolls)
            result["friends"] = friends
            with open(out / "friends.csv", "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=["name", "url"])
                w.writeheader()
                w.writerows(friends)
            pause(4, 8)

        if "photos" in sections:
            photos = scrape_photos(page, base, args.max_scrolls)
            result["photos"] = photos
            (out / "photos.json").write_text(
                json.dumps(photos, ensure_ascii=False, indent=2), encoding="utf-8")

        (out / "tout.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nTerminé. Fichiers dans : {out.resolve()}")
        ctx.close()


if __name__ == "__main__":
    main()
