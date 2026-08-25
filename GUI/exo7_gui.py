import tkinter as tk

def mise_a_jour(*args):
    texte = var_texte.get()
    label_resultat.config(text=f"Vous tapez : {texte}")

root = tk.Tk()
root.title("Liaison de variables")

var_texte = tk.StringVar()
var_texte.trace_add("write", mise_a_jour)

entry = tk.Entry(root, textvariable=var_texte, width=30)
entry.pack(pady=10)

label_resultat = tk.Label(root, text="Vous tapez : ")
label_resultat.pack(pady=10)

root.mainloop()