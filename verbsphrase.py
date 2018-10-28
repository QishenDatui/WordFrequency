import os
import glob
import argparse
import collections
import re
from time import time


def comprise(line, pharse):
    length = len(line) - pharse + 1
    result = []
    for i in range(length):
        flag = True
        temp = ''
        for j in range(pharse):
            # 这部分判断可以优化
            if line[i + j][0] > 'z' or line[i + j][0] < 'a':
                flag = False
                break
            temp = temp + line[i + j] + ' '
        if flag:
            result.append(temp[:-1])
    return result

def comprise_verbs(line, pharse, verb_dict):
    length = len(line) - pharse + 1
    result = []
    for i in range(length):
        flag = True
        temp = ''
        for j in range(pharse):
            # 这部分判断可以优化
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

def filePharseCounter(filepath, number, stopwords, pharse):
    
    f = open(filepath, "r")
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(pharse)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b\w+\b|[^\s\w]'
    strmatch = re.compile(strmatch)
    if stopwords == None:
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            line = comprise(line, pharse)
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = stopfile.readline().lower().split(' ')
        stopfile.close()
        stop = collections.Counter(stop)
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            line = [element for element in line if element not in stop]
            line = comprise(line, pharse)
            count.update(line)
    
    f.close()

    if number == -1:
        return count.most_common()
    
    return count.most_common(number) 


def directoryPharseCounter(directory, number, stopwords, pharse):
    fileList = glob.glob(directory+'*.txt')
    for file in fileList:
        count = fileWordCounter(file, number, stopwords, pharse)
        print("the words in %s are" % file)
        print(count)

def allDirectoryPharseCounter(directory, number, stopwords, pharse):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                count = fileWordCounter(maindir.join('/'.join(filename)), number, stopwords, pharse)
                print("%s has words:" % filename)
                print(count)

def verbsWordReference(verbs):
    f = open(verbs, "r")
    strmatch = r'\b[a-z]+[a-z0-9]*\b'
    verbdict = {}
    for line in f.readlines():
        line = re.findall(strmatch, line)
        for i in range(1,len(line)):
            verbdict[line[i]] = line[0]

    f.close()

    return verbdict

def fileVerbsWordCounter(filepath, number, stopwords, verbs):
    
    verb_dict = verbsWordReference(verbs)
    f = open(filepath, "r")
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(pharse)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b[a-z]+[0-9a-z]*\b'
    strmatch = re.compile(strmatch)
    if stopwords == None:
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = stopfile.readline().lower().split(' ')
        stopfile.close()
        stop = collections.Counter(stop)
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            count.update(line)
        for element in stop:
            del(count[element])
    
    f.close()

    for element in verb_dict.keys():
        count[verb_dict[element]] += count[element]
        del(count[element])

    
    count = count - collections.Counter()


    if number == -1:
        return count.most_common()
    
    return count.most_common(number) 

def fileVerbsPharseCounter(filepath, number, stopwords, pharse, verbs):
    verb_dict = verbsWordReference(verbs)
    f = open(filepath, "r")
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(pharse)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b\w+\b|[^\sa-z0-9]'
    strmatch = re.compile(strmatch)
    if stopwords == None:
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            line = comprise_verbs(line, pharse, verb_dict)
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = stopfile.readline().lower().split(' ')
        stopfile.close()
        stop = collections.Counter(stop)
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            line = [element for element in line if element not in stop]
            line = comprise_verbs(line, pharse, verb_dict)
            count.update(line)
        for element in stop:
            del(count[element])
    
    f.close()

    if number == -1:
        return count.most_common()
    
    return count.most_common(number) 


def directoryVerbsPharseCounter(directory, number, stopwords, pharse, verbs):
    fileList = glob.glob(directory+'*.txt')
    for file in fileList:
        count = fileVerbsPharseCounter(file, number, stopwords, pharse, verbs)
        print("the words in %s are" % file)
        print(count)

def allDirectoryVerbsPharseCounter(directory, number, stopwords, pharse, verbs):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                count = fileVerbsPharseCounter(maindir.join('/'.join(filename)), number, stopwords, pharse, verbs)
                print("%s has words:" % filename)
                print(count)

def directoryVerbsWordCounter(directory, number, stopwords, verbs):
    fileList = glob.glob(directory+'*.txt')
    for file in fileList:
        count = fileVerbsWordCounter(file, number, stopwords, verbs)
        print("the words in %s are" % file)
        print(count)

def allDirectoryVerbsWordCounter(directory, number, stopwords, verbs):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                count = fileVerbsWordCounter(maindir.join('/'.join(filename)), number, stopwords, verbs)
                print("%s has words:" % filename)
                print(count)

def alphabet(filepath):
    count = collections.Counter()
   
    f = open(filepath, "r")
    
    for line in f.readlines():
        # 匹配所有字母
        line = re.findall(r'[a-z]', line.lower())
        count.update(line)
    
    f.close()
    
    sumAlphabet = sum(count.values())

    if sumAlphabet == 0:
        return dict()
        
    for key in count.keys():
        count[key] = round(count[key] / sumAlphabet, 2)
    
    return count.most_common()

def fileWordCounter(filepath, number, stopwords):
    
    f = open(filepath, "r")
    count = collections.Counter("")
    if stopwords == None:
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(r"\b[a-z]+[a-z0-9]*\b", line.lower())
            count.update(line)
    else:
        stopfile = open(stopwords, "r")
        stop = (stopfile.readline().lower()).split(' ')
        stopfile.close()
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(r"\b[a-z]+[a-z0-9]*\b", line.lower())
            count.update(line)
        for element in stop:
            del(count[element])
    f.close()

    if number == -1:
        return count.most_common()
    
    return count.most_common(number) 


def directoryWordCounter(directory, number, stopwords):
    fileList = glob.glob(directory+'*.txt')
    for file in fileList:
        count = fileWordCounter(file, number, stopwords)
        print("the words in %s are" % file)
        print(count)

def allDirectoryWordCounter(directory, number, stopwords):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                count = fileWordCounter(maindir.join('/'.join(filename)), number, stopwords)
                print("%s has words:" % filename)
                print(count)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=-1, help="output number of the program")
    parser.add_argument("-v", "--verbs", help="filepath of verbs")
    parser.add_argument("-x", "--stopwords", default=None, help="the path of the stopwords file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--character", help="count the number of character", action='count')
    group.add_argument("-f", "--word", help="count the number of word", action='count')
    group.add_argument("-p", "--pharse", type=int, help="the length of phrase to be counted")
    group_path = parser.add_mutually_exclusive_group()
    group_path.add_argument("-d", "--directory", help="directory of the file", action='count')
    group_path.add_argument("-s", "--directorys", help="directory of the file", action='count')
    parser.add_argument("file", help="the path of the file")
    args = parser.parse_args()
    
    if args.directory and args.file and args.verbs and args.pharse:
        directoryWordCounter(args.directory, args.number, args.stopwords, args.pharse, args.verbs)
        exit(0)
    
    if args.directorys and args.file and args.verbs and args.pharse:
        allDirectoryWordCounter(args.directorys, args.number, args.stopwords, args.pharse, args.verbs)
        exit(0)

    if args.file and args.verbs and args.pharse:
        start_time = time()
        count = fileVerbsPharseCounter(args.file, args.number, args.stopwords, args.pharse, args.verbs)
        print(count)
        end_time = time()
        print("total time is ",end_time - start_time)
        exit(0)

    if args.directory and args.file and args.verbs and args.word:
        directoryVerbsWordCounter(args.directory, args.number, args.stopwords, args.verbs)
        exit(0)
    
    if args.directorys and args.file and args.verbs and args.word:
        allDirectoryVerbsWordCounter(args.directorys, args.number, args.stopwords, args.verbs)
        exit(0)

    if args.file and args.verbs and args.word:
        start_time = time()
        count = fileVerbsWordCounter(args.file, args.number, args.stopwords, args.verbs)
        print(count)
        end_time = time()
        print("total time is ",end_time - start_time)
        exit(0)
