__author__ = 'vasilina'
import sys

spaces = [' ', '\n', '\t'];
keywords = ['else', 'if','int', 'while', 'return', 'float', 'void'];
specSymbolsG1 = ['+','-','*','/','<','=',';',',','(',')','[',']','{','}', '!', '>'];
specSymbolsG2 = ['<','>','=','!'];
numbers = ['0-9'];
alphabet = ['a-zA-Z'];

def main():
    inputFile = sys.argv[1];
    fileVar = open(inputFile, 'r');
    content = fileVar.readlines();
    offset = -1;
    voffset = -1;
    current = 'start';
    moveToNext = 0;
    word = '';
    specWord = '';
    depth = 0;
    for line in content:
        for char in line:
            if char=='/':
                res = processComment(line, offset, content, voffset);
                if res == 1:
                    print 'INPUT: ', line[(offset+1):]
                    offset = -1
                    break
                elif res == 0:
                    pass
                elif res == [-1,-1]:
                    print line[offset:]
                    printLines(voffset, content)
                    break;
                else:
                    printLines(offset, voffset,res, content)
                    break;
            if char in alphabet:
                if current != 'number':
                    word+=char
                    offset += 1;
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
            elif char in spaces:
                offset+=1
                if current == 'start':
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
                processWord(word, depth)
                offset += 1;
                word = ''
                specWord += char
                print specWord
                specWord = ''
            elif current == 'error':
                word += char;
        voffset+=1;
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
        str = 'keyword: '+ word;
    elif aNumber(word, numbers):
        str = 'NUM: ' + word;
    else:
        str = 'ID: ' + word + ' ' + depth;
    print str;


def parseLine(line, offset, content, voffset, c1, c2):
    cDepth = 1;
    i = offset + 3
    while i < len(line):
        if line[i] == c2 and line[i+1] == c1:
            cDepth += 1;
            i+=2
            continue;
        elif line[i] == c1 and line[i+1] == c2:
            cDepth -= 1;
            if cDepth == 0:
                return [i, voffset];
            i+=1;
        i+=1;
    for i in range (voffset+2, len(content)):
        line = content[i];
        for j in range (0, len(line)-1):
            if line[j] == c2 and line[j+1] == c1:
                cDepth += 1;
                continue;
            elif line[j] == c1 and line[j+1] == c2:
                cDepth -= 1;
                if cDepth == 0:
                    return [j, i];
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
        print content[i]

def printLines(offset, voffset, res, content):
    ln = res[0] - voffset - 2;
    if ln == -1:
        line = content[res[0]]
        print line[offset+2:res[1]]
    elif ln == 0:
        line = content[voffset+2]
        print line[offset+2:]
        line = content[res[0]]
        print line[:res[1]]
    else:
        i = voffset+1
        line = content[i]
        print 'INPUT: ', line[offset+1:]
        while i<res[1]:
            line = content[i]
            print 'INPUT: ', line
            i+=1
        line = content[res[1]]
        print line[:res[1]]

main();