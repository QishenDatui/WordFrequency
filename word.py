import os
import glob
import argparse
import collections
import re


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

def fileWordCounter(filepath, number):
    
    f = open(filepath, "r")
    count = collections.Counter("")
    for line in f.readlines():
        # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
        line = re.findall(r"\b[a-z]+[a-z0-9]*\b", line.lower())
        count.update(line)
    
    f.close()

    if number < 1:
        return count.most_common()
    
    return count.most_common(number) 


def directoryWordCounter(directory, number):
    fileList = glob.glob(directory+'*.txt')
    for file in fileList:
        count = fileWordCounter(file, number)
        print("the words in %s are" % file)
        print(count)

def allDirectoryWordCounter(directory, number):
    for maindir, _, fileList in os.walk(directory):
        for filename in fileList:
            if filename[-4:] == ".txt":
                count = fileWordCounter(maindir+'/'+filename, number)
                print("%s has words:" % filename)
                print(count)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=-1, help="output number of the program")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--character", help="count the number of character", action='count')
    group.add_argument("-f", "--word", help="count the number of word", action='count')
    group_path = parser.add_mutually_exclusive_group()
    group_path.add_argument("-d", "--directory", help="directory of the file", action='count')
    group_path.add_argument("-s", "--directorys", help="directory of the file", action='count')
    parser.add_argument("file", help="the path of the file")
    args = parser.parse_args()
    
    if args.file and args.word:
        count = fileWordCounter(args.file, args.number)
        print(count)
        exit(0)
    
    if args.directory and args.file and args.word:
        directoryWordCounter(args.directory, args.number)
        exit(0)
    
    if args.directorys and args.file and args.word:
        allDirectoryWordCounter(args.directorys, args.number)
        exit(0)

    if args.file and args.character:
        count = alphabet(args.file)
        print(count)
        exit(0)

