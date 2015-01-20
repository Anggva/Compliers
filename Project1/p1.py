__author__ = 'vasilina'
import sys

def main():
    inputFile = sys.argv[1];
    fileVar = open(inputFile, 'r');
    spaces = [' ', '\n'];
    keywords = ['else', 'if','int', 'while', 'return', 'float', 'void'];
    specSymbols = ['+','-','*','/','<','<=','>','>=','==','!=','=',';',',','(',')','[',']','{','}','/*','*/'];
    numbers = ['1','2','3','4','5','6','7','8','9','0'];
    content = fileVar.readlines();
    isStart = 1;
    keywordOn = 0;
    idOn = 0;
    for line in content:
        word = '';
        lineDic = '';
        count = 0;
        c = line.read(1);
        while c != '\n':
            if c in spaces:
                if isStart:
                    continue;
                else:
                    if word in keywords:
                        str = 'keyword'+count;
                        lineDic[str] = word;
                        keywordOn = 1;
                    elif word in specSymbols:
                        str = 'specSymb' + count;
                        lineDic[str] = word;
                    elif aNumber(word, numbers) and idOn:
                        str = 'NUM' + count;
                        lineDic[str] = word;
                    elif idOn or keywordOn:
                        for char in word:
                            if char not in numbers:

            d = line.read(1);

            if c == '/':
                processComment(line);

    while True:
        c = fileVar.read(1);
        if not c:
            print "End of file";
            break;


        # else:
        #    print "Read a character:", c;
    fileVar.close();


def processComment(fileVar):
    d = fileVar.read(1);
    str = d;
    if d != '/' and d != '*': #Not a comment, just a division
        return;
    if d == '/':
        while d != '\n':
            d = fileVar.read(1);
            str+=d;
        return str;
    if d =='*':

def aNumber(line, numbers):
    for char in line:
        if char not in numbers:
            return 0;
        else:
            return 1;


main();