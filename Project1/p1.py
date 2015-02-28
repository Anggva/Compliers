__author__ = 'vasilina'
import sys

spaces = [' ', '\n', '\t'];
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
                    current = 'arithmetic symbol'
                    print char;
                    offset += 1;
                elif char in compareSymb:
                    d = next(line, offset);
                    if d == '=':
                        current = 'comparison';
                        specWord+=char+d
                        print specWord
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
                        current = 'comparison'
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
                else:
                    current = 'specSymbol'
                    offset += 1;
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
main();