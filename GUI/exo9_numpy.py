#NumPy – Création et statistiques
import numpy as np
# 1. Matrice aléatoire 5x5 d'entiers entre 0 et 100 (inclus)
matrice = np.random.randint(0, 101, (5, 5))
print("Matrice :")
print(matrice)

# 2. Moyenne, écart-type, variance
moyenne = np.mean(matrice)
ecart_type = np.std(matrice)
variance = np.var(matrice)
print(f"Moyenne : {moyenne:.2f}")
print(f"Écart-type : {ecart_type:.2f}")
print(f"Variance : {variance:.2f}")

# 3. Somme de chaque ligne (axis=1)
sommes_lignes = np.sum(matrice, axis=1)
print("Somme par ligne :", sommes_lignes)

# 4. Sous-matrice lignes 1 à 3 et colonnes 2 à 4 (indices Python)
sous_matrice = matrice[1:4, 2:5]   # ligne 1,2,3 et colonne 2,3,4
print("Sous-matrice (lignes 1-3, colonnes 2-4) :")
print(sous_matrice)