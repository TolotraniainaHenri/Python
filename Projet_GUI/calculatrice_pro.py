import tkinter as tk
from tkinter import messagebox
import math


class CalculatricePro:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculatrice")
        self.root.geometry("340x540")
        self.root.resizable(False, False)
        self.root.configure(bg="#1C1C1E")

        # Variables
        self.expression = ""
        self.resultat = tk.StringVar()
        self.resultat.set("0")
        self.memoire = 0
        self.historique = []
        self.theme_sombre = True

        # Création de l'interface
        self.creer_menu()
        self.creer_affichage()
        self.creer_boutons()
        self.lier_clavier()

    def creer_menu(self):
        """Crée le menu supérieur"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        fichier_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁", menu=fichier_menu)
        fichier_menu.add_command(label="🔄 Réinitialiser", command=self.reinitialiser)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="📋 Historique", command=self.afficher_historique)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="🚪 Quitter", command=self.root.quit)

        affichage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️", menu=affichage_menu)
        affichage_menu.add_command(label="🌙 Sombre", command=self.theme_sombre_mode)
        affichage_menu.add_command(label="☀️ Clair", command=self.theme_clair_mode)

        aide_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓", menu=aide_menu)
        aide_menu.add_command(label="Aide", command=self.afficher_aide)
        aide_menu.add_command(label="À propos", command=self.afficher_a_propos)

    def creer_affichage(self):
        """Crée l'affichage de la calculatrice"""

        self.frame_affichage = tk.Frame(self.root, bg="#1C1C1E", height=100)
        self.frame_affichage.pack(fill="both", padx=8, pady=(15, 5))

        self.label_expression = tk.Label(
            self.frame_affichage,
            text="",
            font=("Segoe UI", 11),
            bg="#1C1C1E",
            fg="#8E8E93",
            anchor="e",
            height=1
        )
        self.label_expression.pack(fill="x", padx=5)

        self.label_resultat = tk.Label(
            self.frame_affichage,
            textvariable=self.resultat,
            font=("Segoe UI", 34, "bold"),
            bg="#1C1C1E",
            fg="#FFFFFF",
            anchor="e",
            height=1
        )
        self.label_resultat.pack(fill="x", padx=5)

        self.separator = tk.Frame(self.frame_affichage, bg="#2C2C2E", height=1)
        self.separator.pack(fill="x", pady=6)

    def creer_boutons(self):
        """Crée les boutons de la calculatrice"""

        self.frame_boutons = tk.Frame(self.root, bg="#1C1C1E")
        self.frame_boutons.pack(expand=True, fill="both", padx=8, pady=8)

        # Configuration compacte
        self.boutons_config = [
            # Ligne 1 : Mémoire
            ("MC", "mc", "#3A3A3C", "#4A4A4C"),
            ("MR", "mr", "#3A3A3C", "#4A4A4C"),
            ("M+", "mplus", "#3A3A3C", "#4A4A4C"),
            ("M-", "mminus", "#3A3A3C", "#4A4A4C"),

            ("√", "racine", "#3A3A3C", "#4A4A4C"),
            ("x²", "carre", "#3A3A3C", "#4A4A4C"),
            ("1/x", "inverse", "#3A3A3C", "#4A4A4C"),
            ("C", "efface", "#FF3B30", "#FF554A"),

            # Ligne 2
            ("C", "effacer", "#FF3B30", "#FF554A"),
            ("±", "negatif", "#3A3A3C", "#4A4A4C"),
            ("%", "pourcent", "#3A3A3C", "#4A4A4C"),
            ("÷", "/", "#FF9500", "#FFA833"),

            # Ligne 3

            ("7", "7", "#2C2C2E", "#3A3A3C"),
            ("8", "8", "#2C2C2E", "#3A3A3C"),
            ("9", "9", "#2C2C2E", "#3A3A3C"),
            ("×", "*", "#FF9500", "#FFA833"),

            # Ligne 4

            ("4", "4", "#2C2C2E", "#3A3A3C"),
            ("5", "5", "#2C2C2E", "#3A3A3C"),
            ("6", "6", "#2C2C2E", "#3A3A3C"),
            ("-", "-", "#FF9500", "#FFA833"),

            # Ligne 5

            ("1", "1", "#2C2C2E", "#3A3A3C"),
            ("2", "2", "#2C2C2E", "#3A3A3C"),
            ("3", "3", "#2C2C2E", "#3A3A3C"),
            ("+", "+", "#FF9500", "#FFA833"),

            # Ligne 6
            ("0", "0", "#2C2C2E", "#3A3A3C", 2),
            (".", ".", "#2C2C2E", "#3A3A3C"),
            ("=", "egal", "#FF9500", "#FFA833"),
        ]

        self.creer_grille_boutons()

    def creer_grille_boutons(self):
        """Crée la grille de boutons"""
        row = 0
        col = 0
        self.boutons = {}

        for bouton in self.boutons_config:
            if len(bouton) == 5:
                texte, commande, couleur, hover, colspan = bouton
            else:
                texte, commande, couleur, hover = bouton
                colspan = 1

            btn = tk.Button(
                self.frame_boutons,
                text=texte,
                font=("Segoe UI", 13, "bold"),
                bg=couleur,
                fg="#FFFFFF",
                relief="flat",
                cursor="hand2",
                command=lambda cmd=commande: self.click(cmd) if cmd != "egal" else self.calculer()
            )

            btn.bind("<Enter>", lambda e, b=btn, c=hover: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=couleur: b.config(bg=c))

            btn.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3, sticky="nsew")

            self.boutons[commande] = btn

            col += colspan
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            self.frame_boutons.grid_columnconfigure(i, weight=1)

        for i in range(6):
            self.frame_boutons.grid_rowconfigure(i, weight=1)

    def lier_clavier(self):
        """Lie les touches du clavier"""
        self.root.bind("<Key>", self.touche_clavier)

    def touche_clavier(self, event):
        """Gère les touches du clavier"""
        touche = event.char

        if touche in "0123456789.":
            self.click(touche)
        elif touche in "+-*/":
            self.click(touche)
        elif touche == "\r":
            self.calculer()
        elif touche == "\x08":
            self.effacer_dernier()
        elif touche == "c" or touche == "C":
            self.click("effacer")

    def click(self, valeur):
        """Gère les clics sur les boutons"""
        if valeur == "effacer":
            self.expression = ""
            self.resultat.set("0")
            self.label_expression.config(text="")
            return

        if valeur == "negatif":
            if self.expression and self.expression[0] == "-":
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.resultat.set(self.expression)
            return

        if valeur == "pourcent":
            try:
                nombre = float(self.expression)
                self.expression = str(nombre / 100)
                self.resultat.set(self.expression)
            except:
                pass
            return

        if valeur == "racine":
            try:
                nombre = float(self.expression)
                result = math.sqrt(nombre)
                self.expression = str(round(result, 10))
                self.resultat.set(self.expression)
                self.label_expression.config(text=f"√({nombre}) =")
            except:
                self.resultat.set("Erreur")
            return

        if valeur == "carre":
            try:
                nombre = float(self.expression)
                result = nombre ** 2
                self.expression = str(round(result, 10))
                self.resultat.set(self.expression)
                self.label_expression.config(text=f"({nombre})² =")
            except:
                self.resultat.set("Erreur")
            return

        if valeur == "inverse":
            try:
                nombre = float(self.expression)
                if nombre == 0:
                    self.resultat.set("Erreur")
                    self.label_expression.config(text="Division par zéro !")
                    return
                result = 1 / nombre
                self.expression = str(round(result, 10))
                self.resultat.set(self.expression)
                self.label_expression.config(text=f"1/({nombre}) =")
            except:
                self.resultat.set("Erreur")
            return

        if valeur == "mc":
            self.memoire = 0
            return

        if valeur == "mr":
            self.expression = str(self.memoire)
            self.resultat.set(self.expression)
            return

        if valeur == "mplus":
            try:
                self.memoire += float(self.expression)
            except:
                pass
            return

        if valeur == "mminus":
            try:
                self.memoire -= float(self.expression)
            except:
                pass
            return

        self.expression += valeur
        self.resultat.set(self.expression)

    def effacer_dernier(self):
        """Efface le dernier caractère"""
        self.expression = self.expression[:-1]
        if not self.expression:
            self.expression = "0"
        self.resultat.set(self.expression)

    def calculer(self):
        """Calcule le résultat"""
        try:
            expression = self.expression.replace("×", "*").replace("÷", "/")
            self.label_expression.config(text=self.expression + " =")
            result = eval(expression)

            if isinstance(result, float):
                result = round(result, 10)
                if result.is_integer():
                    result = int(result)

            self.historique.append(f"{self.expression} = {result}")
            self.resultat.set(str(result))
            self.expression = str(result)

        except ZeroDivisionError:
            self.resultat.set("Erreur")
            self.expression = ""
            self.label_expression.config(text="⚠️ Division par 0 !")
        except Exception:
            self.resultat.set("Erreur")
            self.expression = ""
            self.label_expression.config(text="⚠️ Invalide")

    def reinitialiser(self):
        """Réinitialise tout"""
        self.expression = ""
        self.resultat.set("0")
        self.label_expression.config(text="")
        self.memoire = 0

    def afficher_historique(self):
        """Affiche l'historique"""
        if not self.historique:
            messagebox.showinfo("📋 Historique", "Aucun calcul.")
            return
        historique_text = "\n".join(self.historique[-20:])
        messagebox.showinfo("📋 Historique", historique_text)

    def theme_sombre_mode(self):
        """Thème sombre"""
        self.theme_sombre = True
        self.root.configure(bg="#1C1C1E")
        self.frame_affichage.configure(bg="#1C1C1E")
        self.label_expression.config(bg="#1C1C1E", fg="#8E8E93")
        self.label_resultat.config(bg="#1C1C1E", fg="#FFFFFF")
        self.separator.config(bg="#2C2C2E")
        self.frame_boutons.configure(bg="#1C1C1E")

        for btn in self.frame_boutons.winfo_children():
            if isinstance(btn, tk.Button):
                texte = btn.cget("text")
                if texte in "0123456789.":
                    btn.config(bg="#2C2C2E", fg="#FFFFFF")
                elif texte in "+-×÷":
                    btn.config(bg="#FF9500", fg="#FFFFFF")
                elif texte == "=":
                    btn.config(bg="#FF9500", fg="#FFFFFF")
                elif texte in "C":
                    btn.config(bg="#FF3B30", fg="#FFFFFF")
                else:
                    btn.config(bg="#3A3A3C", fg="#FFFFFF")

    def theme_clair_mode(self):
        """Thème clair"""
        self.theme_sombre = False
        self.root.configure(bg="#F2F2F7")
        self.frame_affichage.configure(bg="#F2F2F7")
        self.label_expression.config(bg="#F2F2F7", fg="#8E8E93")
        self.label_resultat.config(bg="#F2F2F7", fg="#1C1C1E")
        self.separator.config(bg="#E5E5EA")
        self.frame_boutons.configure(bg="#F2F2F7")

        for btn in self.frame_boutons.winfo_children():
            if isinstance(btn, tk.Button):
                texte = btn.cget("text")
                if texte in "0123456789.":
                    btn.config(bg="#FFFFFF", fg="#1C1C1E")
                elif texte in "+-×÷":
                    btn.config(bg="#FF9500", fg="#FFFFFF")
                elif texte == "=":
                    btn.config(bg="#FF9500", fg="#FFFFFF")
                elif texte in "C":
                    btn.config(bg="#FF3B30", fg="#FFFFFF")
                else:
                    btn.config(bg="#E5E5EA", fg="#1C1C1E")

    def afficher_aide(self):
        """Affiche l'aide"""
        aide_text = """
🧮 Calculatrice - Aide

🔢 Chiffres : 0-9, virgule
➕ Opérations : +, -, ×, ÷
📐 Fonctions : √, x², 1/x, %
💾 Mémoire : MC, MR, M+, M-

⌨️ Raccourcis :
• 0-9 : Chiffres
• + - * / : Opérateurs
• Entrée : Calculer
• Backspace : Effacer
• C : Tout effacer
"""
        messagebox.showinfo("📖 Aide", aide_text)

    def afficher_a_propos(self):
        """Affiche les informations"""
        messagebox.showinfo(
            "ℹ️ À propos",
            "🧮 Calculatrice\n"
            "Version 2.0\n"
            "Python + Tkinter \n"
            "Projet GUI python cree par Henri (2026)"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatricePro(root)
    root.mainloop()