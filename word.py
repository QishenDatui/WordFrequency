import os
import glob
import argparse
import collections
import re


def fileWordCounter(filepath, number):
    
    f = open(filepath, "r")
    count = collections.Counter("")
    for line in f.readlines():
        # 此处问题为若字符串有 \f ，则会被认为是一个转义字符
        line = re.findall(r"\b[a-z]+[a-z0-9]*\b", line.lower())
        count.update(line)
    
    f.close()

    if number == -1:
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
    group.add_argument("-f", "--file", help="path of the file")
    group.add_argument("-d", "--directory", help="directory of the file")
    group.add_argument("-s", "--directorys", default="./", help="directory of the file")
    args = parser.parse_args()
    
    if args.file:
        count = fileWordCounter(args.file, args.number)
        print(count)
        exit(0)
    
    if args.directory:
        directoryWordCounter(args.directory, args.number)
        exit(0)
    
    if args.directorys:
        allDirectoryWordCounter(args.directorys, args.number)
        exit(0)

