class Cffx:
    """
    词法分析类
    """

    def __init__(self, string):
        self.syn = 0
        self.p = 0
        self.prog = string
        self.ch = ''
        self.token = ''
        self.Error_text = ''
        self.res_word = ['if', 'else', 'while', 'do', 'main', 'int', 'float', 'double', 'return', 'const', 'void',
                         'continue',
                         'break', 'char', 'unsigned', 'enum', 'long', 'switch', 'case', 'signed', 'auto', 'static',
                         'include']
        self.spec_symbol = ['#', '+', '-', '*', '/', '=', '<', '>', '{', '}', ';', '(', ')', "'", '"', '==', '!=', '&&',
                            '||', '>=',
                            '<=', '[', ']', '.', ',']

    # 读取字符，二元式输出
    def GetToken(self):
        # if self.p >= len(self.prog) - 1:
        #     self.syn = -2
        #     return
        self.token = ''
        self.ch, self.p = self.prog[self.p], self.p + 1
        while self.ch == ' ' or self.ch == '\n' or self.ch == '\t':
            # 删除空格、回车、制表符
            if self.p >= len(self.prog) - 1:
                # 文件读取完毕，结束
                self.syn = -2
                break
            self.ch, self.p = self.prog[self.p], self.p + 1
        if 'A' <= self.ch <= 'Z' or 'a' <= self.ch <= 'z' or self.ch == '_':
            # 标识符
            self.syn = 1
            self.token = self.token + self.ch
            self.ch, self.p = self.prog[self.p], self.p + 1
            while 'A' <= self.ch <= 'Z' or 'a' <= self.ch <= 'z' or '0' <= self.ch <= '9' or self.ch == '_':
                self.token = self.token + self.ch
                self.ch, self.p = self.prog[self.p], self.p + 1
            self.syn = 2
            if self.token in self.res_word:
                # 保留字
                self.syn = 3
            self.p = self.p - 1
        elif self.ch == '"':
            self.ch, self.p = self.prog[self.p], self.p + 1
            while self.ch != '"':
                self.token = self.token + self.ch
                self.ch, self.p = self.prog[self.p], self.p + 1
            self.syn = 9
            # self.p = self.p - 1
        elif self.ch == "'":
            self.ch, self.p = self.prog[self.p], self.p + 1
            self.token = self.token + self.ch
            self.syn = 10
            if self.prog[self.p] != "'":
                self.syn = -1
            self.p = self.p + 1
        elif self.ch == '/' and self.prog[self.p] == '*':
            # /*注释
            self.ch, self.p = self.prog[self.p], self.p + 1
            while self.ch != '*' or self.prog[self.p] != '/':
                self.ch, self.p = self.prog[self.p], self.p + 1
            self.syn = 0
            self.p += 1
            return
        elif self.ch == '/' and self.prog[self.p] == '/':
            # 注释
            self.ch, self.p = self.prog[self.p], self.p + 1
            while self.ch != '\n':
                self.ch, self.p = self.prog[self.p], self.p + 1
            self.syn = 0
            self.p += 1
            return
        elif self.ch == '0' and self.prog[self.p] == 'x':
            # 十六进制
            self.token = self.token + '0x'
            self.ch, self.p = self.prog[self.p + 1], self.p + 2
            while '0' <= self.ch <= '9' or 'a' <= self.ch <= 'f' or 'A' <= self.ch <= 'F':
                self.token = self.token + self.ch
                self.ch, self.p = self.prog[self.p], self.p + 1
            self.syn = 5
            self.p = self.p - 1
            return
        elif '0' <= self.ch <= '9':
            # 数字
            self.syn = 4
            self.token = self.token + self.ch
            self.ch, self.p = self.prog[self.p], self.p + 1
            while '0' <= self.ch <= '9' or self.ch == '.' or self.ch == '+' or self.ch == '-' or self.ch == 'E' or self.ch == 'e':
                self.token = self.token + self.ch
                self.ch, self.p = self.prog[self.p], self.p + 1
            while self.ch == 'L' or self.ch == 'l':
                self.token = self.token + self.ch
                self.ch, self.p = self.prog[self.p], self.p + 1
            self.syn = 5
            self.p = self.p - 1
            return
        else:
            # 特殊字符
            if self.ch == '=' and self.prog[self.p] == '=':
                self.token = self.token + self.ch + self.prog[self.p]
                self.syn = 7
                self.p = self.p + 1
            elif self.ch == '<' and self.prog[self.p] == '=':
                self.token = self.token + self.ch + self.prog[self.p]
                self.syn = 7
                self.p = self.p + 1
            elif self.ch == '>' and self.prog[self.p] == '=':
                self.token = self.token + self.ch + self.prog[self.p]
                self.syn = 7
                self.p = self.p + 1
            elif self.ch == '!' and self.prog[self.p] == '=':
                self.token = self.token + self.ch + self.prog[self.p]
                self.syn = 7
                self.p = self.p + 1
            elif self.ch == '&' and self.prog[self.p] == '&':
                self.token = self.token + self.ch + self.prog[self.p]
                self.syn = 7
                self.p = self.p + 1
            elif self.ch == '|' and self.prog[self.p] == '|':
                self.token = self.token + self.ch + self.prog[self.p]
                self.syn = 7
                self.p = self.p + 1
            elif self.ch in self.spec_symbol:
                self.syn = 7
                self.token = self.ch
                return

        # if self.p >= len(self.prog) - 1:
        #     self.syn = -2
        #     return


if __name__ == '__main__':
    file_string = """
    #include <studio.h>
    int main(int argc, char const *argv[])
    {
        char *str = "String123",c = 'a';
        /*
        printf("NULL\n");
        */
    
        int floatnum = 123.456;
        // 不做词法处理
        if(6.4ab <= 3.2E-1){
            int x = 0x454aEf;
            float y = 0347l;
            print("Yes ");}
        return 0;
    }
"""
    cffx = Cffx(file_string)
    cffx.GetToken()
    while cffx.syn != -2:
        if cffx.syn == -1:
            print('Error', cffx.Error_text)
        elif cffx.syn == 0:
            a = 1
        else:
            print('({},{})'.format(cffx.syn, cffx.token))
        cffx.GetToken()
