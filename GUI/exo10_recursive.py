#2. Fonction récursive avec f‑strings
def factorial(n):
    print(f"Appel factorial({n})")
    if n <= 1:
        print(f"Retour de factorial({n}) = 1")
        return 1
    result = n * factorial(n - 1)
    print(f"Retour de factorial({n}) = {result}")
    return result

#3-Script de test et utilisation du débogueur
if __name__ == "__main__":
    n = 5
    print(f"Calcul de {n}!")
    f = factorial(n)
    print(f"Résultat : {f}")