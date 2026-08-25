import numpy as np

# Création des matrices
A = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

B = np.array([
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
])

# Addition
print("Somme (NumPy) :\n", A + B)

# Multiplication
print("Multiplication (NumPy) :\n", A @ B)  # ou np.matmul(A, B)

# Déterminant
print("Déterminant (NumPy) :", np.linalg.det(A))

# Autres opérations utiles
print("Transposée :\n", A.T)
print("Inverse :\n", np.linalg.inv(A))  # Si dét ≠ 0
print("Trace (somme diagonale) :", np.trace(A))