import os
import glob
import argparse
import collections
import re


def fileWordCounter(filepath, number, stopwords, pharse):
    
    f = open(filepath, "r")
    count = collections.Counter("")
    strmatch = [r"[a-z]+[0-9a-z]* " for i in range(pharse)]
    strmatch = ''.join(strmatch).rstrip()
    if stopwords == None:
        for line in f.readlines():
            # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
            line = re.findall(strmatch, line.lower())
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="path of the file")
    group.add_argument("-d", "--directory", help="directory of the file")
    group.add_argument("-s", "--directorys", help="directory of the file")
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-x", "--stopwords", default=None, help="the path of the stopwords file")
    group2.add_argument("-p", "--pharse", type=int, default=1, help="the length of pharse to be counted")
    args = parser.parse_args()
    
    if args.file:
        count = fileWordCounter(args.file, args.number, args.stopwords, args.pharse)
        print(count)
        exit(0)
    
    if args.directory:
        directoryWordCounter(args.directory, args.number, args.stopwords, args.pharse)
        exit(0)
    
    if args.directorys:
        allDirectoryWordCounter(args.directorys, args.number, args.stopwords, args.pharse)
        exit(0)