#Saisie et affichage avec événements
import tkinter as tk

def afficher():
    texte = entry.get()
    label_resultat.config(text=texte)
    entry.delete(0, tk.END)  # vide le champ

root = tk.Tk()
root.title("Saisie et affichage")

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Liaison de la touche Entrée (Return) dans le champ de saisie
entry.bind("<Return>", lambda event: afficher())

btn = tk.Button(root, text="Afficher", command=afficher)
btn.pack(pady=5)

label_resultat = tk.Label(root, text="")
label_resultat.pack(pady=5)

root.mainloop()