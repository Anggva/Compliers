__author__ = 'vasilina'
import sys

spaces = [' ', '\n', '\t'];
keywords = ['else', 'if','int', 'while', 'return', 'float', 'void'];
specSymbolsG1 = ['+','-','*','/','<','=',';',',','(',')','[',']','{','}', '!', '>'];
specSymbolsG2 = ['<=','>=','==','!=']
numbers = ['1','2','3','4','5','6','7','8','9','0'];
alphabet = ['a-zA-Z']

class T(object):
    def __init__(self, type, depth):
        self.type = type
        self.depth = depth


def main():
    inputFile = sys.argv[1];
    fileVar = open(inputFile, 'r');
    content = fileVar.readlines();
    offset = -1;
    voffset = -1;
    current = 0;
    isStart = 1;

    keywordOn = 0;
    idOn = 0;
    j=0;
    word = ''
    for line in content:
        for char in line:
            if char=='/':
                res = processComment(line, offset);
                if res == 1:
                    print line[offset:]
                    offset = -1
                    voffset += 1
                elif res == 0:
                    pass
                elif res == [-1,-1]:
                    print line[offset:]
                    printLines(voffset, content)
                    break;
                else:
                    printLines(offset, voffset,res, content)
            if char in alphabet:
                word+=char
                d = next(line, offset)
                if d in numbers:
                    #Err
                if d in spaces or d in specSymbolsG1:
                    #place word into a category and check if it was a reserved word

        word = '';
        lineDic = '';
        count = 0;
        i = 0;
        for c in line:
            if c in spaces:
                if isStart:
                    continue;
                else:
                    if word.len>0:
                        processWord(word,count);
                        count+=1;
                        word='';
            elif c in specSymbols:
                processWord(word,count);
            elif c == '/':
                processComment(line[i:], content, i, j);
            i+=1;

        voffset+=1;
        # else:
        #    print "Read a character:", c;
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


def processWord(word, count):
    dicEntry='';
    if word in keywords:
        str = 'keyword'+count;
        dicEntry[str] = word;
    elif word in specSymbols:
        str = 'specSymb' + count;
        dicEntry[str] = word;
    elif aNumber(word, numbers):
        str = 'NUM' + count;
        dicEntry[str] = word;


def parseLine(line, offset, content, voffset, c1, c2):
    for i in range (offset+3,len(line)):
        if line[i] == c1 and line[i+1] == c2:
            return [i, voffset];
    for i in range (voffset+2, len(content)):
        line = content[i]
        for j in range (0, len(line)):
            if line[j] == c1 and line[j+1] == c2:
                return [j, i];
    return [-1,-1];

def processComment(line, offset, content, voffset):
    c = next(line, offset);
    if c != '/' or c != '*':
        return 0;
    elif c == '/':
        return 1;
    elif c == '*':
        return parseLine(line, offset, content, voffset, '*', '/');


    for c in line:
        if c != '/' and c != '*': #Not a comment, just a division
            return;
        if c == '*':
        while d != '\n':
            d = fileVar.read(1);
            str+=d;
        return str;
    if d =='*':

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
    elif ln == 0
        line = content[voffset+2]
        print line[offset+2:]
        line = content[res[0]]
        print line[:res[1]]
    else:
        i = voffset+2
        line = content[i]
        print line[offset+2:]
        while i<res[0]:
            line = content[i]
            print line
        line = content[res[0]]
        print line[:res[1]]

main();