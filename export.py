# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:13:46 2024

@author: junwen.fang
"""

import os
import glob
import shutil
import easygui
#import re

filepath=easygui.diropenbox(title='Choose sequencing folder')

#Use glob.glob(recursive=True) for proper implementation
#Change glob_depth to adjust te depth of the search
glob_findchar="/??????_*_*_*"
depth="/*"
glob_depth=3
list=[]

for x in range(glob_depth):
    glob_pattern=filepath+depth*x+"/??????_*_*_*"
    list+=glob.glob(glob_pattern)

list=[x for x in list if os.path.isdir(x)]

# pattern=re.compile("[0-9]{6}[_][a-zA-Z0-9]*[_][a-zA-Z0-9]*[_][a-zA-Z0-9]*")
# for root, dirs, file in os.walk(filepath):
    # for name in dirs:
    #     print(name)
    #     if pattern.findall(name):
    #         list.append(os.path.join(root,name))
    #         print(name)

# name_check=glob.iglob((filepath+"/**/[0-9]*_*_*_*/"),recursive=True)

# for x in name_check:
#     if os.path.isdir(x):
#         list.append(x)
        
output=easygui.diropenbox(title='Choose output location')
output=output+"\sequencing_summary"
files=("RunInfo.xml","RunParameters.xml")

print(f"Files will be exported to {output}")

counter=0
error_counter=0
length=len(list)
for path in list:
    run_name=os.path.basename(path)
    counter+=1
    if not os.path.isdir(output+"/"+run_name):
        os.makedirs(output+"/"+run_name)
        try:
            for file in files:
                shutil.copyfile(path+"/"+file, output+"/"+run_name+"/"+file)
            shutil.copytree(path+"/InterOp",output+"/"+run_name+"/InterOp")
            print(f"{run_name} has been processed successfully {counter}/{length}")
        except:
            error_counter+=1
            print(f"Error processing {run_name}")
            continue

print(f"Batch ran successfully with {error_counter} errors.")
    
    
