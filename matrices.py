import numpy as np
from fractions import Fraction

def getMatrixInverse(m):
	determinant = getMatrixDeterminant(m)
	# special case for 2x2 matrices
	if len(m) == 2:
		return [[m[1][1]/determinant, -1*m[0][1]/determinant], [-1*m[1][0]/determinant, m[0][0]/determinant]]
	# find matrix of cofactors
	cofactors = []
	for r in range(len(m)):
		cofactorRow = []
		for c in range(len(m)):
			minor = getMatrixMinor(m,r,c)
			cofactorRow.append(((-1)**(r+c)) * getMatrixDeterminant(minor))
		cofactors.append(cofactorRow)
	cofactors = transposeMatrix(cofactors)
	for r in range(len(cofactors)):
		for c in range(len(cofactors)):
			cofactors[r][c] = cofactors[r][c]/determinant
	return cofactors

def transposeMatrix(m):
	return [*map(list, zip(*m))]

def getMatrixMinor(m,i,j):
	return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def getMatrixDeterminant(m):
	# base case for 2x2 matrix
	if len(m) == 2:
		return m[0][0]*m[1][1] - m[0][1]*m[1][0]
	determinant = 0
	for c in range(len(m)):
		determinant += ((-1)**c)*m[0][c]*getMatrixDeterminant(getMatrixMinor(m,0,c))
	return determinant

def multiplyMatrix(a,b):
	zip_b = zip(*b)
	zip_b = list(zip_b)
	return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in zip_b] for row_a in a]

def addMatrix(c, d):
	return [[a+b for a,b in zip(row1,row2)] for row1, row2 in zip(c,d)]

# def swaprows(m, i, j):
# 	if len(m.shape) == 1:
# 		m[i],m[j] = m[j].m[i]
# 	else:
# 		temp = m[i].copy()
# 		m[i] = m[j]
# 		m[j] = temp

# def _gauss_det(m, eps = 1.0/(10**10)):
# 	m = np.array([[Fraction(int(x)) for x in row] for row in m])
# 	subs = 0
# 	(h, w) = (len(m), len(m[0]))
# 	for y in range(0,h):
# 		maxrow = y
# 		for y2 in range(y+1, h):    # Find max pivot
# 			if abs(m[y2][y]) > abs(m[maxrow][y]):
# 				maxrow = y2
# 		swaprows(m, y, maxrow)
# 		subs += 1
# 		if abs(m[y][y]) <= eps:     # Singular?
# 			print(m[y][y])
# 			return 0
# 		for y2 in range(y+1, h):    # Eliminate column y
# 			c = m[y2][y] / m[y][y]
# 			m[y2][y:w] -= m[y][y:w]*c
# 	prod = m.diagonal().prod()
# 	if subs%2:
# 		return prod
# 	return -prod

def _eig(m):
	w = np.linalg.eigvals(np.array(m))
	return w
