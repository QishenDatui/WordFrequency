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
    verbdict = {}
    for line in f.readlines():
        line = re.findall(strmatch, line)
        for i in range(1, len(line)):
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
    n = len(line) - 1
    while i < n:
        if line[i] in verb_dict and line[i+1] in preposition_dict:
            result.append('{} {}'.format(verb_dict[line[i]], line[i + 1] ))
            i = i + 2
        else:
            i = i + 1
    return result

def comprise(line, phrase):
    length = len(line) - phrase + 1
    result = []
    for i in range(length):
        result.append(' '.join(line[i:i+phrase]))
    return result

def filePhraseCounter(filepath, number, stopwords, phrase):
    if phrase < 1:
        return
    if phrase == 1:
        fileWordCounter(filepath, number, stopwords)
        return
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    re_line = re.compile(r'[a-zA-Z0-9\s]+')
    strmatch = re.compile(r'(?<![a-z0-9])[a-z][a-z0-9]*')
    if stopwords == None:
        for line in re_line.findall(f.read()):
            line = strmatch.findall(line.lower())
            line = comprise(line, phrase)
            count.update(line)
    else:
        stopfile = open(stopwords, "r", encoding='utf-8', errors='ignore')
        stop = set(stopfile.readline().lower().split(' '))
        stopfile.close()
        for line in re_line.findall(f.read()):
            line = strmatch.findall(line.lower())
            line = [element for element in line if element not in stop]
            line = comprise(line, phrase)
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
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    re_line = re.compile(r'[a-zA-Z0-9\s]+')
    strmatch = re.compile(r'(?<![a-z0-9])[a-z][a-z0-9]*')
    if stopwords == None:
        for line in re_line.findall(f.read()):
            line = strmatch.findall(line.lower())
            line = comprise_verbs(line, verb_dict, preposition_dict)
            count.update(line)
    else:
        stopfile = open(stopwords, "r", encoding='utf-8', errors='ignore')
        stop = stopfile.readline().lower().split(' ')
        stopfile.close()
        stop = collections.Counter(stop)
        for line in re_line.findall(f.read()):
            line = strmatch.findall(line.lower())
            line = [element for element in line if element not in stop]
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
    strmatch = re.compile(r'(?<![a-z0-9])[a-z][a-z0-9]*')
    if stopwords == None:
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            #line = [verb_dict.get(element, element) for element in line]
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = set(stopfile.readline().lower().split(' '))
        stopfile.close()
        for line in f.readlines():
            line = strmatch.findall(line.lower())
            #line = [verb_dict.get(element, element) for element in line]
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
    strmatch = re.compile(r'(?<![a-z0-9])[a-z][a-z0-9]*')
    if stopwords == None:
        for line in f.readlines():
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


def fileVerbsPhraseCounter(filepath, number, stopwords, phrase, verbs):
    verb_dict = verbs
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    count = collections.Counter("")
    re_line = re.compile(r'[a-zA-Z0-9\s]+')
    strmatch = re.compile(r'(?<![a-z0-9])[a-z][a-z0-9]*')
    if stopwords == None:
        for line in re_line.findall(f.read()):
            line = strmatch.findall(line.lower())
            line = [verb_dict.get(element, element) for element in line]
            line = comprise(line, phrase)
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = set(stopfile.readline().lower().split(' '))
        stopfile.close()
        for line in re_line.findall(f.read()):
            line = strmatch.findall(line.lower())
            line = [verb_dict.get(element, element) for element in line if element not in stop]
            line = comprise(line, phrase)
            count.update(line)
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
    s  =time()
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
        e = time()
        print(e - s)
        exit()


    # verb and phrase
    if args.file and args.phrase and args.verbs:
        verb_dict = verbsReference(args.verbs)
        if args.directory:
            d_func(fileVerbsPhraseCounter, args.file, args.number, args.stopwords, args.phrase, verb_dict)
        elif args.directorys:
            s_func(fileVerbsPhraseCounter, args.file, args.number, args.stopwords, args.phrase, verb_dict)
        else:
            fileVerbsPhraseCounter(args.file, args.number, args.stopwords, args.phrase, verb_dict)
        e = time()
        print(e - s)
        exit()

    # phrase
    if args.file and args.phrase:
        if args.directory:
            d_func(filePhraseCounter, args.file, args.number, args.stopwords, args.phrase)
        elif args.directorys:
            s_func(filePhraseCounter, args.file, args.number, args.stopwords, args.phrase)
        else:
            filePhraseCounter(args.file, args.number, args.stopwords, args.phrase)
        e = time()
        print(e - s)
        exit(0)


    # count words with verbs dictionary
    if args.file and args.verbs and args.word:
        verb_dict = verbsReference(args.verbs)
        if args.directory:
            d_func(fileVerbsWordCounter,args.file, args.number, args.stopwords, verb_dict)
        elif args.directorys:
            d_func(fileVerbsWordCounter, args.file, args.number, args.stopwords, verb_dict)
        else:
            fileVerbsWordCounter(args.file, args.number, args.stopwords, verb_dict)
        e = time()
        print(e - s)
        exit()

    # count words
    if args.file and args.word:
        if args.directory:
            d_func(fileWordCounter, args.file, args.number, args.stopwords)
        elif args.directorys:
            s_func(fileWordCounter, args.file, args.number, args.stopwords)
        else:
            fileWordCounter(args.file, args.number, args.stopwords)
        e = time()
        print(e - s)
        exit()

    # count characters
    if args.file and args.character:
        if args.directory:
            d_func(alphabet, args.file)
        elif args.directorys:
            s_func(alphabet, args.file)
        else:
            alphabet(args.file)
        e = time()
        print(e - s)
        exit()