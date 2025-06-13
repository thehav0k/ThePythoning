#2D array or matrix operations

import numpy as np

# Create a 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("2D Array (Matrix):\n", matrix)

# Add 10 to each element
matrix += 10
print("Modified 2D Array:\n", matrix)

# Add a row at the end
new_row = np.array([10, 11, 12])
matrix = np.vstack((matrix, new_row))
print("Appended Row to 2D Array:\n", matrix)

# Add a column at the beginning
new_col = np.array([[0], [0], [0], [0]])
matrix = np.hstack((new_col, matrix))
print("Inserted Column at Beginning:\n", matrix)

# remove a row (e.g., the first row)
matrix = np.delete(matrix, 0, axis=0)
print("Removed First Row:\n", matrix)

# remove a column (e.g., the first column)
matrix = np.delete(matrix, 0, axis=1)
print("Removed First Column:\n", matrix)

# Adding two matrices
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
C = A + B
print("Sum of Two Matrices:\n", C)

# Subtracting two matrices
D = A - B
print("Difference of Two Matrices:\n", D)

# Element-wise multiplication of two matrices
E = A * B
print("Element-wise Multiplication of Two Matrices:\n", E)

# Matrix multiplication (dot product)
F = np.dot(A, B)
print("Matrix Multiplication (Dot Product):\n", F)

# Transpose of a matrix
G = np.transpose(A)
print("Transpose of Matrix A:\n", G)

# Determinant of a matrix
AA = np.array([[1, 2], [3, 4]])
det_A = np.linalg.det(AA)
print("Determinant of Matrix AA:", det_A)

# Inverse of a matrix
A = np.array([[1, 2], [3, 4]])
try:
    inv_A = np.linalg.inv(A)
    print("Inverse of Matrix A:\n", inv_A)
except np.linalg.LinAlgError:
    print("Matrix A is singular and cannot be inverted.")
## displaying matrix without brackets
def print_matrix(mat):
    for row in mat:
        print(" ".join(map(str, row)))

# Example usage of print_matrix
print("Formatted 2D Array (Matrix):")
print_matrix(matrix)

# Eigenvalues and Eigenvectors of a matrix
A = np.array([[4, -2], [1, 1]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues of Matrix A:", " ".join(map(str, eigenvalues)))
print("Eigenvectors of Matrix A:\n", eigenvectors)

# trace of a matrix
trace_A = np.trace(A)
print("Trace of Matrix A:", trace_A)

# Rank of a matrix
rank_A = np.linalg.matrix_rank(A)
print("Rank of Matrix A:", rank_A)

# Linear equations solver
A = np.array([[3, 2], [1, 4]])
b = np.array([5, 6])
try:
    solution = np.linalg.solve(A, b)
    print("Solution of Linear Equations Ax = b:", solution)
except np.linalg.LinAlgError:
    print("Matrix A is singular or not square, cannot solve the linear equations.")

# matrix norm
# I dont know wtf is matrix norm
matrix_norm = np.linalg.norm(A)
print("Norm of Matrix A:", matrix_norm)

# characteristics polynomial of a matrix
A = np.array([[1, 2], [3, 4]])
char_poly = np.poly(A)
print("Characteristic Polynomial of Matrix A:", char_poly)
# this is the coefficients of the polynomial in descending order of powers


 
## Now I understand why first semester e linear algebra porano hoichilo