#Grille et gestionnaire de géométrie

import tkinter as tk

def envoyer():
    nom = entry_nom.get()
    age = entry_age.get()
    ville = entry_ville.get()
    print(f"Nom: {nom}, Âge: {age}, Ville: {ville}")

root = tk.Tk()
root.title("Formulaire")

# Labels
label_nom = tk.Label(root, text="Nom :")
label_nom.grid(row=0, column=0, padx=5, pady=5, sticky="e")

label_age = tk.Label(root, text="Âge :")
label_age.grid(row=1, column=0, padx=5, pady=5, sticky="e")

label_ville = tk.Label(root, text="Ville :")
label_ville.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Champs de saisie
entry_nom = tk.Entry(root)
entry_nom.grid(row=0, column=1, padx=5, pady=5, sticky="w")

entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=5, pady=5, sticky="w")

entry_ville = tk.Entry(root)
entry_ville.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Bouton Envoyer (s'étend sur 2 colonnes)
btn = tk.Button(root, text="Envoyer", command=envoyer)
btn.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()