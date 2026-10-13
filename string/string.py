s = "Bonjour Python" \
""
print(s[1])

#======================= Concatenation =============
s1 = "Bonjour"
s2 = "Python"
resultat = s1 + " " + s2    #Bonjour Python
print(resultat) 
#===================== Repetion =================
s = "Ha" * 3
print(s)

#===================== Joindre une liste =========
liste = ["Python", "est", "super"]
resultat = " ".join(liste)
print(resultat)     #Python est super

#=================== Formatage moderne ============
nom = " Henri"
age = 25 
print(f"Bonjour {nom}, tu as {age} ans") 
print(f"apres 4ans , Tu auras {age + 4} ans ")

prix = 19.9944233333333
print(f"Prix : {prix :.3f} ")

#===================== Formatage a l'acienne (.format) =========== 
print("Bonjour {}, tu as {} ans ".format("Henri","26"))
print("Bonjour {nom}, tu as {age} ans ".format(nom = "Henri", age = 26))

#==================== Acces par index =============
s = "Python"
print(s[0])
print(s[1])
print(s[-0]) #n

#==================== Slicing (tranche)
# [debut:fin:pas]
s = "Bonjour Python"


print(s[0:10])   # Bonjour Py
print(s[8:])   # Python
print(s[::2])  #BoPo
print(s[::-1])  #nohtyP ruojnoB
print(s[8:14]) #Python

#=================== Longeur =========
print(len(s)) # 14

#=================== Verifier si contient =========
print("Python" in s)
print("K" in s)
print("Java" not in s)

#================ Trouver une position ======================
print(s.find("Python"))  #8
print(s.find("Python", 7))


#================ Compter les occurences =============
#print(s.count("Python"))  
#print(s.count("o"))

#=============== Verifier le debut et la fin =========
print(s.startswith("Py"))
print(s.endswith("on"))
#========== Mettre majuscule / miniscules =======

print(s.upper())  #BONJOUR PYTHON
print(s.lower())   #bonjour python
print(s.capitalize()) #Bonjour python
print(s.title())  #Bonjour Python
print(s.swapcase())  #bONJOUR pYTHON

