#将字典存储磁盘
#将字典存储磁盘
def write_dict(name,one_dict):
    with open(name,'w')as file:
        for key,value in one_dict.items():
            file.write('|'+str(key))
            file.write('>'+str(value))


#读取时间特征的dict
def read_dict(name,key_int=True):
    with open(name,'r')as file:
        dict_hours_={}
        f=file.readlines()
        f=''.join(f)
        f=f.split('|')
        f.remove('')
        for line in f:
            feature=line.split('>')
            if key_int:
                dict_hours_[int(feature[0])]=int(feature[1])
            else: 
                dict_hours_[feature[0]]=int(feature[1])                
    
        return dict_hours_


#将双重字典存储磁盘
def write_double_dict(name,double_dict):
    with open(name,'w')as file:
        for k,v in double_dict.items():
            file.write('!')        
            file.write(k)
            for key,value in v.items():
                file.write('|'+str(key))
                file.write('>'+str(value))
                
#从磁盘中将双重字典读取成双重字典               
def read_double_dict(name,key_int=True):
    with open(name,'r')as file:
        f=file.readlines()
        f=''.join(f)

    f=f.split('!')
    f.remove('')
    dict_21={}
    for line in f:
        feature=line
        feature=feature.split('|')
        k_=feature[0]
        feature.remove(k_)
        dict_={}
        for word in feature:
            key_value=word.split('>')
            if key_int:
                dict_[int(key_value[0])]=int(key_value[1])
            else:
                dict_[key_value[0]]=int(key_value[1])
        dict_21[k_]=dict_
    
    return dict_21
#————————————————————————————————————————

#统计数据中所有特征中维度的名字
def count_name(data):
    dict_name_all={}
    for k,v in data.items():
        list_1=[]
        for key,value in v.items():
            list_1.append(value)
        dict_name_all[k]=set(list_1)
    return dict_name_all

#将两个value为set的字典合并起来
def combine_dict_list(dict1,dict2):
    dict3={}
    list_k=[]

    list_k=list(dict1.keys())
    
    for k in list_k:
        list_3=[]
        list_1=list(dict1[k])
        for x in list_1:
            list_3.append(x)
        list_2=list(dict2[k])
        for x in list_2:
            list_3.append(x)
        dict3[k]=set(list_3)
#提取dict2的取值       
    return dict3


#找到数据中前n%的数据
def count_head(dict1,name='0',other_rate=0.01):
    dict2={}
    list_=sorted(dict1.items(),key = lambda x:x[1],reverse = True)
    for x in list_:
        dict2[x[0]]=x[1]
    
    dict3={}
#    print(name,':',dict1['other']/40428968)
    threshold=40428968*(1-other_rate)
    num=0
    rate=0
    for key,value in dict2.items():
              
        if num<threshold:
            dict3[key]=round((value/40428968),5)
            rate+=dict3[key]
        else:
            dict3['other']=1-rate
        num+=value  
    print(len(dict3.values()))
    print(name,':',dict3['other'],'\n')

#    print(dict3)
    return dict3


#合并两个字典中value的分布。
def combine_dict(dict1,dict2):
    dict3={}
    list_k=[]

#    for key in dict1.keys():
#        list_k.append(str(key))
#    for key in dict2.keys():
#        list_k.append(key)
#    set_k=set(list_k)              #获取两个字典的key
    list_k=list(dict1.keys())
    
    for k in list_k:
        dict3[k]={}
        list_key=[]
        for key in dict1[k].keys():
            list_key.append(key)
        for key in dict2[k].keys():
            list_key.append(key)
        set_key=set(list_key)
        for key in set_key:
            if key in dict1[k].keys():
                value1=dict1[k][key]                
            else:
                value1=0
                
            if key in dict2[k].keys():
                value2=dict2[k][key]                
            else:
                value2=0
                
            dict3[k][key]=value1+value2
#提取dict2的取值       
    return dict3
#——————————————————————————————————————————————



def data_plt(data):
    data=data.fillna(-1)
    for col in data.columns:
        fig=plt.figure()
        sns.distplot(data[col].values,bins=30,kde=False)
        plt.xlabel(col,fontsize=24)
        plt.show()



#输入dict绘制相应的饼图                
def plt_pie(plt_data,name='pie',label_n=3):
    labels=[]
    sizes=[]
    colors=[]
    colors_all=['lightskyblue','orange','blue','green','lightcoral'\
                ,'green','lightcyan','purple','red','brown',\
                'gray','olive','cyan','gold','ivory',\
                 'lightpink','pink','lightsalmon','lightslategray','lightseagreen',\
                'lightskyblue','orange','blue','green','lightcoral'\
                ,'green','lightcyan','purple','red','brown',\
                'gray','olive','cyan','gold','ivory',\
                 'lightpink','pink','lightsalmon','lightslategray','lightseagreen',\
                'lightskyblue','orange','blue','green','lightcoral'\
                ,'green','lightcyan','purple','red','brown',\
                'gray','olive','cyan','gold','ivory',\
                 'lightpink','pink','lightsalmon','lightslategray','lightseagreen',\
                'lightskyblue','orange','blue','green','lightcoral'\
                ,'green','lightcyan','purple','red','brown',\
                'gray','olive','cyan','gold','ivory',\
                 'lightpink','pink','lightsalmon','lightslategray','lightseagreen',\
                'lightskyblue','orange','blue','green','lightcoral'\
                ,'green','lightcyan','purple','red','brown',\
                'gray','olive','cyan','gold','ivory',\
                 'lightpink','pink','lightsalmon','lightslategray','lightseagreen',\
                'lightskyblue','orange','blue','green','lightcoral'\
                ,'green','lightcyan','purple','red','brown',\
                'gray','olive','cyan','gold','ivory',\
                 'lightpink','pink','lightsalmon','lightslategray','lightseagreen',\
               'tomato']
    i=0
    plt_list=sorted(plt_data.items(),key = lambda x:x[1],reverse = True)
    
    for key,value in plt_list:
        if i<label_n or key=='other':
            labels.append(key)
            sizes.append(value)
            colors.append(colors_all[i])
        else:
            labels.append('')
            sizes.append(value)
            colors.append(colors_all[i])
        i+=1  
        
    plt.pie(sizes,labels=labels,
        colors=colors,autopct='%1.2f%%',shadow=True,startangle=50)
    plt.axis('equal')    
    plt.title(name)
    plt.show()
#___________________________________________________________________________________________                
                

#对输入list反馈1、类别的数目，各种元素所占比例，
class Edit_List(object):
    def __init__(self,data,head_num=20):
        self.data = list(data)
#list中，类别的比例
        self.class_n=0
#取特征中排名前几的数据
        self.head_num=head_num
#list中，各数据数量的dict
        self.class_num = {}
#list中，各数据数量所占比例   
        self.class_num_rate = {}
#list中，前1%各数据数量所占比例   
        self.class_num_head = {}
#list中，前1%各数据数量所占比例   
        self.class_num_rate_head = {}

        
#在init中初始化如下方法，可以直接以.class_num,.count_num_rate的方式调用数据
#        self.get_class_num()
#        self.get_class_num_rate()
    def get_class_set(self):
        set1=set(self.data)
        return set1

#获得列表中，类别的数量        
    def get_class_n(self):
        set0=set(self.data)
        self.class_n=len(set0)
        return self.class_n

#获得列表中，不同数据的数量
    def get_class_num(self):
        set0 = set(self.data)
        for x in set0:
            self.class_num.update({x: list(self.data).count(x)})
        return self.class_num
    
##获取列表中，元素占比超过前的数据量
    def get_class_num_head(self):
        set0 = set(self.data)
        n_all=0
        other=0
        count_num_all = (self.data).__len__()
#        print(len(set0))
        
        if count_num_all<self.head_num:
            self.head_num=count_num_all

#初始化前n个元素，并获取一个初步阈值
        threshold=count_num_all
#        threshold_index
        list_head_num=list(set0)[:self.head_num]
        for x in list_head_num:
            num=self.data.count(x)
            self.class_num_head[x]=num
            if num<threshold:
                threshold_index=x
                threshold=num 

        for x in set0:
            num=self.data.count(x)
            if num>threshold:
                if x in list(self.class_num_head.keys()):
                    continue
                else:
                    self.class_num_head[x]=num               
#删除此前阈值对应的元素确定新的阈值
                    self.class_num_head.pop(threshold_index)
                    threshold=count_num_all
                    for key,value in self.class_num_head.items():
                        if value<threshold:
                            threshold_index=key
                            threshold=value 
        
        for key,value in self.class_num_head.items():
            n_all+=value
        other=count_num_all-n_all
        self.class_num_head['other']=other
         
        return self.class_num_head
    
#获得列表中，不同数据占总数量的比例
    def get_class_num_rate(self):
        set0 = set(self.data)
        for x in set0:
            self.class_num.update({x: list(self.data).count(x)})

        count_num_all = list(self.data).__len__()
        for key, value in self.class_num.items():
            self.class_num_rate[key] = round(value/count_num_all, 4)
        return self.class_num_rate


##获取列表中，元素占比超过1%的数据
    def get_class_num_rate_head(self):
        set0 = set(self.data)
        rate_all=0.0000
        rate_other=0.0000
        count_num_all = (self.data).__len__()
#        print(len(set0))
        
        if count_num_all<self.head_num:
            self.head_num=count_num_all

#初始化前n个元素，并获取一个初步阈值
        threshold=1
#        threshold_index
        list_head_num=list(set0)[:self.head_num]
        for x in list_head_num:
            rate=self.data.count(x)/count_num_all
            self.class_num_rate_head[x]=rate
            if rate<threshold:
                threshold_index=x
                threshold=rate 

        for x in set0:
            rate=self.data.count(x)/count_num_all  
            if rate>threshold:
                if x in list(self.class_num_rate_head.keys()):
                    continue
                else:
                    self.class_num_rate_head[x]=rate               
#删除此前阈值对应的元素确定新的阈值
                    self.class_num_rate_head.pop(threshold_index)
                    threshold=1
                    for key,value in self.class_num_rate_head.items():
                        if value<threshold:
                            threshold_index=key
                            threshold=value 
        
        for key,value in self.class_num_rate_head.items():
            rate_all+=value
        print('***'+str(rate_all)+'\n'+'\n')
        rate_other=1.00-rate_all
        self.class_num_rate_head['other']=rate_other
        
        for key,value in self.class_num_rate_head.items():
            self.class_num_rate_head[key]=round(value,7)
        
        return self.class_num_rate_head
    

#当采用类调用方法时，有return或print都会触发此命令，故而一个类中仅有一个方法可以触发此命令
    def __repr__(self):
        return 'this is rate:%s' % str(self.class_num_rate)
    
############————————————————————————————————
#---------------------------------------------
def count_class_num(data,list_cols,list_drop=True,head_num_=100):  
    list_class_rate_21_s={}
    cols=list(data.columns)
#是指获取list_cols的元素，还是获取处list_cols外的元素
    if list_drop:
        for x in list_cols:
            cols.remove(x)
    else:
        cols=list_cols    
    
    for col in cols:
#            print(str(col)+'\n')
        start=time.time()
        edit=Edit_List(data[col],head_num=head_num_)
        list_class_rate_21_s[col]=edit.get_class_num_head()    #提取数据中的前n项分布
#            print(list_class_rate_21_s[col])
        end=time.time()
#            print(end-start)
#            print("\n")
        times=end-start
    return list_class_rate_21_s