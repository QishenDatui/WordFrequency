import argparse
import collections
import re

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def main(filepath):
    count = collections.Counter(alphabet)
   
    f = open(filepath, "r")
    
    for line in f.readlines():
        # 匹配所有字母
        line = re.findall(r'[a-z]', line.lower())
        count.update(line)
    
    f.close()
    
    sumAlphabet = sum(count.values())
        
    for key in count.keys():
        count[key] = round(count[key] / sumAlphabet, 2)
    
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="./test.txt", help="directory of the file")
    
    # 从命令行读取参数
    args = parser.parse_args()
    
    # 如果给出了文件路径
    if args.file:
        # 统计各个字母出现次数
        count = main(args.file)
        print(count.most_common())
        exit(0)
    else:
        print("Please give the filepath")
        exit(0)
        