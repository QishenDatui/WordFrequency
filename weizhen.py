import collections
import re
import argparse
#from nltk import tokenize
from time import time
import glob
import os

def print_num(obj):
    for c, p in obj:
        print('%40s\t%d' % (c,p))

def print_float(obj):
    for c, p in obj:
        print('%40s\t%.2f%%' % (c,p*100))

def d_func(function, directory, *ops):
    fileList = glob.glob(os.path.join(directory, '*.txt'))
    for file in fileList:
        print(file)
        function(file, *ops)

def s_func(function, directory, *ops):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                function(os.path.join(maindir, filename), *ops)


def verbsReference(verbs):
    f = open(verbs, "r")
    strmatch = r'\b[a-z]+[a-z0-9]*\b'
    strmatch = re.compile(strmatch)
    verbdict = {}
    for line in f.readlines():
        line = strmatch.findall(line)
        for i in range(len(line)):
            verbdict[line[i]] = line[0]
    f.close()
    return verbdict


def prepositionReference(preposition):
    f = open(preposition, "r")
    preposition_dict = {}
    for line in f.readlines():
        line = line[:-1]
        preposition_dict[line] = 1
    f.close()
    return preposition_dict


def comprise_verbs(line, verb_dict, preposition_dict):
    result = []
    i = 0
    while i < len(line) - 1:
        if line[i] in verb_dict and line[i+1] in preposition_dict:
            result.append(verb_dict[line[i]] + ' ' + line[i + 1])
            i = i + 2
        else:
            i = i + 1
    return result

def comprise_morewords(line, phrase):
    length = len(line) - phrase + 1
    result = []
    i = 0
    j = 0
    temp = []
    while i < length:
        while j < phrase:
            i_j = i + j
            if line[i_j][0] > 'z' or line[i_j][0] < 'a':
                i = i_j
                j = 0
                temp=[]
                break
            temp.append(line[i_j])
            j = j + 1
        if j==phrase:
            j = phrase - 1
            result.append(' '.join(temp))
            temp = temp[1:]
        i = i + 1
    return result
def comprise_verbs_pharse(line, pharse, verb_dict):
    length = len(line) - pharse + 1
    result = []
    for i in range(length):
        flag = True
        temp = ''
        for j in range(pharse):
            if line[i + j][0] > 'z' or line[i  + j][0] < 'a':
                flag = False
                break
            if line[i + j] in verb_dict:
                temp = temp + verb_dict[line[i+j]] + ' '
            else:
                temp = temp + line[i + j] + ' '
        if flag:
            result.append(temp[:-1])
    return result

def filephraseCounter_morewords(filepath, number, stopwords, phrase):
    if phrase < 1:
        return
    if phrase == 1:
        fileWordCounter(filepath, number, stopwords)
        return
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(phrase)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b[0-9a-z]+\b|[^\s0-9a-z]+'
    strmatch = re.compile(strmatch)
    # pynlpir.open()
    templine = []
    temp_phrase = phrase - 1
    if stopwords == None:
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            line = templine + line
            # line = WordSpilt().tokenize(line.lower())
            # line = pynlpir.segment(line.lower(), pos_tagging=False)
            #templine = " ".join(line[-1 * temp_phrase:]) + " "
            templine = line[-1 * temp_phrase:]
            line = comprise_morewords(line, phrase)
            count.update(line)
    else:
        stopfile = open(stopwords, "r", encoding='utf-8', errors='ignore')
        stop = set(stopfile.readline().lower().split(' '))
        stopfile.close()
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            line = [element for element in line if element not in stop]
            line = templine + line
            templine = line[-1 * temp_phrase:]
            line = comprise_morewords(line, phrase)
            count.update(line)
    f.close()
    print('File: ' + filepath)
    if number <= 0:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0])))
    else:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:number])


def fileVerbsPrepositionCounter(filepath, number, stopwords, preposition, verbs):
    verb_dict = verbs
    preposition_dict = preposition
    f = open(filepath, "r")
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(pharse)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b[0-9a-z]+\b|[^\sa-z0-9]'
    strmatch = re.compile(strmatch)
    templine = ""
    if stopwords == None:
        for line in f.readlines():
            line = templine + line
            line = strmatch.findall(line.lower())
            templine = "".join(line[-1:]) + ' '
            line = comprise_verbs(line, verb_dict, preposition_dict)
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = stopfile.readline().lower().split(' ')
        stopfile.close()
        stop = collections.Counter(stop)
        for line in f.readlines():
            line = templine + line
            line = strmatch.findall(line.lower())
            line = [element for element in line if element not in stop]
            templine = "".join(line[-1:]) + ' '
            line = comprise_verbs(line, verb_dict, preposition_dict)
            count.update(line)

    f.close()
    print('File: ' + filepath)
    if number < 0:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0])))
    else:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:number])

def fileVerbsWordCounter(filepath, number, stopwords, verbs):
    verb_dict = verbs
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    strmatch = r'\b[a-z]+[0-9a-z]*\b'
    strmatch = re.compile(strmatch)
    if stopwords == None:
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = set(stopfile.readline().lower().split(' '))
        stopfile.close()
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            count.update(line)
        for element in stop:
            del (count[element])
    f.close()
    for element in verb_dict.keys():
        count[verb_dict[element]] += count[element]
        del (count[element])
    count = count - collections.Counter()
    print('File: ' + filepath)
    if number < 0:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0])))
    else:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:number])


def fileWordCounter(filepath, number, stopwords):
    f = open(filepath, "r",encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    strmatch = re.compile(r"\b[a-z]+[a-z0-9]*\b")
    if stopwords == None:
        for line in f.readlines():
            #line = tokenize.word_tokenize(line.lower())
            #line = [i for i in line if line[0]>='a' and line[0]<='z']
            line = strmatch.findall(line.lower())
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = (stopfile.readline().lower()).split(' ')
        stopfile.close()
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            count.update(line)
        for element in stop:
            del (count[element])
    f.close()
    print('File: ' + filepath)
    if number <= 0:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0])))
    else:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:number])


def fileVerbsPharseCounter(filepath, number, stopwords, pharse, verbs):
    verb_dict = verbs
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(pharse)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b[0-9a-z]+\b|[^\sa-z0-9]'
    strmatch = re.compile(strmatch)
    templine = []
    temp_pharse = pharse - 1
    if stopwords == None:
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            line = templine + line
            templine = line[-1 * temp_pharse:]
            line = comprise_verbs_pharse(line, pharse, verb_dict)
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = set(stopfile.readline().lower().split(' '))
        stopfile.close()
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            line = templine + line
            line = [element for element in line if element not in stop]
            templine = " ".join(line[-1 * temp_pharse:]) + " "
            line = comprise_verbs_pharse(line, pharse, verb_dict)
            count.update(line)
        for element in stop:
            del (count[element])
    f.close()
    if number < 0:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0])))
    else:
        print_num(sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:number])


def alphabet(filepath):
    count = collections.Counter()
   
    f = open(filepath, "r",encoding='utf-8' ,errors='ignore')
    line = f.read()
    line = [i for i in line.lower() if i<='z' and i>='a']
    #line = re.findall(r'[a-z]', line.lower())
    count.update(line)
    f.close()
    
    sumAlphabet = sum(count.values())

    if sumAlphabet == 0:
        return dict()
        
    for key in count.keys():
        count[key] = count[key] / sumAlphabet

    print('File: ' + filepath)
    print_float(sorted(count.items(), key=lambda kv: (-kv[1], kv[0])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=-1, help="output number of the program")
    parser.add_argument("-v", "--verbs", help="filepath of verbs")
    parser.add_argument("-x", "--stopwords", default=None, help="the path of the stopwords file")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--character", help="count the number of character", action='count')
    group.add_argument("-f", "--word", help="count the number of word", action='count')
    group.add_argument("-p", "--phrase", type=int, help="the length of phrase to be counted")
    group.add_argument("-q", "--preposition", help="the filepath of the preposition file")

    group_path = parser.add_mutually_exclusive_group()
    group_path.add_argument("-d", "--directory", help="directory of the file", action='store_true', default=False)
    group_path.add_argument("-s", "--directorys", help="directory of the file", action='store_true', default=False)
    
    parser.add_argument("file", help="the path of the file")
    
    args = parser.parse_args()

    # verb and preposition and phrase:
    if args.file and args.verbs and args.preposition:
        verb_dict = verbsReference(args.verbs)
        preposition_dict = prepositionReference(args.preposition)
        if args.directory:
            d_func(fileVerbsPrepositionCounter, args.file, args.number, args.stopwords, preposition_dict, verb_dict)
        elif args.directorys:
            s_func(fileVerbsPrepositionCounter, args.file, args.number, args.stopwords, preposition_dict, verb_dict)
        else:
            fileVerbsPrepositionCounter(args.file, args.number, args.stopwords, preposition_dict, verb_dict)
        exit()


    # verb and phrase
    if args.file and args.phrase and args.verbs:
        verb_dict = verbsReference(args.verbs)
        if args.directory:
            d_func(fileVerbsPharseCounter, args.file, args.number, args.stopwords, args.pharse, verb_dict)
        elif args.directorys:
            s_func(fileVerbsPharseCounter, args.file, args.number, args.stopwords, args.pharse, verb_dict)
        else:
            fileVerbsPharseCounter(args.file, args.number, args.stopwords, args.pharse, verb_dict)
        exit()

    # phrase
    if args.file and args.phrase:
        if args.directory:
            d_func(filephraseCounter_morewords, args.file, args.number, args.stopwords, args.phrase)
        elif args.directorys:
            s_func(filephraseCounter_morewords, args.file, args.number, args.stopwords, args.phrase)
        else:
            filephraseCounter_morewords(args.file, args.number, args.stopwords, args.phrase)
        exit(0)


    # count words with verbs dictionary
    if args.file and args.verbs and args.word:
        if args.directory:
            d_func(fileVerbsWordCounter,args.file, args.number, args.stopwords, verb_dict)
        elif args.directorys:
            d_func(fileVerbsWordCounter, args.file, args.number, args.stopwords, verb_dict)
        else:
            fileVerbsWordCounter(args.file, args.number, args.stopwords, verb_dict)
        exit()

    # count words
    if args.file and args.word:
        if args.directory:
            d_func(fileWordCounter, args.file, args.number, args.stopwords)
        elif args.directorys:
            s_func(fileWordCounter, args.file, args.number, args.stopwords)
        else:
            fileWordCounter(args.file, args.number, args.stopwords)
        exit()

    # count characters
    if args.file and args.character:
        if args.directory:
            d_func(alphabet, args.file)
        elif args.directorys:
            s_func(alphabet, args.file)
        else:
            alphabet(args.file)
        exit()