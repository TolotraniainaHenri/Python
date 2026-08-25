#=============================== Déclaration et initialisation

# Vide
ma_liste = []

# Avec des valeurs
notes = [12, 15, 8, 19, 10]

# Avec des types mélangés (possible mais déconseillé)
mixte = [10, "bonjour", True, 3.14]

# Créer une liste de 5 zéros (comme new int[5] en Java/C#)
zeros = [0] * 5  # [0, 0, 0, 0, 0]

# Créer une liste avec une séquence (comme range())
nombres = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


#============================= Accès et modification =================
notes = [12, 15, 8, 19, 10]

# Accès (comme dans tous les langages)
print(notes[0])     # 12 (premier)
print(notes[-1])    # 10 (dernier ! pratique)
print(notes[-2])    # 19 (avant-dernier)

# Modification
notes[2] = 20       # [12, 15, 20, 19, 10]

# Ajouter à la fin (comme push en JS ou add en Java)
notes.append(14)    # [12, 15, 20, 19, 10, 14]

# Insérer à une position
notes.insert(1, 99) # [12, 99, 15, 20, 19, 10, 14]

# Supprimer par valeur
notes.remove(99)    # [12, 15, 20, 19, 10, 14]

# Supprimer par index (comme splice en JS)
del notes[0]        # [15, 20, 19, 10, 14]
notes.pop(2)        # retire l'index 2 (19) → [15, 20, 10, 14]
notes.pop()         # retire le dernier → [15, 20, 10]

#============== #Parcourir un tableau 1D =============================
notes = [12, 15, 8, 19, 10]

# Méthode 1 : Pour chaque élément (la plus Pythonique)
for note in notes:
    print(note)

# Méthode 2 : Avec index (comme en C/Java)
for i in range(len(notes)):
    print(f"Index {i} : {notes[i]}")

# Méthode 3 : Avec index ET valeur (très pratique)
for i, note in enumerate(notes):
    print(f"Position {i} = {note}")


#============================ 2. Tableau 2 Dimensions (Matrice) ========
#================================== Déclaration et initialisation ========
# Méthode 1 : Directement
matrice = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Méthode 2 : Matrice 3x3 remplie de zéros
zeros = [[0] * 3 for _ in range(3)]  
# Résultat : [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# ATTENTION PIÈGE ! Ne jamais faire ça :
# matrice = [[0] * 3] * 3  # ❌ C'est un piège ! Toutes les lignes pointent vers le même objet


#============================ Accès et modification ==================
matrice = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Accès (ligne, colonne) comme dans tous les langages
print(matrice[0][0])  # 1
print(matrice[1][2])  # 6
print(matrice[-1][-1])  # 9 (dernier élément)

# Modification
matrice[0][1] = 99
# Résultat : [[1, 99, 3], [4, 5, 6], [7, 8, 9]]

# Ajouter une ligne
matrice.append([10, 11, 12])
# Résultat : [[1, 99, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

# Ajouter une colonne (à chaque ligne)
for ligne in matrice:
    ligne.append(0)
# Résultat : [[1, 99, 3, 0], [4, 5, 6, 0], [7, 8, 9, 0], [10, 11, 12, 0]]


#==================================== Parcourir un tableau 2D ===========================
matrice = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Méthode 1 : Boucles imbriquées classiques
for i in range(len(matrice)):          # Pour chaque ligne
    for j in range(len(matrice[i])):   # Pour chaque colonne
        print(f"matrice[{i}][{j}] = {matrice[i][j]}")

# Méthode 2 : Plus Pythonique (par éléments)
for ligne in matrice:
    for valeur in ligne:
        print(valeur, end=" ")
    print()  # Saut de ligne après chaque ligne
# Affiche :
# 1 2 3
# 4 5 6
# 7 8 9

# Méthode 3 : Avec les index (enumerate)
for i, ligne in enumerate(matrice):
    for j, valeur in enumerate(ligne):
        print(f"Ligne {i}, Col {j} = {valeur}")

#============================== Opérations utiles sur les tableaux =============
# Tableau 1D
notes = [12, 15, 8, 19, 10]

# Longueur (comme .length en Java/JS)
print(len(notes))  # 5

# Trier (modifie le tableau d'origine)
notes.sort()           # [8, 10, 12, 15, 19]
notes.sort(reverse=True)  # [19, 15, 12, 10, 8]

# Trier sans modifier (retourne une nouvelle liste)
triee = sorted(notes)  # nouvelle liste triée

# Minimum, maximum, somme
print(min(notes))  # 8
print(max(notes))  # 19
print(sum(notes))  # 64

# Vérifier si un élément existe (comme .contains en Java)
print(15 in notes)   # True
print(99 in notes)   # False

# Concaténer deux listes (comme concat en JS)
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b  # [1, 2, 3, 4, 5, 6]

# Répéter une liste
zero = [0] * 5  # [0, 0, 0, 0, 0]

# Tableau 2D : nombre de lignes et colonnes
matrice = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
nb_lignes = len(matrice)         # 3
nb_colonnes = len(matrice[0])    # 3 (si toutes les lignes ont la même taille)