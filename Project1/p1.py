__author__ = 'vasilina'
import sys

spaces = [' ', '\n', '\t'];
keywords = ['else', 'if','int', 'while', 'return', 'float', 'void'];
arithmetSymb = ['+','-','*','/'];
compareSymb = ['<','>', '>=', '<=', '==', '!='];
delimiters = [';',',','(',')','[',']','{','}']
floatSymb = ['E', '.', '+', '-'];
superset = arithmetSymb+compareSymb+delimiters+floatSymb
numbers = ['0','1','2','3','4','5','6','7','8','9'];
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];

def main():
    inputFile = sys.argv[1];
    fileVar = open(inputFile, 'r');
    content = fileVar.readlines();
    voffset = -1;
    current = 'start';
    moveToNext = 0;
    word = '';
    specWord = '';
    depth = 0;
    i = 0;
    while i < len(content):
        line = content[i];
        offset = -1;
        j = 0;
        while j < len(line):
            char = line[j];
            if char=='/':
                res = processComment(line, offset, content, voffset);
                if res == 0:
                    pass
                elif res == 1:
                    current = 'comment';
                    print 'INPUT: ', line[(offset+1):len(line)-1]
                    break
                elif res == [-1,-1]:
                    current = 'comment';
                    print 'INPUT: ', line[offset:]
                    printLines(voffset, content)
                    break;
                else:
                    current = 'comment';
                    printLines(offset, voffset,res, content)
                    if res[1] != voffset:
                        voffset = res[1];
                        i = voffset+1;
                        line = content[i];
                    if res[2] >= len(line)-1:
                        break;
                    else:
                        offset = res[2];
                        j = offset+1;
                        char = next(line,offset);
            if char in superset:
                

            if char in alphabet:
                if current != 'number':
                    word+=char
                    offset += 1;
                    # j+=1;
                    current = 'word';
                else:
                    # if char == 'E':

                    processWord(word, depth)
                    print 'Error!: ', char

            elif char in numbers:
                if current != 'word':
                    current = 'number'
                    word+=char
                    offset += 1
                    # j+=1
            elif char in spaces:
                offset+=1
                if current == 'start' or current == 'comment':
                    j+=1
                    continue
                elif len(word) > 0:
                    if current == 'error':
                        print 'Error: ', word;
                    else:
                        processWord(word, depth)
                    word = '';
                    current = 'space';

            elif char in specSymbolsG2:
                d = next(line, offset)
                current = 'spec'
                if d == '=':
                    specWord+=char+d
                    print specWord, '\n'
                    offset+=2
                    processWord(word, depth)
                    word = ''
                    specWord=''
                elif char in specSymbolsG1:
                    processWord(word, depth)
                    word = ''
                    offset += 1
                    specWord += char
                    print specWord
                    specWord = ''
            elif char in specSymbolsG1:
                current = 'spec'
                if len(word) > 0:
                    processWord(word, depth)
                offset += 1;
                word = ''
                specWord += char
                print specWord
                specWord = ''
            elif current == 'error':
                word += char;
            j+=1
        voffset+=1;
        i+=1;
    fileVar.close();


def previous(line, offset):
    if line[offset] != None:
        return line[offset]
    else:
        return None

def next(line, offset):
    if line[offset+2] != None:
        return line[offset+2]
    else:
        return None


def processWord(word, depth):
   # dicEntry='';
    if word in keywords:
        s = 'keyword: '+ word;
    elif aNumber(word, numbers):
        s = 'NUM: ' + word;
    else:
        s = 'ID: ' + word + ' ' + str(depth);
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
        if char not in numbers:
            return 0;
    return 1;
def printLines(voffset, content):
    for i in range (voffset+2, len(content)):
        print content[i][0:]

def printLines(offset, voffset, res, content):
    ln = res[1] - voffset;
    if ln == 0:
        line = content[res[1]+1]
        print 'INPUT: ', line[res[0]+1:res[2]]
    elif ln == 1:
        line = content[voffset+1]
        print 'INPUT: ', line[res[0]+1:len(line)-1]
        line = content[res[1]+1]
        print 'INPUT: ', line[:res[2]]
    else:
        i = voffset+1
        line = content[i]
        print 'INPUT: ', line[offset+1:]
        i+=1
        while i<res[1]:
            line = content[i]
            print 'INPUT: ', line[:len(line)-1]
            i+=1
        line = content[res[1]]
        print line[:res[2]]

main();