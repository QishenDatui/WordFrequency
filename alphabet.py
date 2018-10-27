import argparse
import collections
import re

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--character", action='count', help="count the character")
    parser.add_argument("file", help="the path of the file")
    
    # 从命令行读取参数
    args = parser.parse_args()
    
    # 如果给出了文件路径
    if args.file:
        # 统计各个字母出现次数
        count = alphabet(args.file)
        print(count)
        exit(0)
    else:
        print("Please give the filepath")
        exit(0)
        