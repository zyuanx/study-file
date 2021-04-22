# ( 0) program1 -> program
# ( 1) program -> main block
# ( 2) block -> { stmts }
# ( 3) stmts -> stmt stmts
# ( 4) stmts -> null
# ( 5) stmt -> id = E;
# ( 6) stmt -> while(bool) stmt
# ( 7) stmt -> block
# ( 8) E -> E+F
# ( 9) E -> F
# (10) F -> F*G
# (11) F -> G
# (12) G -> (E)
# (13) G -> T
# (14) bool -> T<=T
# (15) bool -> T>=T
# (16) bool -> T
# (17) T -> id
# (18) T -> num

from Acifa import Cffx

C = [['pro1', '->', 'pro'], ['pro', '->', 'main', 'block'], ['block', '->', '{', 'stmts', '}'], ['stmts', '->', 'stmt', 'stmts'], ['stmts', '->', 'null'], ['stmt', '->', 'id', '=', 'E', ';'], ['stmt', '->', 'while', '(', 'bool', ')', 'stmt'], ['stmt', '->', 'block'], [
    'E', '->', 'E', '+', 'F'], ['E', '->', 'F'], ['F', '->', 'F', '*', 'G'], ['F', '->', 'G'], ['G', '->', '(', 'E', ')'], ['G', '->', 'T'], ['bool', '->', 'T', '<=', 'T'], ['bool', '->', 'T', '>=', 'T'], ['bool', '->', 'T'], ['T', '->', 'id'], ['T', '->', 'num']]
Vn = ['pro1', 'pro', 'block', 'stmts',
      'stmt', 'E', 'bool', 'F', 'G', 'T']
Vt = ['main', '{', '}', 'id', '=',
      '(', ')', '+', '*', '>=', ';', '<=', 'num', 'while', '#']
begin = ['pro1', '->', '·', 'pro']
BEGIN = 'pro'
RES = []


def findI(I, v):
    """
    下一个S状态生成
    """
    newI = []
    global C
    for i in range(len(I)):
        index = location(I[i])
        if index != -1 and I[i][index] == v:
            newI.append(getNextPointI(I[i]))
    addNewI(newI, C)
    return newI


def addNewI(newI, C):
    """
    return;
    闭包生成
    """
    if newI == []:
        return
    oldLen = len(newI)
    for i in range(oldLen):
        index = location(newI[i])
        if index != -1 and isVn(newI[i][index]):
            for j in range(len(C)):
                if C[j][0] == newI[i][index]:
                    _ = addFirstPoint(C[j])
                    if _ not in newI:
                        newI.append(_)
    if oldLen != len(newI):
        addNewI(newI, C)


def location(i):
    """
    找·
    """
    ind = i.index('·')
    if ind != -1 and (ind + 1) != len(i):
        return ind + 1
    return -1


def getNextPointI(i):
    """
    获得下一个
    """
    index = i.index('·')
    temp = i[:index] + i[index+1:][:1]+['·'] + i[index+1:][1:]
    return temp


def isVn(i):
    """
    判断是否为终结符
    """
    global Vn
    if i in Vn:
        return True
    return False


def addFirstPoint(i):
    return i[:2] + ['·'] + i[2:]


def printI(I):
    for i in I:
        print(' '.join(i))
    print("")

# 生成表

def addTd(table, k, a, j, key):
    j = str(j)
    table[k][a] = key + j


def getEndPointI():
    global C
    endI = []
    for i in C:
        if i[2:]==['null']:
            endI.append(i[:2] + ['·','null'])
        else:
            endI.append(i + ['·'])
    return endI


def generateSLRTable(GO, I):
    # print("生成FIRST集：")
    first = getFirst()
    # print(first)
    # print("生成FOLLOW集")
    follow = getFOLLOW(first)
    # print(follow)
    global Vt, Vn, RES
    res = {}
    for k1 in range(len(I)):
        res[k1] = {}
        for k2 in Vt + Vn:
            res[k1][k2] = ' '

    for g in GO:
        for vt in Vt:
            if vt in g:
                addTd(res, g[0], g[1], g[2], 's')
        for vn in Vn:
            if vn in g:
                addTd(res, g[0], g[1], g[2], '')
    endI = getEndPointI()
    # print('endI',endI)
    for i in range(1, len(endI)):
        for In in I:
            if endI[i] in In:
                for vt in follow[endI[i][:1][0]]:
                    if res[I.index(In)][vt] != '':
                        addTd(res, I.index(In), vt, i, 'r')
    for In in I:
        if endI[0] in In:
            addTd(res, I.index(In), '#', 'acc', '')

    print("\nSLR表：")
    print('%5s' % "", end=' ')
    for k in Vt + Vn:
        if k == Vn[-1]:
            print('%5s' % k)
        else:
            print('%5s' % k, end=' ')
    for k1 in res:
        print('%5s' % str(k1), end=' ')
        for k2 in res[k1]:
            print('%5s' % res[k1][k2], end=' ')
        print("")
    RES = res


def getFirst():
    global C, Vt, Vn
    first = {}
    for i in C:
        first[i[:1][0]] = []
    while True:
        flag = False
        for i in C:
            key = i[:1][0]
            r1 = i[2:][0]
            if r1 in Vt or r1 == 'null':
                if addInSet(first[key], r1) == True:
                    flag = True
            if r1 in Vn:
                empty = 0
                for t in i[2:]:
                    if t in Vn:
                        if addInSet(first[key], [_ for _ in first[t] if _ != 'null']) == True:
                            flag = True
                        if checkEmpty(t) == False:
                            break
                        else:
                            empty += 1
                    else:
                        break
                if empty == len(i[2:]):
                    if addInSet(first[key], 'null') == True:
                        flag = True
        if flag == False:
            break
    return first


def getFOLLOW(first):
    follow = {}
    global C, BEGIN
    for v in Vn:
        if v == BEGIN:
            follow[v] = set('#')
        else:
            follow[v] = set()
    while True:
        _flag = False
        for i in C:
            left = i[:1][0]
            right = i[2:]
            for index in range(len(right)):
                if right[index] in Vt or 'null' in right[index]:
                    continue
                if index == (len(right) - 1):
                    for _ in follow[left]:
                        lg = len(follow[right[index]])
                        follow[right[index]].add(_)
                        if lg < len(follow[right[index]]):
                            _flag = True
                else:
                    if right[index+1] in Vt:
                        follow[right[index]].add(right[index+1])
                        lg = len(follow[right[index]])
                        if lg < len(follow[right[index]]):
                            _flag = True
                    else:
                        for _ in first[right[index+1]]:
                            if _ != 'null':
                                follow[right[index]].add(_)
                                lg = len(follow[right[index]])
                                if lg < len(follow[right[index]]):
                                    _flag = True
                    flag = False
                    for _ in right[index + 1:]:
                        if (_ in Vt) or ('null' not in first[_]):
                            flag = True
                    if flag == False:
                        for _ in follow[left]:
                            follow[right[index]].add(_)
                            lg = len(follow[right[index]])
                            if lg < len(follow[right[index]]):
                                _flag = True

        if _flag == False:
            break
    return follow


def addInSet(arr, o):
    flag = False
    if type(o) == str:
        if o not in arr:
            flag = True
            arr.append(o)
    else:
        for m in o:
            if m not in arr:
                flag = True
                arr.append(m)
    return flag


def checkEmpty(v):
    global C
    for i in C:
        if i[:1] == v and i[2:] == ['null']:
            return True
    return False


def main():
    global begin, C
    I = []
    GO = []
    I0 = [begin]
    addNewI(I0, C)
    I.append(I0)
    print("添加S0:")
    printI(I[0])
    for In in I:
        for v in (Vn + Vt):
            newI = findI(In, v)
            if newI != []:
                thisI = I.index(In)
                if newI in I:
                    GO.append([thisI, v, I.index(newI)])
                else:
                    GO.append([thisI, v, len(I)])
                    print("添加S" + str(len(I)) + ":")
                    I.append(newI)
                    printI(newI)
    print("GO关系:")
    # print(GO)
    for g in GO:
        print("GO(S" + str(g[0]) + ", " + g[1] + ") = S" + str(g[2]))
    generateSLRTable(GO, I)


def print_str(t):
    print('%2s | %-40s | %-40s | %50s | %30s' % t)


if __name__ == '__main__':
    input_string = """
    main
    {
        i =2;
        while (i<=100)
        {
            sum = sum + i; 
            i = i+2;
        }
    }
    """
    cffx = Cffx(input_string)
    cffx.GetToken()
    input_list = []
    syn_list = []
    while cffx.syn != -2:
        if cffx.syn == -1:
            a = 1
        else:
            input_list.append(cffx.token)
            if cffx.syn == 2:
                syn_list.append('id')
            elif cffx.syn == 7 or cffx.syn == 3:
                syn_list.append(cffx.token)
            elif cffx.syn == 5:
                syn_list.append('num')
            # print('({},{})'.format(cffx.syn, cffx.token))
        cffx.GetToken()
    # for i in range(len(input_list)):
    #     print(input_list[i], end=' ')
    # print('\n')
    for i in range(len(syn_list)):
        print(syn_list[i], end=' ')
    print('\n')
    main()
    header = Vn + Vt
    i = 1
    stack_status = [0, ]
    stack_symbol = ['#', ]
    syn_list_new = syn_list + ['#']

    print(syn_list_new)
    print_str((' ', '栈中状态', '栈中符号', '输入符号串', '分析步骤'))
    r = RES[stack_status[-1:][0]][syn_list_new[:1][0]]
    while r != 'acc':
        stack_status_new = [str(x) for x in stack_status]
        if r[0] == 's':
            print_str((i, ' '.join(stack_status_new), ''.join(stack_symbol), ''.join(syn_list_new),
                       r+' 移进'+syn_list_new[:1][0]+'，状态转至'+r[1:]))
            # print(r+' 移进'+syn_list_new[:1][0]+'，状态转至'+r[1:])
            stack_status.append(int(r[1:]))
            stack_symbol.append(syn_list_new[:1][0])
            syn_list_new = syn_list_new[1:]

        elif r[0] == 'r':
            # print('r',r)
            c_gy = C[int(r[1:])]
            print_str((i, ' '.join(stack_status_new), ''.join(stack_symbol), ''.join(syn_list_new),
                       r+' 用第'+r[1:]+'产生式'+''.join(c_gy)+'规约'))
            # print(r+' 用第'+r[1:]+'产生式'+''.join(c_gy)+'规约')
            r_len = len(c_gy[2:])
            for j in range(r_len):
                stack_status.pop()
                stack_symbol.pop()
            stack_symbol.append(c_gy[:1][0])
            r = RES[stack_status[-1:][0]][stack_symbol[-1:][0]]
            stack_status.append(int(r))
        else:
            print_str((i, ' '.join(stack_status_new), ''.join(
                stack_symbol), ''.join(syn_list_new), 'Error'))
            break
        i += 1
        r = RES[stack_status[-1:][0]][syn_list_new[:1][0]]
    stack_status_new = [str(x) for x in stack_status]
    print_str((i, ' '.join(stack_status_new), ''.join(stack_symbol), ''.join(syn_list_new),
                       r+' success'))
    # print(r+' success')