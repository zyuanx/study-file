# 100: i = 2
# 101: if i <= 100 goto
# 102: goto
# 103: t1 = sum + i
# 104: sum = t1
# 105: t2 = i+2
# 106: i = t2
# 107: goto
# 108:
table = ['i', '=', '2', ';', 'while',
         '(', 'i', '<=', '100', ')', '{', 'sum', '=', 'sum', '+', 'i', ';', 'i', '=', 'i', '+', '2', ';', '}', '#']
# 1为{与}，2为标识符，3为运算符，4为数字串，5为控制关键字，6为符号
dic = {'{': 1, '}': 1, 'i': 2, '=': 3, ';': 6,
       'while': 5, '(': 3, ')': 3, '<=': 6, '5': 4, 'sum': 2, '+': 3}

siyuan = []  # 四元式


class yuyi:
    def __init__(self):
        print('\n语义分析结果(四元式):')
        self.i = 0  # 栈指针
        self.t = 1  # 记录临时变量T数目
        self.flag = False
        self.beg()
        for i in siyuan:  # 输出四元式结果
            print(i)

    def beg(self):
        if dic[table[self.i]] == 2:
            left = table[self.i]
            self.i += 1
            op = table[self.i]
            self.i += 1
            if table[self.i+1] == ';':
                right = table[self.i]
                self.i += 1
                siyuan.append('({},{},{},{})'.format(op, right, '_', left))
                self.i += 1
            else:
                right1 = table[self.i]
                self.i += 1
                op1 = table[self.i]
                self.i += 1
                right2 = table[self.i]
                self.i += 1
                temp = 'T'+str(self.t)
                self.t += 1
                siyuan.append('({},{},{},{})'.format(
                    op1, right1, right2, temp))
                siyuan.append('({},{},{},{})'.format(
                    op, temp, '_', left))
                self.i += 1
            self.beg()
        elif dic[table[self.i]] == 5:
            self.i += 2

            s = []
            while table[self.i] != ')':
                s.append(table[self.i])
                self.i += 1

            siyuan.append('({},{},{},{})'.format(
                'j'+s[1], s[0], s[2], '#'))
            self.i += 1
            if table[self.i] == '{':
                self.i += 1
                self.flag = True
            self.beg()


if __name__ == '__main__':
    print(dic)
    print(table)
    yuyi()
    i = 100
    print('开始生成中间代码')
    mid = []
    for item in siyuan:
        temp = item[1:-1].split(',')
        if temp[0][:1] == 'j':
            mid.append('if {}{}{} goto {}'.format(
                temp[1], temp[0][1:], temp[2], len(mid)+101))
            mid.append('goto {}'.format('107'))
        elif temp[0][:1] == '=':
            mid.append('{}{}{}'.format(temp[3], '=', temp[1]))
        elif temp[0][:1] == '+':
            mid.append('{}{}{}'.format(temp[3], '+', temp[1]))
    mid.append('other')
    for i in range(len(mid)):
        print(100+i, mid[i])
