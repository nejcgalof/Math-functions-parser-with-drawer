# Math-functions-parser-with-drawer
Lexer and parser for math functions and simulating drawing graphs

Using Parser class:
```
parser = Parser()
parser.build()  # Build lexer
parser.parsing("[x,y] function") # Parsing / evaluate
parser.getTokens("[x,y] function") # Get tokens
parser.draw() # Draw graph
```
