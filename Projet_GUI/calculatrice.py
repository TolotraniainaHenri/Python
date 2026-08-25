import tkinter as tk
from tkinter import ttk
import math


class CalculatriceModerne:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculatrice Pro")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1C1C1E")

        # Variable pour stocker l'expression
        self.expression = ""
        self.resultat = tk.StringVar()
        self.resultat.set("0")

        # Création de l'interface
        self.creer_affichage()
        self.creer_boutons()

    def creer_affichage(self):
        """Crée l'affichage de la calculatrice"""

        # Cadre pour l'affichage
        frame_affichage = tk.Frame(self.root, bg="#1C1C1E", height=120)
        frame_affichage.pack(fill="both", padx=10, pady=(20, 10))

        # Label pour l'expression (ce qui est en cours de calcul)
        self.label_expression = tk.Label(
            frame_affichage,
            text="",
            font=("Arial", 14),
            bg="#1C1C1E",
            fg="#8E8E93",
            anchor="e",
            height=1
        )
        self.label_expression.pack(fill="x", padx=5)

        # Label pour le résultat (grand)
        self.label_resultat = tk.Label(
            frame_affichage,
            textvariable=self.resultat,
            font=("Arial", 40, "bold"),
            bg="#1C1C1E",
            fg="#FFFFFF",
            anchor="e",
            height=1
        )
        self.label_resultat.pack(fill="x", padx=5)

        # Ligne de séparation
        separator = tk.Frame(frame_affichage, bg="#2C2C2E", height=2)
        separator.pack(fill="x", pady=10)

    def creer_boutons(self):
        """Crée les boutons de la calculatrice"""

        # Configuration des couleurs
        couleurs = {
            "bg": "#1C1C1E",
            "btn_num": "#2C2C2E",
            "btn_num_hover": "#3A3A3C",
            "btn_op": "#FF9500",
            "btn_op_hover": "#FFA833",
            "btn_func": "#3A3A3C",
            "btn_func_hover": "#4A4A4C",
            "btn_egal": "#FF9500",
            "btn_egal_hover": "#FFA833",
            "btn_effacer": "#FF3B30",
            "btn_effacer_hover": "#FF554A"
        }

        # Cadre principal des boutons
        frame_boutons = tk.Frame(self.root, bg="#1C1C1E")
        frame_boutons.pack(expand=True, fill="both", padx=10, pady=10)

        # Configuration des boutons
        boutons = [
            # Ligne 1 : Fonctions
            ("C", "effacer", couleurs["btn_effacer"], couleurs["btn_effacer_hover"]),
            ("±", "negatif", couleurs["btn_func"], couleurs["btn_func_hover"]),
            ("%", "pourcent", couleurs["btn_func"], couleurs["btn_func_hover"]),
            ("÷", "/", couleurs["btn_op"], couleurs["btn_op_hover"]),

            # Ligne 2 : Chiffres + opérateurs
            ("7", "7", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("8", "8", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("9", "9", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("×", "*", couleurs["btn_op"], couleurs["btn_op_hover"]),

            # Ligne 3
            ("4", "4", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("5", "5", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("6", "6", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("-", "-", couleurs["btn_op"], couleurs["btn_op_hover"]),

            # Ligne 4
            ("1", "1", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("2", "2", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("3", "3", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("+", "+", couleurs["btn_op"], couleurs["btn_op_hover"]),

            # Ligne 5 : 0, virgule, égal
            ("0", "0", couleurs["btn_num"], couleurs["btn_num_hover"], 2),
            (".", ".", couleurs["btn_num"], couleurs["btn_num_hover"]),
            ("=", "egal", couleurs["btn_egal"], couleurs["btn_egal_hover"]),
        ]

        # Création des boutons dans une grille
        row = 0
        col = 0
        for bouton in boutons:
            if len(bouton) == 5:  # Bouton avec colspan
                texte, commande, couleur, hover, colspan = bouton
            else:
                texte, commande, couleur, hover = bouton
                colspan = 1

            btn = tk.Button(
                frame_boutons,
                text=texte,
                font=("Arial", 18, "bold"),
                bg=couleur,
                fg="#FFFFFF",
                relief="flat",
                cursor="hand2",
                command=lambda cmd=commande: self.click(cmd) if cmd != "egal" else self.calculer()
            )

            # Effet hover
            btn.bind("<Enter>", lambda e, b=btn, c=hover: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=couleur: b.config(bg=c))

            # Placement dans la grille
            btn.grid(row=row, column=col, columnspan=colspan, padx=4, pady=4, sticky="nsew")

            col += colspan
            if col > 3:
                col = 0
                row += 1

        # Ajuster les colonnes pour qu'elles soient égales
        for i in range(4):
            frame_boutons.grid_columnconfigure(i, weight=1)

        # Ajuster les lignes pour qu'elles soient égales
        for i in range(5):
            frame_boutons.grid_rowconfigure(i, weight=1)

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

        # Ajouter la valeur à l'expression
        self.expression += valeur
        self.resultat.set(self.expression)

    def calculer(self):
        """Calcule le résultat de l'expression"""
        try:
            # Remplacer × et ÷ par * et / pour le calcul
            expression = self.expression.replace("×", "*").replace("÷", "/")

            # Afficher l'expression complète
            self.label_expression.config(text=self.expression + " =")

            # Calculer le résultat
            result = eval(expression)

            # Arrondir pour éviter les erreurs de flottants
            if isinstance(result, float):
                result = round(result, 10)
                # Si c'est un entier, le montrer comme entier
                if result.is_integer():
                    result = int(result)

            # Afficher le résultat
            self.resultat.set(str(result))
            self.expression = str(result)

        except ZeroDivisionError:
            self.resultat.set("Erreur")
            self.expression = ""
            self.label_expression.config(text="Division par zéro !")
        except Exception:
            self.resultat.set("Erreur")
            self.expression = ""
            self.label_expression.config(text="Expression invalide")


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatriceModerne(root)
    root.mainloop()