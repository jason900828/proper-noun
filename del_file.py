import shutil
import os
del_dir = ['./excel_document/','./output/','../sinica-ckip/CKIPWS/input/','../sinica-ckip/CKIPWS/output/']
for dir_ in del_dir:
    del_list = os.listdir(dir_)
    if len(del_list)<100:
    	continue
    else:
    	for del_in in del_list:
    		shutil.rmtree(dir_+del_in)