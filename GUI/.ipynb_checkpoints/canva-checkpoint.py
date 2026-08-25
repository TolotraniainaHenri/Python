# Canvas interactif
import tkinter as tk
import random

def dessiner_cercle(event):
    x, y = event.x, event.y
    couleur = random.choice(["red", "blue", "green"])
    canvas.create_oval(x-10, y-10, x+10, y+10, fill=couleur, outline=couleur)

def effacer():
    canvas.delete("all")

root = tk.Tk()
root.title("Canvas interactif")

canvas = tk.Canvas(root, width=500, height=400, bg="white")
canvas.pack(pady=10)

# Lier le clic gauche
canvas.bind("<Button-1>", dessiner_cercle)

btn_effacer = tk.Button(root, text="Effacer", command=effacer)
btn_effacer.pack(pady=5)

root.mainloop()