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
	print(type(cofactors))
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

lk = [[1,0,0], [0,1,0], [0,0,1]]
kj = [[3,7,6,9,8,3], [4,0,2,2,-7,-4], [-2,2,1,0,0,4]]
print(getMatrixInverse(lk))
print(multiplyMatrix(lk, kj))