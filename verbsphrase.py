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
            result.append(temp.rstrip())
    return result

    
def verbsReference(verbs):
    f = open(verbs, "r")
    strmatch = r'\b[a-z]+[a-z0-9]*\b'
    verbdict = {}
    for line in f.readlines():
        line = re.findall(strmatch, line)
        for i in range(1,len(line)):
            verbdict[line[i]] = line[0]

    return verbdict

def fileWordCounter(filepath, number, stopwords, pharse, verbs):
    
    verb_dict = verbsReference(verbs)
    f = open(filepath, "r")
    count = collections.Counter("")
    # strmatch = [r"\b\w+" for i in range(pharse)]
    # strmatch = ''.join(strmatch)
    strmatch = r'\b[a-z]+[a-z0-9]*\b|[^\sa-z0-9]'
    strmatch = re.compile(strmatch)
    if stopwords == None:
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
            line = comprise(line, pharse)
            count.update(line)
    else:
        stop = (open(stopwords, "r").readline().lower()).split(' ')
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

    if number == -1:
        return count.most_common()
    
    return count.most_common(number) 


def directoryWordCounter(directory, number, stopwords, pharse):
    fileList = glob.glob(directory+'*.txt')
    for file in fileList:
        count = fileWordCounter(file, number, stopwords, pharse)
        print("the words in %s are" % file)
        print(count)

def allDirectoryWordCounter(directory, number, stopwords, pharse):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                count = fileWordCounter(maindir.join('/'.join(filename)), number, stopwords, pharse)
                print("%s has words:" % filename)
                print(count)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=-1, help="output number of the program")
    parser.add_argument("-v", "--verbs", help="filepath of verbs")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="path of the file")
    group.add_argument("-d", "--directory", help="directory of the file")
    group.add_argument("-s", "--directorys", help="directory of the file")
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-x", "--stopwords", default=None, help="the path of the stopwords file")
    group2.add_argument("-p", "--pharse", type=int, default=1, help="the length of pharse to be counted")
    args = parser.parse_args()
    
    if args.file and args.verbs:
        start_time = time()
        count = fileWordCounter(args.file, args.number, args.stopwords, args.pharse, args.verbs)
        print(count)
        end_time = time()
        print("total time is ",end_time - start_time)
        exit(0)
    
    if args.directory:
        directoryWordCounter(args.directory, args.number, args.stopwords, args.pharse)
        exit(0)
    
    if args.directorys:
        allDirectoryWordCounter(args.directorys, args.number, args.stopwords, args.pharse)
        exit(0)
