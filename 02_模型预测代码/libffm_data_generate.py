import lightgbm as lgbm
#from lgbm.sklearn import LGBMClassifier
import xlearn as xl
import pandas as pd 
import numpy as np
import time

from pandas import DataFrame

def original_gbm_ffm_data(x,y,dict_gbm,data_gbm,save_name='D:/ffm_data.txt'):
#将lightgbm生成的数据转化为DataFrame格式,获取特征的数量
    df=DataFrame(x)
    df_gbm=DataFrame(data_gbm)
    df=pd.concat([df,df_gbm],axis=1)   
    
    
    tree_num=df.shape[1]
    label_dict={'C1': 4, 'C14': 373, 'C15': 3, 'C16': 4, 'C17': 238, 
            'C18': 4, 'C19': 43, 'C20': 76, 'C21': 41,  'app_category': 6, 
            'app_domain': 16, 'app_id': 145, 'banner_pos': 3, 'device_conn_type': 4, 'device_model': 141,
             'device_type': 4, 'site_category': 7, 'site_domain': 110, 'site_id': 129,'hour_hours':24,
            'hour_weekday':7}
    
    for key,value in dict_gbm.items():
        label_dict[key]=value
    
    
    
#生成每颗树中包含的特征的数量，用于生成数据表格
        
    #将标签click与特征数据合并在一起
    y=DataFrame(y)
    df['click']=y
    cols=df.columns
    
 #对于送入的单行特征返回一个list，其中包括  1，1，8，1
    def data_for_libffm(row,cols,label_dict):
        data_list=[]
        data_list.append(row['click'])
        i=0
        value_sum=0
        for col,value in label_dict.items():
            if col=='click':
                continue
            else:
                data_list.append(i+1)
                data_list.append(value_sum+row[col]+1)
                data_list.append(1)
            value_sum+=label_dict[col]
            i+=1
        return data_list   
    
    ffm_data_list= df.apply(lambda row: data_for_libffm(row,cols,label_dict), axis=1)
    
    
    with open(save_name,'w')as file:
        for datas in ffm_data_list:
            i=0
            for data in datas:
                if i==0:
                    file.write(str(data))
                    file.write(' ')
                else:
                    if i%3==1:
                        file.write(str(data))
                        file.write(':')
                    if i%3==2:
                        file.write(str(data))
                        file.write(':')
                    if i%3==0:
                        file.write(str(data))
                        file.write(' ')
                i+=1
            file.write('\n')

#original lib_ffm_data_generate
def original_ffm_data(x,y,save_name='D:/ffm_data.txt'):
#将lightgbm生成的数据转化为DataFrame格式,获取特征的数量
    df=DataFrame(x)
    
    tree_num=df.shape[1]
    label_dict={'C1': 4, 'C14': 373, 'C15': 3, 'C16': 4, 'C17': 238, 
            'C18': 4, 'C19': 43, 'C20': 76, 'C21': 41,  'app_category': 6, 
            'app_domain': 16, 'app_id': 145, 'banner_pos': 3, 'device_conn_type': 4, 'device_model': 141,
             'device_type': 4, 'site_category': 7, 'site_domain': 110, 'site_id': 129,'hour_hours':24,
            'hour_weekday':7,'hour_days':10}
#生成每颗树中包含的特征的数量，用于生成数据表格
        
    #将标签click与特征数据合并在一起
    y=DataFrame(y)
    df['click']=y
    cols=df.columns
    
 #对于送入的单行特征返回一个list，其中包括  1，1，8，1
    def data_for_libffm(row,cols,label_dict):
        data_list=[]
        data_list.append(row['click'])
        i=0
        value_sum=0
        for col,value in label_dict.items():
            if col=='click':
                continue
            else:
                data_list.append(i+1)
                data_list.append(value_sum+row[col]+1)
                data_list.append(1)
            value_sum+=label_dict[col]
            i+=1
        return data_list   
    
    ffm_data_list= df.apply(lambda row: data_for_libffm(row,cols,label_dict), axis=1)
    
    
    with open(save_name,'w')as file:
        for datas in ffm_data_list:
            i=0
            for data in datas:
                if i==0:
                    file.write(str(data))
                    file.write(' ')
                else:
                    if i%3==1:
                        file.write(str(data))
                        file.write(':')
                    if i%3==2:
                        file.write(str(data))
                        file.write(':')
                    if i%3==0:
                        file.write(str(data))
                        file.write(' ')
                i+=1
            file.write('\n')





#lightgbm-libffm_data_generate
def gbm_ffm_data(x,y,save_name=r'/usr/local/ffm_data.txt'):
#将lightgbm生成的数据转化为DataFrame格式
    df=DataFrame(x)
    tree_num=df.shape[1]
    
#生成每颗树中包含的特征的数量，用于生成数据表格
    feature_n=df.max()
    label_list={}
    i=0
    num=0
    for x in feature_n:
        label_list[i]=num
        i+=1
        num+=x+1
        
    #将标签click与特征数据合并在一起
    y=DataFrame(y)
    df['click']=y

    cols=df.columns
    
 #对于送入的单行特征返回一个list，其中包括  1，1:8:1
    def data_for_libffm(row,cols,label_list):
        data_list=[]
        data_list.append(row['click'])
        for col in label_list:
            if col=='click':
                continue
            else:
                data_list.append(col+1)
                data_list.append(label_list[col]+row[col]+1)
                data_list.append(1)
        return data_list   
    
    ffm_data_list= df.apply(lambda row: data_for_libffm(row,cols,label_list), axis=1)
    
    
    with open(save_name,'w')as file:
        for datas in ffm_data_list:
            i=0
            for data in datas:
                if i==0:
                    file.write(str(data))
                    file.write(' ')
                else:
                    if i%3==1:
                        file.write(str(data))
                        file.write(':')
                    if i%3==2:
                        file.write(str(data))
                        file.write(':')
                    if i%3==0:
                        file.write(str(data))
                        file.write(' ')
                i+=1
            file.write('\n')
