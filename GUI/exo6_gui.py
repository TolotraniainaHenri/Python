# Fenêtres multiples et boîtes de dialogue
import tkinter as tk
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre principale")
        self.geometry("300x150")

        self.label = tk.Label(self, text="Message reçu : Aucun")
        self.label.pack(pady=10)

        btn_ouvrir = tk.Button(self, text="Ouvrir la saisie", command=self.ouvrir_saisie)
        btn_ouvrir.pack(pady=10)

        # Gestion de la fermeture
        self.protocol("WM_DELETE_WINDOW", self.quitter)

    def ouvrir_saisie(self):
        # Fenêtre secondaire
        self.fenetre_saisie = tk.Toplevel(self)
        self.fenetre_saisie.title("Saisie")
        self.fenetre_saisie.geometry("250x100")

        entry = tk.Entry(self.fenetre_saisie, width=30)
        entry.pack(pady=10)

        def valider():
            texte = entry.get()
            self.label.config(text=f"Message reçu : {texte}")
            self.fenetre_saisie.destroy()

        btn_valider = tk.Button(self.fenetre_saisie, text="Valider", command=valider)
        btn_valider.pack()

    def quitter(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?"):
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()