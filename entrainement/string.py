""" 
7. TABLEAU RÉCAPITULATIF COMPLET 📊
Fonction	Description	Exemple	Résultat
+	Concaténation	"a"+"b"	"ab"
*	Répétition	"a"*3	"aaa"
len()	Longueur	len("abc")	3
in	Contient	"b" in "abc"	True
find()	Cherche position	"abc".find("b")	1
index()	Cherche position (erreur si absent)	"abc".index("b")	1
count()	Compte occurrences	"aaa".count("a")	3
upper()	Majuscules	"abc".upper()	"ABC"
lower()	Minuscules	"ABC".lower()	"abc"
capitalize()	1ère en majuscule	"abc".capitalize()	"Abc"
title()	Chaque mot en majuscule	"abc def".title()	"Abc Def"
swapcase()	Inverse la casse	"AbC".swapcase()	"aBc"
strip()	Enlève les espaces début/fin	" a ".strip()	"a"
lstrip()	Enlève à gauche	" a ".lstrip()	"a "
rstrip()	Enlève à droite	" a ".rstrip()	" a"
replace()	Remplace	"abc".replace("b","z")	"azc"
split()	Coupe en liste	"a,b".split(",")	['a','b']
join()	Joint une liste	",".join(['a','b'])	"a,b"
startswith()	Commence par	"abc".startswith("a")	True
endswith()	Fini par	"abc".endswith("c")	True
isalpha()	Que des lettres	"abc".isalpha()	True
isdigit()	Que des chiffres	"123".isdigit()	True
isalnum()	Lettres ou chiffres	"a1".isalnum()	True
islower()	Toutes minuscules	"abc".islower()	True
isupper()	Toutes majuscules	"ABC".isupper()	True
isspace()	Que des espaces	" ".isspace()	True
istitle()	Chaque mot en majuscule	"Abc Def".istitle()	True
center()	Centrer	"a".center(5,"-")	"--a--"
ljust()	Aligner à gauche	"a".ljust(3,"-")	"a--"
rjust()	Aligner à droite	"a".rjust(3,"-")	"--a"
zfill()	Remplir de zéros	"42".zfill(5)	"00042"
partition()	Diviser en 3	"a-b".partition("-")	('a','-','b')
"""
#========================================= 📌 RAPPEL : Les chaînes sont IMMUTABLES
s = "Bonjour Python"
# s[0] = "b"  # ❌ ERREUR ! On ne peut pas modifier 

#======= 1. CRÉATION ET CONCATÉNATION
# =================== 1.1 Concaténation (+)
s1 = "Bonjour"
s2 = "Python"
resultat = s1 + " " + s2  # "Bonjour Python"
print(resultat)

#======================1.2 Répétition (*)
s = "Ha" * 3  # "HaHaHa"
print(s)

#====================== 1.3 Joindre une liste (join)
liste = ["Python", "est", "super"]
resultat = " ".join(liste)  # "Python est super"
print(resultat)

# Séparateur personnalisé
resultat = ",".join(liste)  # "Python,est,super"

#=================== 1.4 F-strings (formatage moderne) ⭐
nom = "Alice"
age = 30
print(f"Bonjour {nom}, tu as {age} ans")  # "Bonjour Alice, tu as 30 ans"

# Avec expressions
print(f"Dans 5 ans, tu auras {age + 5} ans")  # "Dans 5 ans, tu auras 35 ans"

# Formatage des nombres
prix = 19.99
print(f"Prix : {prix:.2f} €")  # "Prix : 19.99 €"

#================== 1.5 Formatage à l'ancienne (.format)

print("Bonjour {}, tu as {} ans".format("Alice", 30))
print("Bonjour {nom}, tu as {age} ans".format(nom="Alice", age=30))

#====================2. ACCÈS ET RECHERCHE
#========================= 2.1 Accès par index
s = "Python"
print(s[0])    # 'P' (premier)
print(s[-1])   # 'n' (dernier)
print(s[-2])   # 'o' (avant-dernier)
#======================== 2.2 Slicing (tranches) ⭐

s = "Bonjour Python"

# [début:fin:pas]
print(s[0:7])      # "Bonjour" (de 0 à 6)
print(s[:7])       # "Bonjour" (jusqu'à 6)
print(s[8:])       # "Python" (de 8 à la fin)
print(s[::2])      # "Bnu yhn" (un caractère sur 2)
print(s[::-1])     # "nohtyP ruojnoB" (inversé)
print(s[8:14])     # "Python"


#================= 2.3 Longueur (len)
s = "Python"
print(len(s))  # 6

#==================== 2.4 Vérifier si contient (in / not in)
s = "Bonjour Python"
print("Python" in s)      # True
print("Java" in s)        # False
print("java" not in s)    # True (sensible à la casse)

#===================== 2.5 Trouver une position (find / index)
s = "Bonjour Python Python"

# find (retourne -1 si pas trouvé)
print(s.find("Python"))      # 8 (première occurrence)
print(s.find("Python", 10))  # 15 (à partir de l'index 10)
print(s.find("Java"))        # -1

# index (lève une exception si pas trouvé)
print(s.index("Python"))     # 8
# print(s.index("Java"))     # ValueError

#=================== 2.6 Compter les occurrences (count)

s = "Bonjour Python Python"
print(s.count("Python"))  # 2
print(s.count("o"))       # 3

#====================== 2.7 Vérifier le début et la fin (startswith / endswith)
s = "Bonjour Python"
print(s.startswith("Bon"))   # True
print(s.startswith("bon"))   # False (sensible à la casse)
print(s.endswith("thon"))    # True
print(s.endswith("py"))      # False

#==================== 3. MODIFICATION (RETOURNE UNE NOUVELLE CHAÎNE)
#===========================3.1 Mettre en majuscules/minuscules
s = "Bonjour Python"

print(s.upper())          # "BONJOUR PYTHON"
print(s.lower())          # "bonjour python"
print(s.capitalize())     # "Bonjour python" (1ère lettre en majuscule)
print(s.title())          # "Bonjour Python" (chaque mot en majuscule)
print(s.swapcase())       # "bONJOUR pYTHON" (inverse la casse)

#========================== 3.2 Supprimer les espaces ⭐
s = "  Hello World  "

print(s.strip())      # "Hello World" (début + fin)
print(s.lstrip())     # "Hello World  " (début seulement)
print(s.rstrip())     # "  Hello World" (fin seulement)

# Supprimer d'autres caractères
s = "---Hello---"
print(s.strip("-"))   # "Hello"

#========================= 3.3 Remplacer (replace)

s = "Bonjour Python"
print(s.replace("Python", "Java"))  # "Bonjour Java"
print(s.replace("o", "0"))          # "B0nj0ur Pyth0n"

# Remplacer plusieurs fois
s = "aaabbbccc"
print(s.replace("b", "B", 2))  # "aaaBBbccc" (seulement 2 fois)

#========================= 3.4 Mettre en liste (split) ⭐

s = "Bonjour Python est super"

# Couper par espaces
print(s.split())          # ['Bonjour', 'Python', 'est', 'super']

# Couper par un séparateur personnalisé
s = "1,2,3,4,5"
print(s.split(","))       # ['1', '2', '3', '4', '5']

# Limiter le nombre de coupes
print(s.split(",", 2))    # ['1', '2', '3,4,5'] (seulement 2 coupes)

# Split avec maxsplit
s = "pomme,poire,banane,orange"
print(s.split(",", 2))    # ['pomme', 'poire', 'banane,orange']

#========================= 3.5 Partitioner (partition)
s = "Bonjour-Python-2024"
print(s.partition("-"))   # ('Bonjour', '-', 'Python-2024')
print(s.rpartition("-"))  # ('Bonjour-Python', '-', '2024') (par la droite)

#=========================== 3.6 Remplir avec des espaces (center, ljust, rjust, zfill)

s = "42"

print(s.center(10))        # "    42    " (centré)
print(s.center(10, "-"))   # "----42----" (rempli de -)

print(s.ljust(10))         # "42        " (à gauche)
print(s.rjust(10))         # "        42" (à droite)

print(s.zfill(5))          # "00042" (remplit de zéros à gauche)







# ==================== 4. VÉRIFICATION DE CONTENU

#========================== 4.1 Vérifier les caractères
s = "123abc"

print(s.isalnum())   # True (lettres ET chiffres)
print(s.isalpha())   # False (contient des chiffres)
print(s.isdigit())   # False (contient des lettres)
print(s.isnumeric()) # False (idem)
print(s.isdecimal()) # False
print(s.islower())   # True (toutes minuscules)
print(s.isupper())   # False
print(s.isspace())   # False (pas que des espaces)
print(s.istitle())   # False (pas "123Abc")

#========================= 4.2 Vérifier pour l'affichage

s = "Bonjour\nPython"
print(s.isprintable())  # False (contient \n)

s = "Hello"
print(s.isprintable())  # True

#===========================5. TRANSFORMATIONS AVANCÉES ================= 
#===============================5.1 Inverser une chaîne ⭐ ===========================
s = "Python"
print(s[::-1])  # "nohtyP"

#========================= 5.2 Enlever les accents

import unicodedata

def enlever_accents(chaine):
    return ''.join(c for c in unicodedata.normalize('NFD', chaine)
                   if unicodedata.category(c) != 'Mn')

s = "éèêëàâôç"
print(enlever_accents(s))  # "eeeeaaoc"

#===============================5.3 Extraire les mots #===============================
import re
s = "Bonjour, Python! Comment ça va?"
mots = re.findall(r'\w+', s)
print(mots)  # ['Bonjour', 'Python', 'Comment', 'ça', 'va']

#=============================== 5.4 Inverser l'ordre des mots #===============================

s = "Bonjour Python est super"
mots = s.split()
mots_inverses = mots[::-1]
resultat = " ".join(mots_inverses)
print(resultat)  # "super est Python Bonjour"

##=============================== 5.5 Compter les mots #===============================

s = "Bonjour Python est super"
nb_mots = len(s.split())
print(nb_mots)  # 4

#=============================== 6. EXEMPLES PRATIQUES COMPLETS #===============================
#================= Exemple 1 : Nettoyer un texte

texte = "  Bonjour, Python! C'est SUPER.  "

# Nettoyage complet
propre = texte.strip()                    # Enlever les espaces
propre = propre.lower()                   # Tout en minuscules
propre = propre.replace("!", "")          # Enlever les ponctuations
propre = propre.replace(".", "")
propre = propre.replace(",", "")

print(propre)  # "bonjour python cest super"

#================= Exemple 2 : Extraire les données d'une chaîne formatée
donnees = "Alice,30,Paris,Boulanger"

# Méthode 1 : split
infos = donnees.split(",")
print(f"Nom: {infos[0]}, Âge: {infos[1]}, Ville: {infos[2]}, Métier: {infos[3]}")

# Méthode 2 : unpacking
nom, age, ville, metier = donnees.split(",")
print(f"{nom} a {age} ans et vit à {ville}")

# ================= Exemple 3 : Valider un email (simple)

def email_valide(email):
    return "@" in email and "." in email and email.count("@") == 1

print(email_valide("alice@email.com"))  # True
print(email_valide("alice@email"))      # False

#=================Exemple 4 : Transformer un nom en pseudo

def generer_pseudo(nom_prenom):
    # "Jean Dupont" -> "jdupont"
    parties = nom_prenom.lower().split()
    if len(parties) >= 2:
        return parties[0][0] + parties[1]  # jdupont
    return parties[0]

print(generer_pseudo("Jean Dupont"))  # "jdupont"