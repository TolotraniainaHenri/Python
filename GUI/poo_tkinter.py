#Programmation orientée objet avec Tkinter
import tkinter as tk

class CompteurApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compteur")
        self.compteur = 0

        # Label
        self.label = tk.Label(self, text="Compteur : 0", font=("Arial", 16))
        self.label.pack(pady=10)

        # Boutons
        btn_plus = tk.Button(self, text="+1", command=self.incrementer)
        btn_plus.pack(pady=5)

        btn_moins = tk.Button(self, text="-1", command=self.decrementer)
        btn_moins.pack(pady=5)

        btn_reset = tk.Button(self, text="Réinitialiser", command=self.reinitialiser)
        btn_reset.pack(pady=5)

    def incrementer(self):
        self.compteur += 1
        self.maj_label()

    def decrementer(self):
        self.compteur -= 1
        self.maj_label()

    def reinitialiser(self):
        self.compteur = 0
        self.maj_label()

    def maj_label(self):
        self.label.config(text=f"Compteur : {self.compteur}")

if __name__ == "__main__":
    app = CompteurApp()
    app.mainloop()