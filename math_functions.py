import ply.lex as lex
import matplotlib.pyplot as plt
import re
import numpy as np
import math as math


class Parser(object):
    x = []
    y = []
    interval_x_to = 0
    interval_x_from = 0
    val = 0

    # Lista tokenov
    tokens = (
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'OGLATD',
        'OGLATL',
        'VEJICA',
        'SYMBOL',
        'POWER',
        'SINUS',
        'COSINUS',
        'TANGES',
        'SQRT',
        'LOG'
    )

    # regularni izrazi za tokene
    t_MINUS = r'\-'
    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_OGLATL = r'\['
    t_OGLATD = r'\]'
    t_VEJICA = r'\,'
    t_POWER = r'\^'
    t_SINUS = r'sin'
    t_COSINUS = r'cos'
    t_TANGES = r'tan'
    t_SQRT = r'sqrt'
    t_LOG = r'log'
    t_SYMBOL = r'(x){1}'

    def t_NUMBER(self, t):
        r'\d+(\.\d{1,2})?'
        t.value = float(t.value)
        return t

    # Kaj ignoriramo
    t_ignore = ' \t'

    # Napaka pr tokenih
    def t_error(self, t):
        print("Nepravilni token '%s'" % t.value[0])
        t.lexer.skip(1)

    # Zbuildam lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Izpis tokenov
    def getTokens(self, data):
        self.lexer.input(data)  # vstavim string
        while True:
            tok = self.lexer.token()  # da naslednji token ali none
            if not tok:  # ce je non prenehamo
                break
            print(tok)

    def parsing(self, data):
        self.lexer.input(data)  # vstavim string
        self.konec = 1
        self.t = self.lexer.token()
        self.parse_interval()  # dobim interval
        self.x = np.arange(self.interval_x_from, self.interval_x_to+0.01, 0.01)  # naredim interval X
        self.po_vrsti = 0
        data=data.split("]",1)[1]
        for index in range(len(self.x)):
            self.lexer.input(data)
            self.t = self.lexer.token()
            self.result=self.parse_expr()  # nato funkcijo izvajam glede na interval
            print(self.result)
            self.y.append(self.result) #  vstavim rešitev v Y
            self.po_vrsti += 1

    def draw(self):
        plt.plot(self.x, self.y)
        plt.gca().spines['bottom'].set_position('center')
        plt.gca().spines['left'].set_position('center')
        plt.show()

    def get_token(self):
        self.t = self.lexer.token()
        if not self.t:  # ce je none prenehamo
            self.konec = 0
            return False
        else:
            self.konec = 1
            return True

    def parse_expr(self):
        term = self.parse_term()
        while 1:
            if self.konec == 0:
                return term
            if self.t.value == '^':
                self.get_token()
                return math.pow(term, self.parse_number())
            if self.t.value == '+':
                if not (self.get_token()):
                    return term
                term += self.parse_term()
            elif self.t.value == '-':
                if not (self.get_token()):
                    return term
                term -= self.parse_term()
            else:
                return term

    def parse_term(self):
        factor = self.parse_factor()
        while 1:
            if self.konec == 0:
                return factor
            elif self.t.value == '*':
                if not (self.get_token()):
                    return factor
                factor *= self.parse_factor()
            elif self.t.value == '/':
                if not (self.get_token()):
                    return factor
                factor /= self.parse_factor()
            else:
                return factor

    def parse_factor(self):
        negate = 1
        if self.t.value == '-':
            self.get_token()
            negate = -1
        elif self.t.value == '+':
            self.get_token()
            negate = 1
        pattern = re.compile("\d+(\.\d{1,2})?")
        if pattern.match(str(self.t.value)):
            return negate*self.parse_number()
        pattern = re.compile("(x){1}")
        if pattern.match(str(self.t.value)):
            return negate*self.parse_symbol()
        if self.t.value == '(':
            self.get_token()
            expr = self.parse_expr()
            if self.t.value == ')':
                self.get_token()
                return negate*expr
        return self.math_functions()

    def math_functions(self):
        if self.t.value == 'sin':
            self.get_token()
            if self.t.value == '(':
                self.get_token()
                expr = self.parse_expr()
                if self.t.value == ')':
                    self.get_token()
                    return math.sin(expr)
        if self.t.value == 'cos':
            self.get_token()
            if self.t.value == '(':
                self.get_token()
                expr = self.parse_expr()
                if self.t.value == ')':
                    self.get_token()
                    return math.cos(expr)
        if self.t.value == 'tan':
            self.get_token()
            if self.t.value == '(':
                self.get_token()
                expr = self.parse_expr()
                if self.t.value == ')':
                    self.get_token()
                    return math.tan(expr)
        if self.t.value == 'sqrt':
            self.get_token()
            if self.t.value == '(':
                self.get_token()
                expr = self.parse_expr()
                if self.t.value == ')':
                    self.get_token()
                    return math.sqrt(expr)
        if self.t.value == 'log':
            self.get_token()
            if self.t.value == '(':
                self.get_token()
                expr = self.parse_expr()
                if self.t.value == ')':
                    self.get_token()
                    return math.log(expr)

    def parse_number(self):
        num = float(self.t.value)
        self.get_token()
        if self.konec == 0:
            return num
        if self.t.value == '^':
            self.get_token()
            return math.pow(num, self.parse_factor())
        return num

    def parse_symbol(self):
        num = self.x[self.po_vrsti]
        self.get_token()
        return num

    def parse_interval(self):
        if self.konec == 1:
            if self.t.value == '[':
                self.get_token()
                expr = self.parse_expr()
                self.interval_x_from = int(expr)
                if self.t.value == ',':
                    self.get_token()
                    expr = self.parse_expr()
                    self.interval_x_to = int(expr)
                    if self.t.value == ']':
                        self.get_token()


# TEST
m = Parser()
m.build()  # Build lexer

#m.parsing("[-10,10] sqrt(2^3)*x + sin(2^3)+1*x / cos(2^3)*3^2")
#m.parsing("[-3.3,3.3] sin(x)/cos(x)")
#m.parsing("[-10,10] sin(cos(tan(x)))")
#m.parsing("[-10,10] 1+2*x*(3+x)+1*2^4")
m.parsing("[1,10] tan(x+3*(2^3))*sin(log(x))")  # tan(x)*sin(log(x)) interval [1, 10]
#m.parsing("[-10,10] 1/x^3")
#m.parsing("[1,10]3+5*-2")
#m.parsing("[-100,100] x^3")
#m.parsing("[-3.2,0] (-1 / (x+2))+5 ")
#m.getTokens("[-10,10] sqrt(2^3) + sin(2^3)+1 / cos(2+3)*3^2")  # dobi vse tokene

m.draw()


