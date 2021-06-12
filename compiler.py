from myprogram import Parser
from myprogram import Lexer
#From my program that was created before I had generated a function to return a parser and a function to return my lexer. Those two functions are imported in this
lexer = Lexer()
parsers = Parser()
input1 = int(input('Try writing a formula:\n 1) Yes: \n 2) No: \n'))
while input1 == 1:
    input2 = int(input('Add input:\n 1) Yes: \n 2) No: \n'))
    if input2 == 1:
        text1 = input('Formula: ')
        print(parsers.parse(lexer.lex(text1)).eval())
    else:
        break