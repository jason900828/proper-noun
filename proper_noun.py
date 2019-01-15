#! python3
# coding='UTF-8'
import re
import pandas as pd
import os


class Loading:###load指定的excel，並測試轉碼###
    """docstring for Loading"""
    def __init__(self,excel_name,excel_content_at,path):
        self.excel_name = excel_name
        self.excel_content_at = excel_content_at
        self.path = path

    def clean_url(self,temp_data):#清理url
        results=re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
    
        temp_data=results.sub("",str(temp_data))
        results=re.compile(r'https://[a-zA-Z0-9.?/&=:]*',re.S)
    
        temp_data=results.sub("",str(temp_data))
        #print(time1-time0)
        return temp_data

    def check_encode(self,message_lst):#檢查是否為utf-16le
        f = open(self.path+'content.txt','w',encoding = 'utf-16le')
        for message in message_lst:
            str_ = b''
            for j in range(len(message)):
                try:
                    str_ = str_ + message[j].encode('utf-16le')
                except:
                    print('Waring!! This word can\'t be encoding by utf-16le ，will pass \''+message[j]+'\'')
                    continue
    
            f.write(str_.decode('utf-16le')+'\n')#
        f.close()

    def loading_excel(self):#load excel內文
        message_lst = []
        df = pd.read_excel(self.excel_name)
        df_message = df[self.excel_content_at].fillna('N/A')
        rate = 0
        for df_content in df_message:
            #print('Loading '+str(rate),end='\r')
            if df_content == 'N/A':
                continue
            message_lst.append(self.clean_url(df_content).replace('\n',',').replace('\r',''))
            rate+=1
        self.check_encode(message_lst)
        
class Pick_content:#取出含有keyword的前後20個字
    """docstring for Pick_content"""
    def __init__(self,keyword_lst,Proper_list,path,timefolder = '123'):
        self.keyword_lst = keyword_lst
        self.Proper_list = Proper_list
        self.keyword = keyword_lst[0]
        self.path = path
        self.timefolder = timefolder

    def load_content(self):#取出確認為UTF-16LE編碼的文章
        f = open(self.path+'content.txt','r',encoding = 'utf-16le')
        content_lst = f.readlines()
        f.close()
        return content_lst
    def pick_for_back_20(self,content_lst):#抓取前後20個字，如有前或後小於20個字元，則會抓取到最長字數
        summary_forward = []
        summary_backward = []
        rate = 0
        for content in content_lst:
            start = content.find(self.keyword)
            end_ = content.rfind(self.keyword)
    
            #print("catch 20 words : complete"+ str(rate),end='\r')
            rate+=1
            while True:
        
                if end_ == -1:
                    break
        
                keyword_all_have = 1
                if start-20 < 0 and start+20>len(content):
                    for k in self.keyword_lst:
                        if k == self.keyword:
                            continue
                        if k in content[0:start] or k in content[start+len(self.keyword):-1]:
                            keyword_all_have = 1
                        else:
                            keyword_all_have = 0
                    if keyword_all_have == 1:
                        if content[0:start] == '':
                            summary_forward.append("N/A")
                        else:
                            summary_forward.append(content[0:start])
                        if content[start+len(self.keyword):-1] == '':
                            summary_backward.append("N/A")
                        else:
                            summary_backward.append(content[start+len(self.keyword):-1])
                elif start-20 < 0:
                    for k in self.keyword_lst:
                        if k == self.keyword:
                            continue
                        if k in content[0:start] or k in content[start+len(self.keyword):start+len(self.keyword)+20]:
                            keyword_all_have = 1
                        else:
                            keyword_all_have = 0
                    if keyword_all_have == 1:
                        if content[0:start] == '':
                            summary_forward.append("N/A")
                        else:
                            summary_forward.append(content[0:start])
                        summary_backward.append(content[start+len(self.keyword):start+len(self.keyword)+20])
                
                elif start+20 > len(content):
                    for k in self.keyword_lst:
                        if k == self.keyword:
                            continue
                        if k in content[start-20:start] or k in content[start+len(self.keyword):-1]:
                            keyword_all_have = 1
                        else:
                            keyword_all_have = 0
                    if keyword_all_have == 1:
                        summary_forward.append(content[start-20:start])
                        if content[start+len(self.keyword):-1] == '':
                            summary_backward.append("N/A")
                        else:
                            summary_backward.append(content[start+len(self.keyword):-1])
        
                else:
                    for k in self.keyword_lst:
                        if k == self.keyword:
                            continue
                        if k in content[start-20:start] or k in content[start+len(self.keyword):start+len(self.keyword)+20]:
                            keyword_all_have = 1
                        else:
                            keyword_all_have = 0
                    if keyword_all_have == 1:
                        summary_forward.append(content[start-20:start])
                        summary_backward.append(content[start+len(self.keyword):start+len(self.keyword)+20])

                if end_==start:
                    break
                else:
                    start = content.find(self.keyword,start+len(self.keyword))
        return summary_forward,summary_backward

    def pick_proper(self,summary_forward,summary_backward):#尋找有無與使用者指定之Proper_list相符的字眼，若有，則調整結構
        mid_word_list = []
        for c in range(len(summary_forward)):
            mid_word_list.append(self.keyword)
        Max_Pnoun_size = 0
        for word in self.Proper_list:
            if len(word)>Max_Pnoun_size:
                Max_Pnoun_size = len(word)

        for i in range(len(summary_forward)):
            #前後抓取Max_Pnoun_size個字，尋找是否有匹配之文字
            if len(summary_forward[i])>Max_Pnoun_size : 
                str_small = summary_forward[i][-Max_Pnoun_size:-1]+summary_forward[i][-1]+mid_word_list[i]
            elif summary_forward[i] == 'N/A':
                str_small = mid_word_list[i]
            else:
                str_small = summary_forward[i][0:-1]+summary_forward[i][-1]+mid_word_list[i]
            if len(summary_backward[i])>Max_Pnoun_size:
                str_small = str_small +summary_backward[i][0:Max_Pnoun_size]
            elif summary_backward == 'N/A':
                str_small = str_small
            else:
                str_small = str_small +summary_backward[i][0:-1]

            for pro in self.Proper_list:  
                if pro in str_small:
                    #print(str_small,pro)
                    if mid_word_list[i]=='':
                        mid_word_list[i] = pro
                        str_all = summary_forward[i]+self.keyword+summary_backward[i]
                        a = str_all.find(str_small)
                        b = str_small.find(pro)
                        summary_forward[i] = str_all[0:a+b]
                        summary_backward[i] = str_all[a+b+len(pro):-1]
                        #print(summary_forward[i],mid_word_list[i],summary_backward[i])
                    else:
                        if len(mid_word_list[i])<len(pro):
                            mid_word_list[i] = pro
                            str_all = summary_forward[i]+self.keyword+summary_backward[i]
                            a = str_all.find(str_small)
                            b = str_small.find(pro)
                            summary_forward[i] = str_all[0:a+b]
                            summary_backward[i] = str_all[a+b+len(pro):-1]
                            #print(summary_forward[i],mid_word_list[i],summary_backward[i])

        return summary_forward,summary_backward,mid_word_list
    def call_ckip(self,summary_forward,summary_backward):#呼叫CKIP.exe
        if not(os.path.isdir('../sinica-ckip/CKIPWS/input/')):
            os.mkdir('../sinica-ckip/CKIPWS/input/')
        if not(os.path.isdir('../sinica-ckip/CKIPWS/input/'+self.timefolder+'/')):
            os.mkdir('../sinica-ckip/CKIPWS/input/'+self.timefolder+'/')
        if not(os.path.isdir('../sinica-ckip/CKIPWS/output/')):
            os.mkdir('../sinica-ckip/CKIPWS/output/')  
        if not(os.path.isdir('../sinica-ckip/CKIPWS/output/'+self.timefolder+'/')):
            os.mkdir('../sinica-ckip/CKIPWS/output/'+self.timefolder+'/')
        

        width = 100
        count = 0
        for i in range(0,len(summary_forward),width):
    
            if i+width > len(summary_forward):
                width = len(summary_forward)%width
            with open('../sinica-ckip/CKIPWS/input/'+self.timefolder+'/'+str(count)+'.txt','w',encoding = 'utf-16le') as f:
                f.write('\ufeff')#utf-16帶簽名需要加的字元
                for j in range(i,i+width):
                    f.write(summary_forward[j]+' forback '+summary_backward[j]+' cuthere ')
            count+=1
        #print('done!')
        #print('Start tagging')

        ###要有CKIPWS，output為詞性標記輸出結果
        os.system('cd ../sinica-ckip/CKIPWS&CKIPWSTesterDir ws.ini input/'+self.timefolder+' output/'+self.timefolder)

    def str2tuple(self,tag):#將string轉換成我們需要的tuple格式 (詞，詞性)
        a = tag.rfind('(')
        b = tag.rfind(')')
        return  (tag[0:a],tag[a+1:b])

    def arrange_tag(self):#讀取結果並將格式轉換成 [(詞，詞性),(詞，詞性)...]
        output_lst = os.listdir('../sinica-ckip/CKIPWS/output/'+self.timefolder+'/')
        term = []
        
        for output_file in output_lst:
    
            f = open('../sinica-ckip/CKIPWS/output/'+self.timefolder+'/'+output_file,'r',encoding='utf-16le')
            tag_string = f.read()
            f.close()
            tag_lst = tag_string.replace('\n','').split('\u3000')
            tag_tuple_lst = []
            for tag in tag_lst:
                if '(' not in tag:
                    continue
                else:
                    tag_tuple_lst.append(self.str2tuple(tag))

            term_forward = []
            term_backward = []
            for_back = 0
            for tag_tuple in tag_tuple_lst:
                if 'forback' == tag_tuple[0]:
                    for_back = 1
                elif 'cuthere' == tag_tuple[0]: 
                    if term_forward == []:
                        term_forward.append(('N/A','N/A'))
                    elif term_backward == []:
                        term_backward.append(('N/A','N/A'))
                    term.append([term_forward,term_backward])
                    term_forward = []
                    term_backward = []
                    for_back = 0
                elif for_back == 0:
                    term_forward.append(tag_tuple)
                elif for_back == 1:
                    term_backward.append(tag_tuple)
        return term

    def pick_words(self):
        content_lst = self.load_content()
        summary_forward,summary_backward = self.pick_for_back_20(content_lst)
        summary_forward,summary_backward,mid_word_list = self.pick_proper(summary_forward,summary_backward)
        self.call_ckip(summary_forward,summary_backward)
        term = self.arrange_tag()
        return term,mid_word_list

class Merge_word:
    """docstring for """
    def __init__(self, Threshold,keyword):
        self.Threshold = Threshold
        self.keyword = keyword
        
    def merge_proper(self,term,mid_word_list):#將符合詞性規則的詞合併
        ###Na/Nb/Nc/FW + Na/Nb/Nc/FW = 新專有名詞 ，Na/Nb/Nc/FW + 新專有名詞 = 新專有名詞###
        proper_noun_lst = []
        Special_symbol = [';','/','?',':','@','&','=','+','-','.','_','\"','※','●','├','┤','|',']','*','\'','◢','▆','▅','▄','▃','']
        number = 0
        proper_noun_Frequency = []
        for re_lst in term:
            text_forward = len(re_lst[0])-1
            text_backward = 0
            proper_noun = mid_word_list[number]
            number+=1
            forward_stop = 0
            backword_stop = 0
            
            while True:
        
                if forward_stop==0 and (re_lst[0][text_forward][1]=='Na' or re_lst[0][text_forward][1]=='Nb' or re_lst[0][text_forward][1]=='Nc' or re_lst[0][text_forward][1]=='FW'):
                    for symbol in Special_symbol:
                        if symbol in re_lst[0][text_forward][0]:
                            forward_stop = 1
                    if forward_stop==0:
                        if len(re_lst[0][text_forward][0])>1:
                            proper_noun = re_lst[0][text_forward][0]+proper_noun
                        else:
                            forward_stop = 1
                    if text_forward>0:
                        text_forward=text_forward-1
                    else:
                        forward_stop = 1
                elif forward_stop == 0:
                    forward_stop = 1
                if backword_stop==0 and (re_lst[1][text_backward][1]=='Na' or re_lst[1][text_backward][1]=='Nb' or re_lst[1][text_backward][1]=='Nc' or re_lst[1][text_backward][1]=='FW'):
                    for symbol in Special_symbol:
                        if symbol in re_lst[1][text_backward][0]:
                            backword_stop = 1
                    if backword_stop == 0:
                        if len(re_lst[1][text_backward][0])>1:
                            proper_noun = proper_noun+re_lst[1][text_backward][0]
                    if text_backward<len(re_lst[1])-1:
                        text_backward=text_backward+1
                    else:
                        backword_stop = 1
                elif backword_stop == 0:
                    backword_stop=1
                if forward_stop and backword_stop:
                    if proper_noun in proper_noun_lst:
                        index = proper_noun_lst.index(proper_noun)
                        proper_noun_Frequency[index] = proper_noun_Frequency[index]+1 
                    if (proper_noun not in proper_noun_lst) and len(proper_noun)>len(self.keyword):
                        proper_noun_lst.append(proper_noun)
                        proper_noun_Frequency.append(1)
                    break

        return proper_noun_lst,proper_noun_Frequency
    def lcs(self,str1,str2):##計算詞1與詞2相同的字數
        count = 0
        for i in str1:
            if i in str2:
                count+=1
        return count

    def similarity(self,str1,str2,q):#計算相似度
        return (self.lcs(str1,str2)-len(q))/(((len(str1)-len(q))*(len(str2)-len(q)))**0.5)

    def caculate_similarity(self,proper_noun_lst):
        ###列出 len(proper_noun_lst)*len(proper_noun_lst) 的矩陣###
        matrix = [[None] * len(proper_noun_lst) for i in range(len(proper_noun_lst))]
        i_index = 0
        for i_str in proper_noun_lst:
            j_index = 0
            for j_str in proper_noun_lst:
                if i_str==j_str:
                    matrix[i_index][j_index] = 1
                    break
                else:
                    matrix[i_index][j_index] = self.similarity(i_str,j_str,self.keyword)
                j_index+=1
            i_index+=1
        return matrix
    def group_proper_word(self,Threshold,proper_noun_lst,proper_noun_Frequency,matrix):
        ##將符合threshold的專有名詞合併在同一list##
        proper_noun_lst2 = []
        category = 0
        proper_noun_lst2.append([])
        proper_noun_Frequency2 = []
        proper_noun_Frequency2.append([])

        for Pnoun in range(len(proper_noun_lst)):
            not_in_list = 1
            category_pause = 0
            go_next_Pnoun = 0
            for proper_noun_small_lst in proper_noun_lst2:
                for word in proper_noun_small_lst:
                    if proper_noun_lst[Pnoun] == word:
                        go_next_Pnoun = 1
            if go_next_Pnoun:
                continue
            for i in range(Pnoun,len(proper_noun_lst)):
                dont_input = 0
                if matrix[i][Pnoun]>Threshold :
                    not_in_list = 0
                    #print(matrix[i][Pnoun],proper_noun_lst[Pnoun],proper_noun_lst[i])
                    for proper_noun_small_lst in proper_noun_lst2:
                        for word in proper_noun_small_lst:
                            if proper_noun_lst[i] == word:
                                dont_input = 1
                    
                    if dont_input==0:
                        category_pause = 1
                        proper_noun_lst2[category].append(proper_noun_lst[i])
                        proper_noun_Frequency2[category].append(proper_noun_Frequency[i])
            if category_pause:
                category+=1
                proper_noun_lst2.append([])
                proper_noun_Frequency2.append([])
        return  proper_noun_lst2,proper_noun_Frequency2

    def cluster_name(self,lst):##決定群集名稱
        max_name = ''
        max_word = 0
        word_count = []
        if len(lst)==1:
            return lst[0]
        for word in lst:
            word_name = []
            for w in word:
                if w not in word_name:
                    word_name.append(w)
            if len(word_name)>max_word:
                max_name = word
                max_word = len(word) 
    
        for n_word in max_name:
            count=0
        
            for name in lst:
                if n_word in name:
                    count+=1
            word_count.append(count)
    
        final_name = ''
        for i in range(len(word_count)):
            if word_count[i]/len(lst) > 0.5:
                #if max_name[i] not in final_name:
                final_name = final_name+max_name[i]
        return final_name
    def chose_cluster_name(self,proper_noun_lst):##記錄所有群集名稱
        clu_all = []
        for i in range(len(proper_noun_lst)):
            clu_all.append(self.cluster_name(proper_noun_lst[i]))
        return clu_all
    def get_output(self,term,mid_word_list):##main
        proper_noun_lst,proper_noun_Frequency = self.merge_proper(term,mid_word_list)
        matrix = self.caculate_similarity(proper_noun_lst)
        proper_noun_lst,proper_noun_Frequency = self.group_proper_word(self.Threshold,proper_noun_lst,proper_noun_Frequency,matrix)
        clu_all = self.chose_cluster_name(proper_noun_lst)
        return clu_all,proper_noun_lst,proper_noun_Frequency


   
