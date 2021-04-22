from Acifa import Cffx


class Yffx():
    def __init__(self, final_table):
        self.final_table = final_table

        self.final_num = 0
        self.flag_error = 0

    def match(self, char):
        if char != self.final_table[self.final_num]:
            self.flag_error = 1
            return
        self.final_num += 1

    def program(self):
        print('program -> block')
        self.block()
        if self.flag_error:
            print('Error')
            return

    def block(self):
        if self.flag_error:
            return
        print('block -> { stmts }')
        self.match('{')
        self.stmts()
        self.match('}')

    def stmts(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '}':
            # 第二个字符是}
            print('stmts -> null')
            return
        print('stmts -> stmt stmts')
        self.stmt()
        self.stmts()

    def stmt(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == 'id':
            print('stmt -> id = expr;')
            self.match('id')
            self.match('=')
            self.expr()
            self.match(';')
        elif self.final_table[self.final_num] == 'if':
            self.match('if')
            self.match('(')
            self.bool()
            self.match(')')
            self.stmt()
            if self.final_table[self.final_num] == 'else':
                print('stmt -> if(bool) stmt else stmt')
                self.match('else')
                self.stmt()
            else:
                print('stmt -> if(bool) stmt')
        elif self.final_table[self.final_num] == 'while':
            print('stmt -> while( bool ) stmt')
            self.match('while')
            self.match('(')
            self.bool()
            self.match(')')
            self.stmt()
        elif self.final_table[self.final_num] == 'do':
            print('stmt -> do stmt while(bool)')
            self.match('do')
            self.stmt()
            self.match('while')
            self.match('(')
            self.bool()
            self.match(')')
        elif self.final_table[self.final_num] == 'break':
            print('stmt -> break')
            self.match('break')
        else:
            print('stmt -> block')
            self.block()

    def bool(self):
        if self.flag_error:
            return
        print('bool -> expr bool1')
        self.expr()
        self.bool1()

    def bool1(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '<=':
            print('bool1 -> <= expr')
            self.match('<=')
            self.expr()
        elif self.final_table[self.final_num] == '<':
            print('bool1 -> < expr')
            self.match('<')
            self.expr()
        elif self.final_table[self.final_num] == '>=':
            print('bool1 -> >= expr')
            self.match('>=')
            self.expr()
        elif self.final_table[self.final_num] == '>':
            print('bool1 -> expr > expr')
            self.match('>')
            self.expr()
        else:
            print('bool1 -> null')

    def expr(self):
        if self.flag_error:
            return
        print('expr -> term expr1')
        self.term()
        self.expr1()

    def expr1(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '+':
            print('expr1 -> + term expr1')
            self.match('+')
            self.term()
            self.expr1()
        elif self.final_table[self.final_num] == '-':
            print('expr1 -> - term expr1')
            self.match('-')
            self.term()
            self.expr1()
        else:
            print('expr1 -> null')
            return

    def term(self):
        if self.flag_error:
            return
        print('term -> factor term1')
        self.factor()
        self.term1()

    def term1(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '*':
            print('term1 -> * factor term1')
            self.factor()
            self.term1()
        elif self.final_table[self.final_num] == '/':
            print('term1 -> / factor term1')
            self.factor()
            self.term1()
        else:
            print('term1 -> null')
            return

    def factor(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '(':
            print('factor -> ( expr )')
            self.match('(')
            self.expr()
            self.match(')')
        elif self.final_table[self.final_num] == 'id':
            print('factor -> id')
            self.match('id')
        elif self.final_table[self.final_num] == 'num':
            print('factor -> num')
            self.match('num')


if __name__ == '__main__':
    input_string = """
    {
        i = 2;
        while(i <= 100)
        {
            sum = sum + i;
            i = i + 2;
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
    for i in range(len(input_list)):
        print(input_list[i], end=' ')
    print('\n')
    for i in range(len(syn_list)):
        print(syn_list[i], end=' ')
    print('\n')
    yffx = Yffx(syn_list)
    yffx.program()
