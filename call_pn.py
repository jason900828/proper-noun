#! python3
# coding=UTF-8
import proper_noun as pn
import sys
import json
import os
import csv

timefolder = str(sys.argv[1]);
path = './excel_document/'+timefolder+'/'
f = open(path+'excel_category.json','r',encoding = 'utf-8')
content = f.read()
f.close()
jsondata = json.loads(content)

keyword_input = jsondata['keyword']
keyword_lst = keyword_input.split(' ')

Threshold = 0.7
if jsondata['proper_file'] !='':
    f = open(path+jsondata['proper_file'],'r',encoding = 'utf-8')
    Proper_list = f.readlines()
    f.close()
else:
    Proper_list = ['']

for i in range(len(Proper_list)):
    Proper_list[i] = Proper_list[i].replace('\n','')

excel_name = path+jsondata['excel_file']#input('excel名稱：')
excel_content_at = jsondata['excel_content']#input('文章位置：')

load_text = pn.Loading(excel_name,excel_content_at,path)
load_text.loading_excel()

start_pick = pn.Pick_content(keyword_lst,Proper_list,path,timefolder)
term,mid_word_list = start_pick.pick_words()

start_merge = pn.Merge_word(Threshold,keyword_lst[0])
clu_all,proper_noun_lst,proper_noun_Frequency = start_merge.get_output(term,mid_word_list)


# 開啟輸出的 CSV 檔案
key = ''
if not(os.path.isdir('output/')):
    os.mkdir('output/')
path = 'output/output'+timefolder+'/'
if not(os.path.isdir(path)):
    os.mkdir(path)

for k in keyword_lst:
    key = key+k
with open(path+'output.csv', 'w', newline='') as csvfile:
  # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile,delimiter='\t')

  # 寫入一列資料
    writer.writerow(['keyword', 'Frequency', 'Cluster'])
    for i in range(len(clu_all)):
        if clu_all[i]!='':
            writer.writerow(['cluster = '+clu_all[i],sum(proper_noun_Frequency[i]) , '*'])
        for j in range(len(proper_noun_lst[i])):
            if proper_noun_lst[i][j]!='':
                try:
                    writer.writerow([proper_noun_lst[i][j],proper_noun_Frequency[i][j] , i])
                except:
                    print([proper_noun_lst[i][j],proper_noun_Frequency[i][j] , i],'編碼問題無法寫入')
        writer.writerow([' ','' , ''])        
   