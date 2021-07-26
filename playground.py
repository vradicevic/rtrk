import os


file_list=os.listdir(r"D:\\logovi\\3PROC_OPTI\\")

for file in file_list:
    print(file[0:-13])