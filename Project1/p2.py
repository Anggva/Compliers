__author__ = 'vasilina'

global counter;
global tokens;
#0
def main(tokens):
    counter = 0;
    nextToken(tokens);
    prg(nextToken);
    return 1;
#1
def prg(token):
    TypeSpec(token);
    if nextToken(tokens) is ID:
        counter+=1;
    #else
    T(nextToken(tokens));
    DecListPrime(nextToken(tokens));

#2
def DecListPrime(token):
    TypeSpec(token);
    if nextToken(tokens) is ID:
        counter+=1;
    #else
    T(nextToken(tokens));
    DecListPrime(nextToken(tokens));

    #Or check follows
    isFollow(token);
#3
def T(token):
    VarDecl(token);

    #Or if failed

    if token == '(':
        counter+=1;
    Params(nextToken(tokens));
    if nextToken(tokens) == '(':
        counter+=1;
    CompoundStmt(nextToken(tokens));
#4
def VarDecl (token):
    if token == ';':
        counter+=1;
    elif token == '[':
        counter+=1;
        if nextToken(tokens) is NUM:
            counter+=1;
        if nextToken(tokens) == ']':
            counter+=1;
        if nextToken(tokens) == ';':
            counter+=1;
#5
def TypeSpec (token):
    if token == 'int':
        counter+=1;
    elif token == 'void':
        counter+=1;
    elif token == 'float':
        counter+=1;
#6
def Params (token):
    if token == 'int' or token == 'float':
        counter+=1;
        if nextToken(tokens) is ID:
            counter += 1;
        Y(nextToken(tokens));
        ParamList(nextToken(tokens));
    elif token == 'void':
        counter += 1;
        P(nextToken(tokens));
#7
def P (token):
    if token is ID:
        counter += 1;
    Y(nextToken(tokens));
    ParamList(nextToken(tokens));

    #check the follows

#8
def ParamsList (token):
    if token == ',':
        counter += 1;
    TypeSpec(nextToken(tokens));
    if nextToken(tokens) is ID:
        counter += 1;
    Y(nextToken(tokens));
    ParamList(nextToken(tokens));

    #Or check the follows
#9
def Y(token):
    if token == '[':
        counter += 1;
    if nextToken(tokens) == ']':
        counter += 1;

    # or check for follows

#10
def CompoundStmt(token):
    if token == '{':
        counter += 1;
    LocalDecl(nextToken(tokens));
    StmtList(nextToken(tokens));
    if nextToken(tokens) == '}':
        counter += 1;
#11
def LocalDecl(token):
    LocalDeclPrime(token);

#12
def LocalDeclPrime(token):
    TypeSpec(token);
    if nextToken(tokens) is ID:
        counter+=1;
    VarDecl(nextToken(tokens));
    LocalDeclPrime(nextToken(tokens));

    #or check for follow

#13
def StmtList(token):
    StmtListPrime(token);
#14
def StmtListPrime (token):
    Stmt(token);
    StmtListPrime(nextToken(tokens));

    #or check for follows

#15
def Stmt(token):
    ExprStmt(token);
    #or
    CompoundStmt(token);
    #or
    SelectionStmt(token);
    #or
    IterStmt(token);
    #or
    ReturnStmt(token);
#16
def ExprStmt(token):
    if token == ';':
        counter += 1;
    else:
        Expr(token);
        if token == ';':
            counter += 1;
#17
def SelectionStmt(token):
    if token == 'if':
        counter += 1;
    if nextToken(tokens) == '(':
        counter += 1;
    Expr(nextToken(tokens));
    if nextToken(tokens) == ')':
        counter += 1;
    Stmt(nextToken(tokens));
    X(nextToken(tokens));

#18
def X(token):
    if token == 'else':
        counter += 1;
    Stmt(nextToken(tokens));

    #or check the follows