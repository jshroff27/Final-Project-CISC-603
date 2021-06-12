# This is the code for simple compiler just using lexers and parsers
# Rply is the package that has been used
from rply import LexerGenerator

lg = LexerGenerator()
# lexergenerator add is the function that is used to add different tokens
lg.add('NUMBER', r'\d+')  # Generate lexer for number
lg.add('PLUS', r'\+')  # Generate lexer for addition
lg.add('MINUS', r'-')  # Generate lexer for subtraction
lg.add('MULTIPLICATION', r'\*')  # Generate lexer for multiplication
lg.add('DIVISION', r'/')  # Generate lexer for division
lg.add('OPENPARENTHESIS', r'\(')  # Generate lexer for open parenthesis
lg.add('CLOSEPARENTHESIS', r'\)')  # Generate lexer for close parenthesis
lg.ignore('\s+')  # lexer to ignore blanks spaces



# Creating a function to build the lexers so that it can be used as a package in the main compiled script for the toy compiler
def Lexer():
    return lg.build()  # This will just build the lexers and return it


# Basebox is the rply function to categorize tokens into the boxes
from rply.token import BaseBox


class Number(BaseBox):
    def __init__(self, value):
        self.value = value  # initializing the tokens into values

    def eval(self):
        return self.value


# This is going to create all the binary operation nodes which will take in the nodes left and right
class operator(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right


# creating an object that is taking in the left node, the addition operator and the right node
# each of the classes below will have eval methods which basically help see the results of our classes
class Plus(operator):
    def eval(self):
        return self.left.eval() + self.right.eval()


# creating an object that is taking in the left node, the subtraction operator and the right node
class Minus(operator):
    def eval(self):
        return self.left.eval() - self.right.eval()


# creating an object that is taking in the left node, the multiplication operator and the right node
class Multiplication(operator):
    def eval(self):
        return self.left.eval() * self.right.eval()


# creating an object that is taking in the left node, the division operator and the right node
class Division(operator):
    def eval(self):
        return self.left.eval() / self.right.eval()


# buiding parsers that will take the input of the tokens and parse them
from rply import ParserGenerator

pg = ParserGenerator(
    ['NUMBER', 'OPENPARENTHESIS', 'CLOSEPARENTHESIS',
     'PLUS', 'MINUS', 'MULTIPLICATION', 'DIVISION'
     ], precedence=[('left', ['PLUS', 'MINUS']), ('left', ['MULTIPLICATION', 'DIVISION'])])


# the precedence is set from left to right in how the tokens are read and to remove any disambiguity

# This first production rule is telling the parser that an expression is a number
# The method below is returning the number which is the string and converting it into an integer
@pg.production('expression : NUMBER')
def expression_number(p):
    return Number(int(p[0].getstr()))


# the production decorators are used along with the parsers to take in the nodes in the form of the expression then the different operators and then the following operations
@pg.production('expression : OPENPARENTHESIS expression CLOSEPARENTHESIS')
def expression_parens(p):
    return p[1]


# this will not work if the input is 1 1 instead of 1+1
# creating productions here which are decorators which is taking a string that is corresponding to name of the production
# These productions are saying that an expression will be having an expression then an operator and then another expression and to return the integers of first and third values which does not include the operator
@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MULTIPLICATION expression')
@pg.production('expression : expression DIVISION expression')
# the following function is basically getting the tokens and taking the first and third value and then based on the operator it is performing the arithmetic calculation.
def expression_binop(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return Plus(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Minus(left, right)
    elif p[1].gettokentype() == 'MULTIPLICATION':
        return Multiplication(left, right)
    elif p[1].gettokentype() == 'DIVISION':
        return Division(left, right)
    else:
        raise AssertionError('Error')


# building the function for the parser that I will be using in my program as an import
def Parser():
    return pg.build()

