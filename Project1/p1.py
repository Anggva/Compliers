__author__ = 'vasilina'
import sys

spaces = [' ', '\n', '\t', '\r'];
keywords = ['else', 'if','int', 'while', 'return', 'float', 'void'];
arithmetSymb = ['+','-','*','/'];
compareSymb = ['<','>','!', '='];
delimiters = [';',',','(',')','[',']','{','}']
allDelimiters = arithmetSymb + ['<','>',';','(',')','[',']','{','}'];
floatSymb = ['E', '.', '+', '-'];
superset = arithmetSymb+compareSymb+delimiters+['='];
numbers = ['0','1','2','3','4','5','6','7','8','9'];
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];

tokens = [];
counter = 0;
errorMarker = 0;

def main():
    if len(sys.argv) < 2:
        print 'Error, no input file!'
        return 0;
    inputFile = sys.argv[1];
    fileVar = open(inputFile, 'r');
    content = fileVar.readlines();
    voffset = -1;
    word = '';
    specWord = '';
    depth = 0;
    i = 0;
    global tokens;
    while i < len(content):
        current = 'start';
        floatC = '';
        line = content[i];
        j = removeSpaces(line);
        if notEmpty(line):
            print 'INPUT:', line[j:len(line)-1];
        else:
            print line[:len(line)-1];
        offset = j-1;
        while j < len(line):
            char = line[j];
            if char=='/':
                processWord(word, depth);
                word = ''
                res = processComment(line, offset, content, voffset);
                if res == 0: #Not a comment
                    pass
                elif res == 1: #Comment starts with //
                    break
                elif res == [-1,-1]: #Comment started but never ended
                    printLines(voffset, res, content);
                    i = len(content);
                    break;
                else: #Comment starts with /* and ends with */
                    current = 'comment';
                    printLines(voffset, res, content)
                    if res[1] != voffset:
                        voffset = res[1];
                        i = voffset+1;
                        line = content[i];
                    if res[2] >= len(line)-1:
                        break;
                    else:
                        offset = res[2];
                        j = res[2]+1;
                        char = line[j];
            if current == 'number' and char in floatSymb:
                if char == '.' and floatC == '':
                   word += char;
                   floatC = char;
                elif char == 'E' and (floatC == '' or floatC == '.'):
                    if j < len(line) - 2:
                        d = next(line, offset);
                        e = next(line, offset+1);
                        if (d == '+' or d =='-') and e in numbers:
                            word += char;
                            floatC = char;
                        elif d in numbers:
                            word += char;
                            floatC = char;
                        else:
                            processWord(word, depth);
                            word = ''
                            current = 'error';
                            k = processError(line, j);
                            offset = k;
                            j = k+1;
                            continue;
                    else:
                        processWord(word, depth);
                        word = ''
                        current = 'error';
                        k = processError(line, j);
                        offset = k;
                        j = k+1;
                        continue;
                elif (char == '+' or char == '-') and floatC == 'E':
                    word += char;
                    floatC = char;
                elif char == '+' or char == '-':
                    current = 'arithmetic symbol';
                    newToken = [];
                    newToken.append('arithmSymb');
                    newToken.append(char);
                    tokens.append(newToken);
                    offset -=1;
                    j-=1;
                else:
                    processWord(word, depth);
                    word = ''
                    current = 'error';
                    k = processError(line, j);
                    offset = k;
                    j = k+1;
                    continue
                offset += 1;
            elif char in superset:
                processWord(word, depth);
                word = ''
                if char in arithmetSymb:
                    current = 'arithmetic symbol';
                    newToken = [];
                    newToken.append('arithmSymb');
                    newToken.append(char);
                    tokens.append(newToken);
                    print char;
                    offset += 1;
                elif char in compareSymb:
                    d = next(line, offset);
                    if d == '=':
                        current = 'comparison';
                        specWord+=char+d
                        print specWord
                        newToken = [];
                        newToken.append('compare');
                        newToken.append(specWord);
                        tokens.append(newToken);
                        offset+=2
                        j+=2;
                        specWord=''
                        continue;
                    elif char == '!':
                        current = 'error';
                        k = processError(line, j);
                        offset = k;
                        j = k+1;
                        continue;
                    else:
                        current = 'comparison';
                        newToken = [];
                        newToken.append('compare');
                        newToken.append(char);
                        tokens.append(newToken);
                        print char
                        offset +=1;
                elif char in delimiters:
                    current = 'delimiter';
                    if char == '{':
                        depth += 1;
                        offset +=1;
                        print char
                    elif char == '}':
                        depth -= 1;
                        offset +=1;
                        print char;
                    else:
                        offset += 1;
                        print char;
                    newToken = [];
                    newToken.append('delim');
                    newToken.append(char);
                    tokens.append(newToken);
                else:
                    current = 'specSymbol'
                    offset += 1;
                    newToken = [];
                    newToken.append('delim');
                    newToken.append(char);
                    tokens.append(newToken);
                    print char;
            elif char in alphabet:
                if current != 'number':
                    word+=char
                    offset += 1;
                    current = 'word';
                else:
                    processWord(word, depth);
                    word = '';
                    current = 'error'
                    k = processError(line, j);
                    offset = k;
                    j = k+1;
                    continue;
            elif char in numbers:
                if current != 'word':
                    current = 'number'
                    word+=char
                    offset += 1
                else:
                    processWord(word, depth);
                    word = '';
                    current = 'error'
                    k = processError(line, j);
                    offset = k;
                    j = k+1;
                    continue;
            elif char in spaces:
                offset+=1
                if current == 'start' or current == 'comment':
                    j+=1
                    continue
                else:
                    processWord(word, depth)
                    word = '';
                    floatC = '';
                    current = 'space';
            else:
                processWord(word, depth)
                word = '';
                current = 'error';
                k = processError(line, j);
                offset = k;
                j = k+1;
                continue;
            j+=1
        voffset+=1;
        i+=1;
    fileVar.close();
    tokens.append(['End','$']);
    global counter;
    counter = 0;
    global errorMarker;
    if (errorMarker):
        result = 'No'
    else:
        result = prg();
    print result;
    return 1;

def nextToken(counter):
    global tokens;
    return tokens[counter];

def next(line, offset):
    if line[offset+2] != None:
        return line[offset+2]
    else:
        return None


def processWord(word, depth):
    global tokens;
    newToken = [];
    if len(word) > 0:
        if word in keywords:
            s = 'keyword: '+ word;
            newToken.append('keyword');
            newToken.append(word);
        elif aNumber(word, numbers):
            s = 'NUM: ' + word;
            newToken.append('NUM');
            newToken.append(word);
        else:
            s = 'ID: ' + word + ' |depth:' + str(depth);
            newToken.append('ID');
            newToken.append(word);
        tokens.append(newToken);
        print s;


def parseLine(line, offset, content, voffset, c1, c2):
    cDepth = 1;
    i = offset + 3; #Skip /*
    while i < len(line):
        if line[i] == c2 and line[i+1] == c1:
            cDepth += 1;
            i+=2
            continue;
        elif line[i] == c1 and line[i+1] == c2:
            cDepth -= 1;
            if cDepth == 0:
                return [offset, voffset, i+2];
            i+=1;
        i+=1;

    for i in range (voffset+2, len(content)):
        line = content[i];
        j = 0;
        while j < len(line):
            if line[j] == c2 and line[j+1] == c1:
                cDepth += 1;
                j+=2
                continue;
            elif line[j] == c1 and line[j+1] == c2:
                cDepth -= 1;
                if cDepth == 0:
                    return [offset,i-1,j+2];
                j+=1;
            j+=1
        i+=1;
    return [-1,-1];

def processComment(line, offset, content, voffset):
    c = next(line, offset);
    if c != '/' and c != '*':
        return 0;
    elif c == '/':
        return 1;
    elif c == '*':
        return parseLine(line, offset, content, voffset, '*', '/');

def aNumber(line, numbers):
    for char in line:
        if char not in numbers and char not in floatSymb:
            return 0;
    return 1;

def printLines(voffset, res, content):
    if res == [-1, -1]:
        for i in range (voffset+2, len(content)):
            print 'INPUT:',content[i][0:]
    ln = res[1] - voffset;
    if ln == 1:
        line = content[res[1]+1]
        print 'INPUT:', line[:len(line)-1]
    elif ln>0:
        i = voffset+2
        while i<res[1]+1:
            line = content[i]
            print 'INPUT:', line[:len(line)-1]
            i+=1
        line = content[res[1]+1]
        print 'INPUT:',line[:res[2]]

def processError(line, offset):
    errorMessage = 'Error: '
    i = offset;
    while line[i] not in spaces and line[i] not in allDelimiters:
        errorMessage += line[i];
        i+=1;
    print errorMessage;
    global errorMarker;
    errorMarker = 1;
    return i-1;

def notEmpty(line):
    if len(line) > 1:
        for char in line:
            if char not in spaces:
                return 1;
    return 0;

def removeSpaces(line):
    i = 0;
    for char in line:
        if char not in spaces:
            return i;
        else:
            i+=1;
    return 0;
#main();

def isID(token):
    if token[0] == 'ID':
        return 1;
    else:
        return 0;

def isNUM(token):
    if token[0] == 'NUM':
        return 1;
    else:
        return 0;



#--------------------Parser Methods Start Here-------------------------

#1
def prg():
    global counter;
    check = TypeSpec();
    if check == 'No':
        return check;
    if isID(nextToken(counter)):
        counter+=1;
    else:
        return 'No';
    check = T();
    if check == 'No':
        return check;
    check = DecListPrime();
    return check;

#2
def DecListPrime():
    global counter;
    check = TypeSpec();
    if check == 'No':
        nt = nextToken(counter);
        if nt[1] == '$':
            return 'Yes'
        else:
            return 'No'
    if isID(nextToken(counter)):
        counter+=1;
    else:
        return 'No';
    check = T();
    if check == 'No':
        return check;
    check = DecListPrime();
    return check;

#3
def T():
    global counter;
    check = VarDecl();
    if check == 'No':
        nt = nextToken(counter);
        if nt[1] == '(':
            counter+=1;
        else:
            return 'No';
        check = Params();
        if check == 'No':
            return check;
        nt = nextToken(counter);
        if nt[1] == ')':
            counter+=1;
        else:
            return 'No';
        check = CompoundStmt();
        if check == 'No':
            return check;
    return check;
#4
def VarDecl():
    global counter;
    nt = nextToken(counter);
    if nt[1] == ';':
        counter+=1;
        return 'Yes';
    elif nt[1] == '[':
        counter+=1;
        if isNUM(nextToken(counter)):
            counter+=1;
            nt = nextToken(counter);
            if nt[1] == ']':
                counter+=1;
                nt = nextToken(counter);
                if nt[1] == ';':
                    counter+=1;
                    return 'Yes';
                else:
                    return 'No'
            else:
                return'No';
        else:return 'No';
    else:
        return 'No';
#5
def TypeSpec():
    global counter;
    nt = nextToken(counter);
    if nt[1] == 'int' or nt[1] == 'void' or nt[1] == 'float':
        counter+=1;
        return 'Yes';
    else:
        return 'No'

#6
def Params():
    global counter;
    nt = nextToken(counter);
    if nt[1] == 'int' or nt[1] == 'float':
        counter+=1;
        nt = nextToken(counter);
        if isID(nt):
            counter += 1;
            check = Y();
            if check == 'No':
                return 'No';
            check = ParamList();
            return check;
        else:
            return 'No';
    elif nt[1] == 'void':
        counter += 1;
        check = P();
        return check;

#7
def P():
    global counter;
    if isID(nextToken(counter)):
        counter += 1;
        check = Y();
        if check == 'No':
            return 'No';
        check = ParamList();
        if check == 'No':
            return 'No';
        return 'Yes'
    elif nextToken(counter)[1] == ')':
        return 'Yes';
    else:
        return 'No';

#8
def ParamList():
    global counter;
    if nextToken(counter)[1] == ',':
        counter += 1;
        check = TypeSpec();
        if check == 'No':
            return 'No';
        if isID(nextToken(counter)):
            counter += 1;
            check = Y();
            if check == 'No':
                return 'No';
            check = ParamList();
            if check == 'No':
                return 'No';
            return 'Yes';
        else:
            return 'No';
    elif nextToken(counter)[1] == ')':
        return 'Yes';
    else:
        return 'No'

#9
def Y():
    global counter;
    if nextToken(counter)[1] == '[':
        counter += 1;
        if nextToken(counter)[1] == ']':
            counter += 1;
            return 'Yes'
        else:
            return 'No'
    elif nextToken(counter)[1] == ',' or nextToken(counter)[1] == ')':
        return 'Yes'
    else:
        return 'No'

#10
def CompoundStmt():
    global counter;
    if nextToken(counter)[1] == '{':
        counter += 1;
        check = LocalDecl();
        if check == 'No':
            return 'No';
        check = StmtList();
        if check == 'No':
            return 'No';
        if nextToken(counter)[1] == '}':
            counter += 1;
            return 'Yes'
        else:
            return 'No'
    else:
        return 'No'

#11
def LocalDecl():
    check = LocalDeclPrime();
    return check;

#12
def LocalDeclPrime():
    global counter;
    check = TypeSpec();
    if check == 'No':
        followSet = ['(', ';', '{', 'if','while','return','}'];
        nt = nextToken(counter);
        if nt[1] in followSet or isNUM(nt) or isID(nt):
            return 'Yes'
        return 'No';
    if isID(nextToken(counter)):
        counter+=1;
        check = VarDecl();
        if check == 'No':
            return 'No';
        check = LocalDeclPrime();
        return check;

#13
def StmtList():
    check = StmtListPrime();
    return check;

#14
def StmtListPrime():
    global counter;
    check = Stmt();
    if check == 'No':
        if nextToken(counter)[1] == '}':
            return 'Yes';
        return 'No';
    check = StmtListPrime();
    return check;

#15
def Stmt():
    check = ExprStmt();
    if check == 'No':
        check = CompoundStmt();
        if check == 'No':
            check = SelectionStmt();
            if check == 'No':
                check = IterStmt();
                if check == 'No':
                    check = ReturnStmt();
    return check;

#16
def ExprStmt():
    global counter;
    if nextToken(counter)[1] == ';':
        counter += 1;
        return 'Yes'
    else:
        check = Expr();
        if check == 'No':
            return 'No';
        if nextToken(counter)[1] == ';':
            counter += 1;
            return 'Yes'

#17
def SelectionStmt():
    global counter;
    if nextToken(counter)[1] == 'if':
        counter += 1;
        if nextToken(counter)[1] == '(':
            counter += 1;
            check = Expr();
            if check == 'No':
                return 'No';
            if nextToken(counter)[1] == ')':
                counter += 1;
                check = Stmt();
                if check == 'No':
                    return 'No';
                check = X();
                return check;
            else:
                return 'No';
        else:
            return 'No';
    else:
        return 'No';

#18
def X():
    global counter;
    nt = nextToken(counter);
    followSet = ['(', ';', '{', 'if','while','return', '}'];
    if nt[1] == 'else':
        #add checking where else belongs
        counter += 1;
        check = Stmt();
        return check;
    elif nt[1] in followSet or isNUM(nt) or isID(nt):
        return 'Yes'
    else:
        return 'No'

#19
def IterStmt():
    global counter;
    if nextToken(counter)[1] == 'while':
        counter += 1;
        if nextToken(counter)[1] == '(':
            counter += 1;
            check = Expr();
            if check == 'No':
                return 'No';
            if nextToken(counter)[1] == ')':
                counter += 1;
                check = Stmt();
                return check;
            else:
                return 'No';
        else:
            return 'No';
    else:
        return 'No';

#20
def ReturnStmt():
    global counter;
    if nextToken(counter)[1] == 'return':
        counter += 1;
        check = ExprStmt();
        return check;
    else:
        return 'No';

#21
def Expr():
    global counter;
    nt = nextToken(counter)
    if isID(nt):
        counter += 1;
        check = Q();
        return check;
    elif nt[1] == '(':
        counter += 1;
        check = Args()
        if check == 'No':
            return 'No'
        if nextToken(counter)[1] == ')':
            counter +=1;
            check = N();
            if check == 'No':
                return 'No';
            check = M();
            if check == 'No':
                return 'No';
            check = L();
            return check;
        else:
            return 'No';
    elif isNUM(nt):
        counter += 1;
        check = N();
        if check == 'No':
            return 'No';
        check = M();
        if check == 'No':
            return 'No';
        check = L();
        return check;
    else:
        return 'No';

#22
def Q():
    global counter;
    if nextToken(counter)[1] == '(':
        counter += 1;
        check = Args();
        if check == 'No':
            return 'No';
        if nextToken(counter)[1] == ')':
            counter +=1;
            check = N();
            if check == 'No':
                return 'No';
            check = M();
            if check == 'No':
                return 'No';
            check = L();
            return check;
        else:
            return 'No';
    else:
        check = V();
        if check == 'No':
            return 'No';
        check = B();
        return check;

#23
def B():
    global counter;
    if nextToken(counter)[1] == '=':
        counter += 1;
        check = Expr();
        return check;
    else:
        check = N();
        if check == 'No':
            return 'No';
        check = M();
        if check == 'No':
            return 'No';
        check = L();
        return check;

#24
def V():
    global counter;
    followSet = [';', ')', ']', '=', '*', '/', '+', '-', '<', '>', '!=', '<=', '>=', '==', ','];
    if nextToken(counter)[1] == '[':
        counter += 1;
        check = Expr();
        if check == 'No':
            return 'No';
        if nextToken(counter)[1] == ']':
            counter += 1;
            return 'Yes'
        else: return 'No'
    elif nextToken(counter)[1] in followSet:
        return 'Yes';
    else:
        return 'No'

#25
def L():
    global counter;
    check = Relop();
    if check == 'No':
        followSet = [';', ')', ']', ','];
        if nextToken(counter)[1] in followSet:
            return 'Yes';
        else: return 'No'
    check == AddExpr();
    return check;

#26
def Relop():
    global counter;
    nt = nextToken(counter);
    firstSet = ['<', '>', '=', '==', '!=', '<=', '>='];
    if nt[1] in firstSet:
        counter += 1;
        return 'Yes'
    else:
        return 'No'

#27
def AddExpr():
    check = Term();
    if check == 'No':
        return 'No';
    check = M();
    return check;

#28
def M():
    global counter;
    check = AddOp();
    if check == 'No':
        followSet = ['<=', '>=', '==', '!=', '<', '>', '=', ';', ')', ']', ','];
        if nextToken(counter)[1] in followSet:
            return 'Yes';
        else:
            return 'No'
    check = Term();
    if check == 'No':
        return 'No';
    check = M();
    return check;

#29
def AddOp():
    global counter;
    nt = nextToken(counter);
    if nt[1] == '+' or nt[1] == '-':
        counter += 1;
        return 'Yes';
    else:
        return 'No';

#30
def Term():
    check = Factor();
    if check == 'No':
        return 'No';
    check = N();
    return check;

#31
def N():
    global counter;
    check = MulOp();
    if check == 'No':
        followSet = ['<=', '>=', '==', '!=', '<', '>', '=', ';', ')', ']', ',', '+', '-'];
        if nextToken(counter)[1] in followSet:
            return 'Yes';
        else:
            return 'No'
    check = Factor();
    if check == 'No':
        return 'No';
    check = N();
    return check;

#32
def Factor():
    global counter;
    nt = nextToken(counter);
    if nt[1] == '(':
        counter += 1;
        check = Expr();
        if check == 'No':
            return 'No'
        if nextToken(counter)[1] == ')':
            counter += 1;
            return 'Yes';
        else:
            return 'No';
    elif isID(nt):
        counter += 1;
        check = S();
        return check;
    elif isNUM(nt):
        counter += 1;
        return 'Yes';
    else: return 'No';

#33
def S():
    global counter;
    if nextToken(counter)[1] == '(':
        counter += 1;
        check = Args();
        if check == 'No':
            return 'No';
        if nextToken(counter)[1] == ')':
            counter += 1;
            return 'Yes';
        else:
            return 'No'
    else:
        check = V();
        return check;

#34
def MulOp():
    global counter;
    nt = nextToken(counter);
    if nt[1] == '*' or nt[1] == '/':
        counter += 1;
        return 'Yes';
    else:
        return 'No';

#35
def Args():
    global counter;
    check = ArgList();
    if check == 'No':
        nt = nextToken(counter);
        if nt[1] == '(' or isID(nt) or isNUM(nt):
            return 'Yes';
        else:
            return 'No'
    else:
        return check;

#36
def ArgList():
    check = Expr();
    if check == 'No':
        return 'No';
    check = ArgListPrime();
    return check;

#37
def ArgListPrime():
    global counter;
    if nextToken(counter)[1] == ',':
        counter += 1;
        check = Expr();
        if check != 'No':
            check = ArgListPrime()
            return check;
        else: return 'No'
    elif nextToken(counter)[1] == ')':
        return 'Yes';
    else:
        return 'No'

main();