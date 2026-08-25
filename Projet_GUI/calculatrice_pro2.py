import tkinter as tk
from tkinter import messagebox
import math
import re


# ============================================================
#  PALETTE DE COULEURS "MODERNE"
# ============================================================
class Palette:
    sombre = {
        "bg": "#0E0E12",
        "panel": "#17171D",
        "panel2": "#1D1D24",
        "texte": "#F5F5F7",
        "texte_sec": "#8A8A93",
        "chiffre": "#23232B",
        "chiffre_hover": "#2E2E38",
        "fonction": "#2B2B36",
        "fonction_hover": "#38384A",
        "operateur": "#7C5CFC",
        "operateur_hover": "#9179FF",
        "egal": "#00D2A0",
        "egal_hover": "#28E6BA",
        "effacer": "#FF5D6C",
        "effacer_hover": "#FF7A87",
        "accent": "#7C5CFC",
    }
    clair = {
        "bg": "#F2F2F7",
        "panel": "#FFFFFF",
        "panel2": "#EDEDF3",
        "texte": "#141418",
        "texte_sec": "#6E6E76",
        "chiffre": "#FFFFFF",
        "chiffre_hover": "#E9E9F0",
        "fonction": "#E4E4EC",
        "fonction_hover": "#D6D6E2",
        "operateur": "#7C5CFC",
        "operateur_hover": "#9179FF",
        "egal": "#00B589",
        "egal_hover": "#00D2A0",
        "effacer": "#FF5D6C",
        "effacer_hover": "#FF7A87",
        "accent": "#7C5CFC",
    }


# ============================================================
#  BOUTON ARRONDI "MAISON" (Canvas) — look moderne + animation
# ============================================================
class BoutonRond(tk.Canvas):
    def __init__(self, parent, texte, commande, bg, fg, hover,
                 largeur=76, hauteur=64, rayon=18, police=("Segoe UI", 15, "bold"),
                 fond_parent="#0E0E12"):
        super().__init__(parent, width=largeur, height=hauteur,
                          bg=fond_parent, highlightthickness=0, bd=0)
        self.commande = commande
        self.bg = bg
        self.hover = hover
        self.fg = fg
        self.rayon = rayon
        self.texte = texte
        self.police = police
        self.largeur = largeur
        self.hauteur = hauteur
        self._dessiner(self.bg)

        self.bind("<Enter>", lambda e: self._dessiner(self.hover))
        self.bind("<Leave>", lambda e: self._dessiner(self.bg))
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", lambda e: self._dessiner(self.hover))

    def _forme_arrondie(self, x1, y1, x2, y2, r, **kw):
        pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
               x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(pts, smooth=True, **kw)

    def _dessiner(self, couleur):
        self.delete("all")
        self._forme_arrondie(2, 2, self.largeur - 2, self.hauteur - 2, self.rayon,
                              fill=couleur, outline="")
        self.create_text(self.largeur / 2, self.hauteur / 2, text=self.texte,
                          fill=self.fg, font=self.police)

    def _on_click(self, event):
        self._dessiner(self.hover)
        if self.commande:
            self.commande()

    def maj_couleurs(self, bg, hover, fg, fond_parent=None):
        self.bg, self.hover, self.fg = bg, hover, fg
        if fond_parent:
            self.configure(bg=fond_parent)
        self._dessiner(self.bg)


# ============================================================
#  CALCULATRICE MODERNE
# ============================================================
class CalculatriceModerne:

    RE_VALIDE = re.compile(r"^[0-9+\-*/.()%\s]*$")

    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculatrice")
        self.root.configure(bg=Palette.sombre["bg"])
        self.root.resizable(False, False)

        self.theme_sombre = True
        self.couleurs = Palette.sombre
        self.mode_scientifique = False

        self.expression = ""
        self.resultat_var = tk.StringVar(value="0")
        self.memoire = 0
        self.historique = []
        self.boutons = []  # pour rafraîchir les couleurs au changement de thème

        self.LARGEUR_BASE = 360
        self.HAUTEUR_AFFICHAGE = 100
        self.HAUTEUR_BASE = 520
        self.HAUTEUR_SCI = 720
        self.root.geometry(f"{self.LARGEUR_BASE}x{self.HAUTEUR_BASE}")

        self._creer_entete()
        self._creer_affichage()
        self._creer_zone_boutons()
        self._construire_clavier()
        self._lier_raccourcis()

    # -------------------- ENTÊTE --------------------
    def _creer_entete(self):
        c = self.couleurs
        self.entete = tk.Frame(self.root, bg=c["bg"], height=40)
        self.entete.pack(fill="x", padx=14, pady=(10, 0))

        self.btn_historique = tk.Label(self.entete, text="📋", bg=c["bg"],
                                        fg=c["texte_sec"], font=("Segoe UI", 14),
                                        cursor="hand2")
        self.btn_historique.pack(side="left")
        self.btn_historique.bind("<Button-1>", lambda e: self.afficher_historique())

        self.btn_sci = tk.Label(self.entete, text="🔬", bg=c["bg"],
                                 fg=c["texte_sec"], font=("Segoe UI", 14),
                                 cursor="hand2")
        self.btn_sci.pack(side="left", padx=10)
        self.btn_sci.bind("<Button-1>", lambda e: self.basculer_scientifique())

        self.btn_theme = tk.Label(self.entete, text="🌙", bg=c["bg"],
                                   fg=c["texte_sec"], font=("Segoe UI", 14),
                                   cursor="hand2")
        self.btn_theme.pack(side="right")
        self.btn_theme.bind("<Button-1>", lambda e: self.basculer_theme())

        self.btn_effacer_tout = tk.Label(self.entete, text="🔄", bg=c["bg"],
                                          fg=c["texte_sec"], font=("Segoe UI", 14),
                                          cursor="hand2")
        self.btn_effacer_tout.pack(side="right", padx=10)
        self.btn_effacer_tout.bind("<Button-1>", lambda e: self.reinitialiser())

    # -------------------- AFFICHAGE --------------------
    def _creer_affichage(self):
        c = self.couleurs
        h = self.HAUTEUR_AFFICHAGE
        self.LARGEUR_PANNEAU = self.LARGEUR_BASE - 28
        self.zone_affichage = tk.Canvas(self.root, height=h, bg=c["bg"],
                                         highlightthickness=0)
        self.zone_affichage.pack(fill="x", padx=14, pady=(10, 6))

        self._dessiner_panneau_affichage()

        x_droite = self.LARGEUR_PANNEAU - 16  # marge intérieure droite

        self.label_expression = tk.Label(self.zone_affichage, text="",
                                          font=("Segoe UI", 11), bg=c["panel"],
                                          fg=c["texte_sec"], anchor="e")
        self.zone_affichage.create_window(x_droite, h * 0.32, anchor="e",
                                           window=self.label_expression)

        self.label_resultat = tk.Label(self.zone_affichage, textvariable=self.resultat_var,
                                        font=("Segoe UI", 32, "bold"), bg=c["panel"],
                                        fg=c["texte"], anchor="e")
        self.zone_affichage.create_window(x_droite, h * 0.68, anchor="e",
                                           window=self.label_resultat)

    def _dessiner_panneau_affichage(self):
        c = self.couleurs
        self.zone_affichage.delete("panneau")
        largeur = self.LARGEUR_PANNEAU
        h = self.HAUTEUR_AFFICHAGE
        r = 18
        pts = [r, 0, largeur - r, 0, largeur, 0, largeur, r,
               largeur, h - r, largeur, h, largeur - r, h,
               r, h, 0, h, 0, h - r, 0, r, 0, 0]
        self.zone_affichage.create_polygon(pts, smooth=True, fill=c["panel"],
                                            outline="", tags="panneau")
        self.zone_affichage.tag_lower("panneau")

    # -------------------- ZONE BOUTONS --------------------
    def _creer_zone_boutons(self):
        c = self.couleurs
        self.zone_boutons = tk.Frame(self.root, bg=c["bg"])
        self.zone_boutons.pack(expand=True, fill="both", padx=10, pady=6)

        self.frame_sci = tk.Frame(self.zone_boutons, bg=c["bg"])
        self.frame_base = tk.Frame(self.zone_boutons, bg=c["bg"])
        self.frame_base.pack(expand=True, fill="both")

    # -------------------- CONSTRUCTION CLAVIER --------------------
    def _construire_clavier(self):
        c = self.couleurs

        # ---- Grille scientifique (optionnelle) ----
        sci_config = [
            ("sin", "sin"), ("cos", "cos"), ("tan", "tan"), ("π", "pi"),
            ("log", "log"), ("ln", "ln"), ("(", "("), (")", ")"),
            ("xʸ", "**"), ("x³", "cube"), ("n!", "fact"), ("e", "euler"),
        ]
        self.boutons_sci = []
        for i, (texte, cmd) in enumerate(sci_config):
            b = BoutonRond(self.frame_sci, texte, lambda v=cmd: self.action(v),
                            bg=c["fonction"], hover=c["fonction_hover"], fg=c["texte"],
                            largeur=76, hauteur=52, rayon=14,
                            police=("Segoe UI", 12, "bold"), fond_parent=c["bg"])
            b.grid(row=i // 4, column=i % 4, padx=4, pady=4, sticky="nsew")
            self.boutons_sci.append(b)
        for i in range(4):
            self.frame_sci.grid_columnconfigure(i, weight=1)

        # ---- Grille de base ----
        base_config = [
            ("MC", "mc", "fonction"), ("MR", "mr", "fonction"),
            ("M+", "mplus", "fonction"), ("M-", "mminus", "fonction"),

            ("√", "racine", "fonction"), ("x²", "carre", "fonction"),
            ("1/x", "inverse", "fonction"), ("C", "effacer", "effacer"),

            ("⌫", "retour", "fonction"), ("±", "negatif", "fonction"),
            ("%", "pourcent", "fonction"), ("÷", "/", "operateur"),

            ("7", "7", "chiffre"), ("8", "8", "chiffre"),
            ("9", "9", "chiffre"), ("×", "*", "operateur"),

            ("4", "4", "chiffre"), ("5", "5", "chiffre"),
            ("6", "6", "chiffre"), ("-", "-", "operateur"),

            ("1", "1", "chiffre"), ("2", "2", "chiffre"),
            ("3", "3", "chiffre"), ("+", "+", "operateur"),

            ("0", "0", "chiffre", 2), (",", ".", "chiffre"),
            ("=", "egal", "egal"),
        ]

        self.boutons_base = []
        row = col = 0
        for item in base_config:
            if len(item) == 4:
                texte, cmd, style, colspan = item
            else:
                texte, cmd, style = item
                colspan = 1

            bg_key = style
            hover_key = f"{style}_hover" if f"{style}_hover" in c else c["fonction_hover"]

            b = BoutonRond(self.frame_base, texte,
                            (self.calculer if cmd == "egal" else lambda v=cmd: self.action(v)),
                            bg=c.get(bg_key, c["fonction"]),
                            hover=c.get(hover_key, c["fonction_hover"]),
                            fg="#FFFFFF" if style in ("operateur", "egal", "effacer") else c["texte"],
                            largeur=76 if colspan == 1 else 160, hauteur=62, rayon=18,
                            fond_parent=c["bg"])
            b.grid(row=row, column=col, columnspan=colspan, padx=4, pady=4, sticky="nsew")
            b._style = style
            self.boutons_base.append(b)

            col += colspan
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            self.frame_base.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.frame_base.grid_rowconfigure(i, weight=1)

    # -------------------- RACCOURCIS CLAVIER --------------------
    def _lier_raccourcis(self):
        self.root.bind("<Key>", self._touche_clavier)
        self.root.bind("<Control-c>", lambda e: self.copier_resultat())
        self.root.bind("<Control-v>", lambda e: self.coller_expression())
        self.root.bind("<Escape>", lambda e: self.reinitialiser())

    def _touche_clavier(self, event):
        touche = event.char
        if touche and touche in "0123456789.+-*/()%":
            self.action(touche)
        elif event.keysym == "Return":
            self.calculer()
        elif event.keysym == "BackSpace":
            self.action("retour")
        elif touche.lower() == "c":
            self.action("effacer")

    # -------------------- LOGIQUE --------------------
    def action(self, valeur):
        c = self.couleurs

        if valeur == "effacer":
            self.expression = ""
            self.resultat_var.set("0")
            self.label_expression.config(text="")
            return

        if valeur == "retour":
            self.expression = self.expression[:-1]
            self.resultat_var.set(self.expression if self.expression else "0")
            return

        if valeur == "negatif":
            try:
                nombre = float(self.expression or "0")
                self.expression = self._format(-nombre)
                self.resultat_var.set(self.expression)
            except Exception:
                pass
            return

        if valeur == "pourcent":
            try:
                nombre = float(self.expression)
                self.expression = self._format(nombre / 100)
                self.resultat_var.set(self.expression)
            except Exception:
                pass
            return

        # ---- fonctions à un argument ----
        fonctions_un_arg = {
            "racine": (math.sqrt, "√({v}) ="),
            "carre": (lambda v: v ** 2, "({v})² ="),
            "inverse": (lambda v: 1 / v, "1/({v}) ="),
            "sin": (lambda v: math.sin(math.radians(v)), "sin({v}) ="),
            "cos": (lambda v: math.cos(math.radians(v)), "cos({v}) ="),
            "tan": (lambda v: math.tan(math.radians(v)), "tan({v}) ="),
            "log": (math.log10, "log({v}) ="),
            "ln": (math.log, "ln({v}) ="),
            "cube": (lambda v: v ** 3, "({v})³ ="),
            "fact": (lambda v: math.factorial(int(v)), "({v})! ="),
        }
        if valeur in fonctions_un_arg:
            try:
                nombre = float(self.expression)
                fonc, libelle = fonctions_un_arg[valeur]
                resultat = fonc(nombre)
                self.expression = self._format(resultat)
                self.resultat_var.set(self.expression)
                self.label_expression.config(text=libelle.format(v=self._format(nombre)))
            except Exception:
                self._erreur("Entrée invalide")
            return

        if valeur == "pi":
            self.expression += self._format(math.pi)
            self.resultat_var.set(self.expression)
            return

        if valeur == "euler":
            self.expression += self._format(math.e)
            self.resultat_var.set(self.expression)
            return

        if valeur == "mc":
            self.memoire = 0
            return
        if valeur == "mr":
            self.expression = self._format(self.memoire)
            self.resultat_var.set(self.expression)
            return
        if valeur == "mplus":
            try:
                self.memoire += float(self.expression)
            except Exception:
                pass
            return
        if valeur == "mminus":
            try:
                self.memoire -= float(self.expression)
            except Exception:
                pass
            return

        # ---- saisie normale ----
        self.expression += valeur
        self.resultat_var.set(self.expression)

    def calculer(self):
        expr_affiche = self.expression
        expr = expr_affiche.replace("×", "*").replace("÷", "/")

        if not expr or not self.RE_VALIDE.match(expr):
            self._erreur("Expression invalide")
            return

        try:
            self.label_expression.config(text=expr_affiche + " =")
            resultat = eval(expr, {"__builtins__": {}}, {})

            if isinstance(resultat, float):
                resultat = round(resultat, 10)
                if resultat.is_integer():
                    resultat = int(resultat)

            texte = str(resultat)
            self.historique.append(f"{expr_affiche} = {texte}")
            self.resultat_var.set(texte)
            self.expression = texte

        except ZeroDivisionError:
            self._erreur("Division par zéro")
        except Exception:
            self._erreur("Erreur de calcul")

    def _erreur(self, message):
        self.resultat_var.set("Erreur")
        self.expression = ""
        self.label_expression.config(text=f"⚠️ {message}")

    @staticmethod
    def _format(valeur):
        valeur = round(float(valeur), 10)
        if valeur.is_integer():
            return str(int(valeur))
        return str(valeur)

    def reinitialiser(self):
        self.expression = ""
        self.resultat_var.set("0")
        self.label_expression.config(text="")
        self.memoire = 0

    # -------------------- PRESSE-PAPIER --------------------
    def copier_resultat(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.resultat_var.get())

    def coller_expression(self):
        try:
            contenu = self.root.clipboard_get()
            if self.RE_VALIDE.match(contenu):
                self.expression += contenu
                self.resultat_var.set(self.expression)
        except Exception:
            pass

    # -------------------- HISTORIQUE --------------------
    def afficher_historique(self):
        c = self.couleurs
        fenetre = tk.Toplevel(self.root)
        fenetre.title("📋 Historique")
        fenetre.geometry("320x420")
        fenetre.configure(bg=c["bg"])
        fenetre.resizable(False, False)

        tk.Label(fenetre, text="Historique des calculs", bg=c["bg"], fg=c["texte"],
                 font=("Segoe UI", 13, "bold")).pack(pady=(14, 6))

        cadre_liste = tk.Frame(fenetre, bg=c["bg"])
        cadre_liste.pack(fill="both", expand=True, padx=14, pady=6)

        scrollbar = tk.Scrollbar(cadre_liste)
        scrollbar.pack(side="right", fill="y")

        liste = tk.Listbox(cadre_liste, bg=c["panel"], fg=c["texte"],
                            font=("Segoe UI", 11), bd=0, highlightthickness=0,
                            selectbackground=c["accent"], yscrollcommand=scrollbar.set)
        liste.pack(fill="both", expand=True)
        scrollbar.config(command=liste.yview)

        if not self.historique:
            liste.insert("end", "  Aucun calcul pour le moment.")
        else:
            for ligne in reversed(self.historique[-50:]):
                liste.insert("end", "  " + ligne)

        def reutiliser(event):
            try:
                index = liste.curselection()[0]
                ligne = liste.get(index).strip()
                if "=" in ligne:
                    self.expression = ligne.split("=")[-1].strip()
                    self.resultat_var.set(self.expression)
                    fenetre.destroy()
            except Exception:
                pass

        liste.bind("<Double-Button-1>", reutiliser)

        bas = tk.Frame(fenetre, bg=c["bg"])
        bas.pack(fill="x", padx=14, pady=(0, 14))

        def vider():
            self.historique.clear()
            fenetre.destroy()

        tk.Button(bas, text="Vider", command=vider, bg=c["effacer"], fg="white",
                  relief="flat", font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Button(bas, text="Fermer", command=fenetre.destroy, bg=c["fonction"],
                  fg=c["texte"], relief="flat", font=("Segoe UI", 10, "bold")).pack(side="right")

    # -------------------- MODE SCIENTIFIQUE --------------------
    def basculer_scientifique(self):
        self.mode_scientifique = not self.mode_scientifique
        if self.mode_scientifique:
            self.frame_sci.pack(fill="x", pady=(0, 4), before=self.frame_base)
            self.root.geometry(f"{self.LARGEUR_BASE}x{self.HAUTEUR_SCI}")
            self.btn_sci.config(fg=self.couleurs["accent"])
        else:
            self.frame_sci.pack_forget()
            self.root.geometry(f"{self.LARGEUR_BASE}x{self.HAUTEUR_BASE}")
            self.btn_sci.config(fg=self.couleurs["texte_sec"])

    # -------------------- THÈME --------------------
    def basculer_theme(self):
        self.theme_sombre = not self.theme_sombre
        self.couleurs = Palette.sombre if self.theme_sombre else Palette.clair
        self.btn_theme.config(text="🌙" if self.theme_sombre else "☀️")
        self._appliquer_theme()

    def _appliquer_theme(self):
        c = self.couleurs

        self.root.configure(bg=c["bg"])
        self.entete.configure(bg=c["bg"])
        for lbl in (self.btn_historique, self.btn_sci, self.btn_theme, self.btn_effacer_tout):
            lbl.configure(bg=c["bg"], fg=c["texte_sec"])
        if self.mode_scientifique:
            self.btn_sci.config(fg=c["accent"])

        self.zone_affichage.configure(bg=c["bg"])
        self._dessiner_panneau_affichage()
        self.label_expression.configure(bg=c["panel"], fg=c["texte_sec"])
        self.label_resultat.configure(bg=c["panel"], fg=c["texte"])

        self.zone_boutons.configure(bg=c["bg"])
        self.frame_sci.configure(bg=c["bg"])
        self.frame_base.configure(bg=c["bg"])

        for b in self.boutons_sci:
            b.maj_couleurs(c["fonction"], c["fonction_hover"], c["texte"], c["bg"])

        for b in self.boutons_base:
            style = b._style
            hover_key = f"{style}_hover" if f"{style}_hover" in c else c["fonction_hover"]
            fg = "#FFFFFF" if style in ("operateur", "egal", "effacer") else c["texte"]
            b.maj_couleurs(c.get(style, c["fonction"]), c.get(hover_key, c["fonction_hover"]),
                           fg, c["bg"])


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatriceModerne(root)
    root.mainloop()