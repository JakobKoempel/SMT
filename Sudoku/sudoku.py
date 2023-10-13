import z3
from itertools import combinations, product

solver = z3.Solver()
field = [[z3.Int("row" + str(i) + "col" + str(j)) for j in range(9)] for i in range(9)]

input = [[4, 5, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 2, 0, 7, 0, 6, 3, 0],
         [0, 0, 0, 0, 0, 0, 0, 2, 8],
         [0, 0, 0, 9, 5, 0, 0, 0, 0],
         [0, 8, 6, 0, 0, 0, 2, 0, 0],
         [0, 2, 0, 6, 0, 0, 7, 5, 0],
         [0, 0, 0, 0, 0, 0, 4, 7, 6],
         [0, 0, 0, 0, 4, 5, 0, 0, 0],
         [0, 0, 8, 0, 0, 9, 0, 0, 0]]

init = z3.And([field[i][j] == input[i][j] for (i,j) in product(range(9), range(9)) if input[i][j] != 0])
solver.add(init)

lowerBound = z3.And([1 <= x for row in field for x in row])
solver.add(lowerBound)
upperBound = z3.And([x <= 9 for row in field for x in row])
solver.add(upperBound)

for row in field:
    rowCon = z3.And([x != y for (x,y) in combinations(row, 2)])
    solver.add(rowCon)

for j in range(9):
    col = [field[i][j] for i in range(9)]
    colCon = z3.And([x != y for (x,y) in combinations(col, 2)])
    solver.add(colCon)

for row in [[0,1,2], [3,4,5], [6,7,8]]:
    for col in [[0,1,2], [3,4,5], [6,7,8]]:
        box = [field[i][j] for (i,j) in product(row, col)]
        boxCon = z3.And([x != y for (x,y) in combinations(box, 2)])
        solver.add(boxCon)

solver.check()
model = solver.model()

for i in range(9):
    print([model[field[i][j]] for j in range(9)])