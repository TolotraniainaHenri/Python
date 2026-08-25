#Fenêtre minimale et boucle d’événements
import tkinter as tk

# Création de la fenêtre principale
x = tk.Tk()
x.title("Ma première GUI")
x.geometry("500x200")

# Label avec la police Arial 14, bleue
label = tk.Label(x,
                 text="Bienvenue dans le monde des interfaces graphiques !",
                 font=("Arial", 15),
                 fg="red",
                 bg="white")
label.pack(pady=40)

# Lancement de la boucle d'événements
x.mainloop()

