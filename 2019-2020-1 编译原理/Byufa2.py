from Acifa import Cffx


class Yffx():
    def __init__(self, final_table):
        self.final_table = final_table
        self.temp_in = ['#']
        self.final_num = 0
        self.flag_error = 0
        self.index = 1

    def print_temp(self):
        print('第%2d行' % self.index, end='  ')
        self.index += 1
        print('%-50s\t\t\t' % ' '.join(self.temp_in), '', end='')
        print('%80s' % ' '.join(self.final_table[self.final_num:]), end=' #')
        print('')
        if self.temp_in == ['#'] and self.final_table[self.final_num:]:
            print('Error', self.final_table[self.final_num])

    def match(self, char):
        if char != self.final_table[self.final_num]:
            self.flag_error = 1
            return
        # self.print_temp()
        # if len(self.temp_in):
        #     self.temp_in.pop()

        self.final_num += 1

    def program(self):
        # print('program -> block')
        self.temp_in.append('block')
        self.print_temp()
        self.block()
        if self.flag_error:
            print('Error', self.final_table[self.final_num])
            return

    def block(self):
        if self.flag_error:
            return
        self.temp_in.pop()
        # print('block -> { stmts }')
        self.temp_in.append('}')
        self.temp_in.append('stmts')
        self.temp_in.append('{')
        self.print_temp()
        self.match('{')
        self.temp_in.pop()
        self.print_temp()
        self.stmts()
        self.match('}')
        self.temp_in.pop()
        self.print_temp()

    def stmts(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '}':
            # 第二个字符是}
            self.temp_in.pop()
            self.print_temp()
            # print('stmts -> null')
            # self.temp_in.append('null')
            return
        self.temp_in.pop()
        # print('stmts -> stmt stmts')
        self.temp_in.append('stmts')
        self.temp_in.append('stmt')
        self.print_temp()
        self.stmt()
        self.stmts()

    def stmt(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == 'id':
            self.temp_in.pop()
            # print('stmt -> id = expr;')
            self.temp_in.append(';')
            self.temp_in.append('expr')
            self.temp_in.append('=')
            self.temp_in.append('id')
            self.print_temp()
            self.match('id')
            self.temp_in.pop()
            self.print_temp()
            self.match('=')
            self.temp_in.pop()
            self.print_temp()
            self.expr()
            self.match(';')
            self.temp_in.pop()
            self.print_temp()
        elif self.final_table[self.final_num] == 'if':
            self.match('if')
            self.temp_in.pop()
            self.print_temp()
            self.match('(')
            self.temp_in.pop()
            self.print_temp()
            self.bool()
            self.match(')')
            self.temp_in.pop()
            self.print_temp()
            self.stmt()
            if self.final_table[self.final_num] == 'else':
                # print('stmt -> if(bool) stmt else stmt')
                self.temp_in.append('stmt')
                self.temp_in.append('else')
                self.temp_in.append('stmt')
                self.temp_in.append(')')
                self.temp_in.append('bool')
                self.temp_in.append('(')
                self.temp_in.append('if')
                self.print_temp()
                self.match('else')
                self.temp_in.pop()
                self.print_temp()
                self.stmt()
            else:
                # print('stmt -> {if(bool) stmt')
                self.temp_in.append('stmt')
                self.temp_in.append(')')
                self.temp_in.append('bool')
                self.temp_in.append('(')
                self.temp_in.append('if')
                self.print_temp()
        elif self.final_table[self.final_num] == 'while':
            self.temp_in.pop()
            # print('stmt -> while( bool ) stmt')
            self.temp_in.append('stmt')
            self.temp_in.append(')')
            self.temp_in.append('bool')
            self.temp_in.append('(')
            self.temp_in.append('while')
            self.print_temp()
            self.match('while')
            self.temp_in.pop()
            self.print_temp()
            self.match('(')
            self.temp_in.pop()
            self.print_temp()
            self.bool()
            self.match(')')
            self.temp_in.pop()
            self.print_temp()
            self.stmt()
        elif self.final_table[self.final_num] == 'do':
            self.temp_in.pop()
            # print('stmt -> do stmt while(bool)')
            self.temp_in.append(')')
            self.temp_in.append('bool')
            self.temp_in.append('(')
            self.temp_in.append('while')
            self.temp_in.append('stmt')
            self.temp_in.append('do')
            self.print_temp()
            self.match('do')
            self.temp_in.pop()
            self.print_temp()
            self.stmt()
            self.match('while')
            self.temp_in.pop()
            self.print_temp()
            self.match('(')
            self.temp_in.pop()
            self.print_temp()
            self.bool()
            self.match(')')
            self.temp_in.pop()
            self.print_temp()
        elif self.final_table[self.final_num] == 'break':
            self.temp_in.pop()
            # print('stmt -> break')
            self.temp_in.append('break')
            self.print_temp()
            self.match('break')
            self.temp_in.pop()
            self.print_temp()
        else:
            self.temp_in.pop()
            # print('stmt -> block')
            self.temp_in.append('block')
            self.print_temp()
            self.block()

    def bool(self):
        if self.flag_error:
            return
        self.temp_in.pop()
        # print('bool -> expr bool1')
        self.temp_in.append('bool1')
        self.temp_in.append('expr')
        self.expr()
        self.bool1()

    def bool1(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '<=':
            self.temp_in.pop()
            # print('bool -> expr <= expr')
            self.temp_in.append('expr')
            self.temp_in.append('<=')
            self.print_temp()
            self.match('<=')
            self.temp_in.pop()
            self.print_temp()
            self.expr()
        elif self.final_table[self.final_num] == '<':
            self.temp_in.pop()
            # print('bool -> expr < expr')
            self.temp_in.append('expr')
            self.temp_in.append('<')
            self.print_temp()
            self.match('<')
            self.temp_in.pop()
            self.print_temp()
            self.expr()
        elif self.final_table[self.final_num] == '>=':
            self.temp_in.pop()
            # print('bool -> expr >= expr')
            self.temp_in.append('expr')
            self.temp_in.append('>=')
            self.print_temp()
            self.match('>=')
            self.temp_in.pop()
            self.print_temp()
            self.expr()
        elif self.final_table[self.final_num] == '>':
            self.temp_in.pop()
            # print('bool -> expr > expr')
            self.temp_in.append('expr')
            self.temp_in.append('>')
            self.print_temp()
            self.match('>')
            self.temp_in.pop()
            self.print_temp()
            self.expr()
        else:
            self.temp_in.pop()
            # print('bool -> expr')
            self.print_temp()

    def expr(self):
        if self.flag_error:
            return
        self.temp_in.pop()
        # print('expr -> term expr1')
        self.temp_in.append('expr1')
        self.temp_in.append('term')
        self.print_temp()
        self.term()
        self.expr1()

    def expr1(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '+':
            self.temp_in.pop()
            # print('expr1 -> + term expr1')
            self.temp_in.append('expr1')
            self.temp_in.append('term')
            self.temp_in.append('+')
            self.print_temp()
            self.match('+')
            self.temp_in.pop()
            self.print_temp()
            self.term()
            self.expr1()
        elif self.final_table[self.final_num] == '-':
            self.temp_in.pop()
            # print('expr1 -> - term expr1')
            self.temp_in.append('expr1')
            self.temp_in.append('term')
            self.temp_in.append('-')
            self.print_temp()
            self.match('-')
            self.temp_in.pop()
            self.print_temp()
            self.term()
            self.expr1()
        else:
            self.temp_in.pop()
            self.print_temp()
            # print('expr1 -> null')
            # self.temp_in.append('null')
            return

    def term(self):
        if self.flag_error:
            return
        self.temp_in.pop()
        # print('term -> factor term1')
        self.temp_in.append('term1')
        self.temp_in.append('factor')
        self.print_temp()
        self.factor()
        self.term1()

    def term1(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '*':
            self.temp_in.pop()
            # print('term1 -> * factor term1')
            self.temp_in.append('*')
            self.temp_in.append('term1')
            self.temp_in.append('factor')
            self.factor()
            self.term1()
        elif self.final_table[self.final_num] == '/':
            self.temp_in.pop()
            # print('term1 -> / factor term1')
            self.temp_in.append('/')
            self.temp_in.append('term1')
            self.temp_in.append('factor')
            self.factor()
            self.term1()
        else:
            self.temp_in.pop()
            self.print_temp()
            # print('term1 -> null')
            # self.temp_in.append('null')
            return

    def factor(self):
        if self.flag_error:
            return
        if self.final_table[self.final_num] == '(':
            self.temp_in.pop()
            # print('factor -> ( expr )')
            self.temp_in.append(')')
            self.temp_in.append('expr')
            self.temp_in.append('(')
            self.print_temp()
            self.match('(')
            self.temp_in.pop()
            self.print_temp()
            self.expr()
            self.match(')')
            self.temp_in.pop()
            self.print_temp()
        elif self.final_table[self.final_num] == 'id':
            self.temp_in.pop()
            # print('factor -> id')
            self.temp_in.append('id')
            self.print_temp()
            self.match('id')
            self.temp_in.pop()
            self.print_temp()
        elif self.final_table[self.final_num] == 'num':
            self.temp_in.pop()
            # print('factor -> num')
            self.temp_in.append('num')
            self.print_temp()
            self.match('num')
            self.temp_in.pop()
            self.print_temp()


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
    # for i in range(len(input_list)):
    #     print(input_list[i], end=' ')
    # print('\n')
    # for i in range(len(syn_list)):
    #     print(syn_list[i], end=' ')
    # print('\n')
    yffx = Yffx(syn_list)
    yffx.program()
