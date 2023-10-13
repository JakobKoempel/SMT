import z3

#constants to encode the 8 different corner pieces.
#these constants are also the index of the permutation array (perm) where the corner piece must go 
    #yellow green orange : 0
    #yellow green red : 1
    #yellow blue red : 2
    #yellow blue orange : 3
    #white green orange : 4
    #white green red : 5
    #white blue red : 6
    #white blue orange : 7

#constants to encode the 3 different orientations
    #the yellow or the white face points up or down : 0
    #the yellow or white face points front or back : 1
    #the yellow or white face points right or left : 2

#encode the solved configuation of the 2x2 cube
def defineSolved():
    permSolved = True
    for i in range(8):
        permSolved = z3.And(permSolved, perm_post[i] == i)
    oriSolved = True
    for i in range(8):
        oriSolved = z3.And(oriSolved, ori_post[i] == 0)
    return z3.And(permSolved, oriSolved)

def ori_change(pos_pre, pos_post, ori_0, ori_1, ori_2):
    return z3.And(  z3.Implies(ori_pre[pos_pre] == 0, ori_post[pos_post] == ori_0),
                    z3.Implies(ori_pre[pos_pre] == 1, ori_post[pos_post] == ori_1),
                    z3.Implies(ori_pre[pos_pre] == 2, ori_post[pos_post] == ori_2))

def ori_change_2(pos_pre, pos_post):
    return ori_change(pos_pre, pos_post, 0, 1, 2)

def ori_change_rl(pos_pre, pos_post):
    return ori_change(pos_pre, pos_post, 1, 0, 2)

def ori_change_ud(pos_pre, pos_post):
    return ori_change(pos_pre, pos_post, 0, 2, 1)

def ori_change_fb(pos_pre, pos_post):
    return ori_change(pos_pre, pos_post, 2, 1, 0)

def create_id(a, b, c, d):
    id = True
    id_list = [i for i in range(8) if i not in [a, b, c, d]]
    for i in id_list:
        id = z3.And(id, perm_pre[i] == perm_post[i], ori_pre[i] == ori_post[i])
    return id

def perm_change_1(a, b, c, d):
    perm = z3.And( perm_pre[d] == perm_post[a],  perm_pre[a] == perm_post[b],
                    perm_pre[b] == perm_post[c],  perm_pre[c] == perm_post[d])
    id = create_id(a, b, c, d)
    return z3.And(perm, id)

def perm_change_2(a, b, c, d):
    perm = z3.And( perm_pre[a] == perm_post[b],  perm_pre[b] == perm_post[a],
                    perm_pre[c] == perm_post[d],  perm_pre[d] == perm_post[c])
    id = create_id(a, b, c, d)
    return z3.And(perm, id)

def R():
    perm = perm_change_1(1, 5, 6, 2)
    ori_1 = ori_change_rl(2, 1)
    ori_5 = ori_change_rl(1, 5)
    ori_6 = ori_change_rl(5, 6)
    ori_2 = ori_change_rl(6, 2)

    return z3.And(perm, ori_1, ori_2, ori_5, ori_6, sol_pre + "R," == sol_post)

def Rp():
    perm = perm_change_1(2, 6, 5, 1)
    ori_2 = ori_change_rl(1, 2)
    ori_6 = ori_change_rl(2, 6)
    ori_5 = ori_change_rl(6, 5)
    ori_1 = ori_change_rl(5, 1)

    return z3.And(perm, ori_1, ori_5, ori_6, ori_2, sol_pre + "Rp," == sol_post)

def R2(): 
    perm = perm_change_2(1, 6, 2, 5)
    ori_6 = ori_change_2(1, 6)
    ori_1 = ori_change_2(6, 1)
    ori_2 = ori_change_2(5, 2)
    ori_5 = ori_change_2(2, 5)
    
    return z3.And(perm, ori_1, ori_5, ori_6, ori_2, sol_pre + "R2," == sol_post)

def L():
    perm = perm_change_1(0, 3, 7, 4)
    ori_0 = ori_change_rl(4, 0)
    ori_3 = ori_change_rl(0, 3)
    ori_7 = ori_change_rl(3, 7)
    ori_4 = ori_change_rl(7, 4)

    return z3.And(perm, ori_0, ori_3, ori_7, ori_4, sol_pre + "L," == sol_post)

def Lp():
    perm = perm_change_1(4, 7, 3, 0)
    ori_4 = ori_change_rl(0, 4)
    ori_7 = ori_change_rl(4, 7)
    ori_3 = ori_change_rl(7, 3)
    ori_0 = ori_change_rl(3, 0)

    return z3.And(perm, ori_0, ori_3, ori_7, ori_4, sol_pre + "Lp," == sol_post)

def L2():
    perm = perm_change_2(0, 7, 3, 4)
    ori_7 = ori_change_2(0, 7)
    ori_0 = ori_change_2(7, 0)
    ori_3 = ori_change_2(4, 3)
    ori_4 = ori_change_2(3, 4)

    return z3.And(perm, ori_0, ori_3, ori_7, ori_4, sol_pre + "L2," == sol_post)

def U():
    perm = perm_change_1(1, 2, 3, 0)
    ori_1 = ori_change_ud(0, 1)
    ori_2 = ori_change_ud(1, 2)
    ori_3 = ori_change_ud(2, 3)
    ori_0 = ori_change_ud(3, 0)

    return z3.And(perm, ori_0, ori_1, ori_2, ori_3, sol_pre + "U," == sol_post)

def Up():
    perm = perm_change_1(3, 2, 1, 0)
    ori_3 = ori_change_ud(0, 3)
    ori_2 = ori_change_ud(3, 2)
    ori_1 = ori_change_ud(2, 1)
    ori_0 = ori_change_ud(1, 0)

    return z3.And(perm, ori_0, ori_1, ori_2, ori_3, sol_pre + "Up," == sol_post)

def U2():
    perm = perm_change_2(0, 2, 1, 3)
    ori_2 = ori_change_2(0, 2)
    ori_0 = ori_change_2(2, 0)
    ori_3 = ori_change_2(1, 3)
    ori_1 = ori_change_2(3, 1)

    return z3.And(perm, ori_0, ori_1, ori_2, ori_3, sol_pre + "U2," == sol_post)

def Dp():
    perm = perm_change_1(5, 6, 7, 4)
    ori_5 = ori_change_ud(4, 5)
    ori_6 = ori_change_ud(5, 6)
    ori_7 = ori_change_ud(6, 7)
    ori_4 = ori_change_ud(7, 4)

    return z3.And(perm, ori_4, ori_5, ori_6, ori_7, sol_pre + "Dp," == sol_post)

def D():
    perm = perm_change_1(7, 6, 5, 4)
    ori_7 = ori_change_ud(4, 7)
    ori_6 = ori_change_ud(7, 6)
    ori_5 = ori_change_ud(6, 5)
    ori_4 = ori_change_ud(5, 4)

    return z3.And(perm, ori_4, ori_5, ori_6, ori_7, sol_pre + "D," == sol_post)

def D2():
    perm = perm_change_2(4, 6, 7, 5)
    ori_6 = ori_change_2(4, 6)
    ori_4 = ori_change_2(6, 4)
    ori_7 = ori_change_2(5, 7)
    ori_5 = ori_change_2(7, 5)

    return z3.And(perm, ori_4, ori_5, ori_6, ori_7, sol_pre + "D2," == sol_post)

def F():
    perm = perm_change_1(2, 6, 7, 3)
    ori_2 = ori_change_fb(3, 2)
    ori_6 = ori_change_fb(2, 6)
    ori_7 = ori_change_fb(6, 7)
    ori_3 = ori_change_fb(7, 3)

    return z3.And(perm, ori_2, ori_3, ori_6, ori_7, sol_pre + "F," == sol_post)

def Fp():
    perm = perm_change_1(7, 6, 2, 3)
    ori_7 = ori_change_fb(3, 7)
    ori_6 = ori_change_fb(7, 6)
    ori_2 = ori_change_fb(6, 2)
    ori_3 = ori_change_fb(2, 3)

    return z3.And(perm, ori_2, ori_3, ori_6, ori_7, sol_pre + "Fp," == sol_post)

def F2():
    perm = perm_change_2(3, 6, 2, 7)
    ori_6 = ori_change_2(3, 6)
    ori_3 = ori_change_2(6, 3)
    ori_2 = ori_change_2(7, 2)
    ori_7 = ori_change_2(2, 7)

    return z3.And(perm, ori_2, ori_3, ori_6, ori_7, sol_pre + "F2," == sol_post)

def B():
    perm = perm_change_1(4, 5, 1, 0)
    ori_4 = ori_change_fb(0, 4)
    ori_5 = ori_change_fb(4, 5)
    ori_1 = ori_change_fb(5, 1)
    ori_0 = ori_change_fb(1, 0)

    return z3.And(perm, ori_0, ori_1, ori_4, ori_5, sol_pre + "B," == sol_post)

def Bp():
    perm = perm_change_1(1, 5, 4, 0)
    ori_1 = ori_change_fb(0, 1)
    ori_5 = ori_change_fb(1, 5)
    ori_4 = ori_change_fb(5, 4)
    ori_0 = ori_change_fb(4, 0)

    return z3.And(perm, ori_0, ori_1, ori_4, ori_5, sol_pre + "Bp," == sol_post)

def B2():
    perm = perm_change_2(0, 6, 1, 4)
    ori_6 = ori_change_2(0, 6)
    ori_0 = ori_change_2(6, 0)
    ori_4 = ori_change_2(1, 4)
    ori_1 = ori_change_2(4, 1)

    return z3.And(perm, ori_0, ori_1, ori_6, ori_4, sol_pre + "B2," == sol_post)

def getStep(expr, step):
    perm_pre_new = z3.Array("perm" + "'" * step , z3.IntSort(), z3.IntSort())
    ori_pre_new = z3.Array("ori" + "'" * step, z3.IntSort(), z3.IntSort())
    sol_pre_new = z3.String("sol" + "'" * step)
    perm_post_new = z3.Array("perm" + "'" * (step + 1), z3.IntSort(), z3.IntSort())
    ori_post_new = z3.Array("ori" + "'" * (step + 1), z3.IntSort(), z3.IntSort())
    sol_post_new = z3.String("sol" + "'" * (step + 1))
    next = z3.substitute(expr, [(perm_post, perm_post_new), (ori_post, ori_post_new), (sol_post, sol_post_new), 
                                (perm_pre, perm_pre_new), (ori_pre, ori_pre_new), (sol_pre, sol_pre_new)])
    return next
    
def getInit(perm_init, ori_init):
    assert len(perm_init) == len(ori_init) == 8
    init = z3.String("sol") == ""
    for i in range(len(perm_init)):
        init = z3.And(init, perm_pre[i] == perm_init[i], ori_pre[i] ==  ori_init[i])
    return init
    

solver = z3.Solver()

perm_init = [0, 2, 3, 7, 1, 6, 4, 5]
ori_init = [0, 0, 2, 1, 2, 1, 0, 0]

perm_pre = z3.Array("perm", z3.IntSort(), z3.IntSort())
ori_pre = z3.Array("ori", z3.IntSort(), z3.IntSort())
sol_pre = z3.String("sol")
perm_post = z3.Array("perm'", z3.IntSort(), z3.IntSort())
ori_post = z3.Array("ori'", z3.IntSort(), z3.IntSort())
sol_post = z3.String("sol'")

init = getInit(perm_init, ori_init)
step = z3.Or(R(), Rp(), R2(), L(), Lp(), L2(), U(), Up(), U2(), D(), Dp(), D2(), F(), Fp(), F2(), B(), Bp(), B2())
solved = defineSolved()

solver.add(init)

for i in range(11):
    print("iteration: " + str(i))
    solver.add(getStep(step, i))
    solver.push()
    solver.add(getStep(solved, i))
    if solver.check() == z3.sat:
        model = solver.model()
        print(model[getStep(sol_post, i)])
        break
    else:
        solver.pop()

print("finish")