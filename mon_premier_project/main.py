#========================================= VARIABLE ===================================
"""
Demande de nom et age
Il connait automatiquement le nom de la variable

str(34) => "34"
int("34") => 34

nom = input("Quel est ton nom ?")
age = input("Quel est ton age ?")

try :
     age_prochain = int(age) + 3
     print("Mon pronchaine age est " + str(age_prochain))
except:
     print("ERREUR :Vous devez convertir age to int ")
else:
    print("Vous vous appelez " + nom + "vous avez" + age + "ans")
    print("L'ans prochain , l'ans prochain " + str(age_prochain) + "ans")

print(type(age_prochain))
print(type(age))
print(type(nom))
"""
#==================================== BOUCLE  = "tant que" =================================

n = 0        #creer la variable
# print(n)
#n = 8      #reaffecter la variable
# print(n)
# n = n + 1      #incrementer
# print(n)

# while n < 10:
#     print("La valeur n est " + str(n))
#     n += 1
#
# print("Fin de la boucle")
#-----------------------------------------------------------------------------
# mot_de_passe = ""
# while not mot_de_passe == "henri1234":
#     mot_de_passe= input("Quel est votre mot de passe?")
#
# print("Mot de passe corect , vous avez un acces au compte")

#------------------------------------------------------------------------------
""" 
nom = ""
age_prochain = 0

while nom == "":
    nom = input("Quel est ton nom ?")
while age_prochain == 0 :
    age = input("Quel est ton age ?")
    try :
        age_prochain = int(age) + 1
    except:
        print("ERREUR :Vous devez convertir age to int ")

print("Vous vous appelez " + nom + ", vous avez " + age + "ans")
print("L'ans prochain , vous aurez " + str(age_prochain) + "ans")
"""
#==================================== FONCTION =================================
"""
nom = ""
age_prochain = 0

def demander_nom():
    global nom
    while nom == "":
        nom = input("Quel est ton nom ?")
    return nom

def demander_age():
    global age_prochain
    while age_prochain == 0:
        age = input("Quel est ton age ?")
        try:
            age_prochain = int(age) + 1
        except:
            print("ERREUR :Vous devez convertir age to int ")
        return age
nom = demander_nom()
age = demander_age()

print("Vous vous appelez " + nom + ", vous avez " + age + "ans")
"""

#================================= Boolean et Condition ==========================

# condition = int(age) >= 18
#
# print(condition)
# if condition == True:
#     print(nom + ", vous etes mageur!")
# else:
#     print(nom+ ", vous etes mineur!")

#-------------------------------------------------------------
#
# if int(age) == 1 or int(age) == 2 :
#     print("vous etes un bebe")
# elif int(age) >= 12 and int(age) <= 18 :
#     print("vous etes adolescent")
# elif int(age) >= 18:
#     print("vous etes majeur ")
# else :
#     print("vous etes mineur")

#-------------------------------- boucle for --------------------------
for i in range(0,5):
    print(i)
#------------------------------- float -------------
taille = 1.80
nom = "henri"
print(type(taille))
print("votre taille est " + str(taille))
print(f"Votre nom est : {nom}")
print("Votre taille + 1  est %s , %s "% (str(taille + 1),nom ))

print("je m'appelle" , "Henri" " et j'ai " ,26 ,"ans")