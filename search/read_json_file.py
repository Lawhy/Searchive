import sys
sys.path.append('..')  # append the main directory path
from preprocess.normalise import Normaliser


"""customise the filepath in readindex_no_pos.py"""
import os
def walkFile(file):
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            print('file_path', os.path.join(root, f))
            initialise(os.path.join(root, f))

        # 遍历所有的文件夹
        for d in dirs:
            print('Dirs',os.path.join(root, d))

def readfiles():
    walkFile("/Users/mac/Documents/TTDS")

if __name__ == '__main__':
    readfiles()
    # start_time = time.time()
    '''test'''

    write("/Users/mac/Documents/TTDS/2019index.pkl",title_dict)
    # print(read_index_file("/Users/mac/Documents/TTDS/2019index.pkl"))
    # print("--- %s seconds ---" % (time.time() - start_time))




"""customise the filepath yourself"""
# initialise("/Users/AlisonLee/Desktop/ttdsdata/2016/1601.json")
#update(old_file_path, new_file_path)
import os
def walkFile(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print('file_path', os.path.join(root, f))
            initialise(os.path.join(root, f))

        # 遍历所有的文件夹
        for d in dirs:
            print('Dirs',os.path.join(root, d))

def main():
    walkFile("/Users/mac/Documents/TTDS")

if __name__ == '__main__':
    main()