import numpy as np
import math
import random
from sklearn.metrics import log_loss

class FFMClassifier(object):
    
    def __init__(self,n,m,k,eta,lambd,feat_field_dic):
        # n个特征，
        # m个域，
        # 隐向量的维度k
        # 学习率η
        # 正则参数λ
        # feat_field_dic 为每个特征的域索引。格式：{feature_index1:field_index1,......}
        self.n = n
        self.m = m
        self.k = k
        self.eta = eta
        self.lambd = lambd
        self.dic = feat_field_dic
        # 初始化三维权重矩阵w，Xavier初始化w∼G(0,√1/k)
        self.w = np.random.rand(n,m,k)/math.sqrt(k)
#         self.w = np.random.rand(n,m,k)
        # self.G是每轮梯度平方和,用于AdaGrad梯度下降
        self.G = np.ones(shape=(n,m,k),dtype=np.float64)
        
    #用于计算FFM的模型表达式
    def phi(self,each_x):
        phi_result = 0 
        #归一化因子
        sum_v = sum(each_x.values)
        # 获取特征index
        key_index = each_x.keys()
        #循环一条数据的每个特征
        for i in range(len(key_index)):
            #feat_index1为特征索引，fild_index1为特征所属域的索引，value1为特征值
            feat_index1 = i
            fild_index1 = self.dic[feat_index1]
            value1 = each_x[feat_index1]/sum_v 
            #计算每个特征与其他特征的组合
            for j in range(i+1,len(key_index)):
                feat_index2 = j
                fild_index2 = self.dic[feat_index2]
                value2 = each_x[feat_index2]/sum_v 
                w1=self.w[feat_index1,fild_index2]
                w2=self.w[feat_index2,fild_index1]
                #模型公式:∑∑<Wi.fj,Wj.fi>XiXj
                phi_result += np.dot(w1, w2) * value1 * value2
        return phi_result
    
    #用于随机梯度下降优化更新参数
    def sgd_para(self,each_x,grad_phi):
        #grad_phi为目标函数对φ(x)的导数。grad_phi与w无关，故每条数据提前计算好
        sum_v = sum(each_x.values)
        key_index = each_x.keys()
        for i in range(len(key_index)):
            feat_index1 = i
            fild_index1 = self.dic[feat_index1]
            value1 = each_x[feat_index1]/sum_v
            for j in range(i+1,len(key_index)):
                feat_index2 = j
                fild_index2 = self.dic[feat_index2]
                value2 = each_x[feat_index2]/sum_v
                w1=self.w[feat_index1,fild_index2]
                w2=self.w[feat_index2,fild_index1]
                #目标函数对Wi,fj，Wj,fi的偏导
                g_i_fj = grad_phi*value1*value2*w2 + self.lambd*w1
                g_j_fi = grad_phi*value1*value2*w1 + self.lambd*w2
                #各个维度上的梯度累积平方和
                self.G[feat_index1, fild_index2] += g_i_fj ** 2
                self.G[feat_index2, fild_index1] += g_j_fi ** 2
                # AdaGrad，更新两个w
                self.w[feat_index1, fild_index2] -= g_i_fj*self.eta/np.sqrt(self.G[feat_index1, fild_index2])
                self.w[feat_index2, fild_index1] -= g_j_fi*self.eta/np.sqrt(self.G[feat_index2, fild_index1])
                
                
    def train(self,train_x,train_y,max_echo,min_loss):
        # train_x 训练集x
        # val_x 校验集x
        # train_y 训练集y
        # val_y 校验集y
        # max_echo 最大迭代次数
        # min_loss loss阈值
        for i in range(max_echo):
            n = 0  
            order = list(range(len(train_y)))
            #打乱顺序
            random.shuffle(order)
            #训练集训练
            for each_train_index in order:
                #根据index从训练集取出这条x
                train_each_x = train_x.iloc[each_train_index]
                #构造模型φ(x)表达式
                phi = self.phi(train_each_x)
                #此条数据对应的y值
                y_i = train_y.iloc[each_train_index][0]
                #目标函数对φ(x)的导数
                g_phi = -y_i/(1 + math.exp(y_i * phi))
                #梯度下降，更新参数
                self.sgd_para(train_each_x,g_phi)
                if n%500 == 0:
                    print("epoch: {},第: {} 条数据训练".format(i,n))
                n = n+1
            y_pred = self.predict(train_x)
            loss_train = log_loss(train_y,y_pred)
            print("epoch: {}, train_loss: {}".format(i,loss_train))
            if loss_train<= min_loss:
                print('损失已小于阈值！训练提前结束!')
                break
                
                
    def predict_proba(self,test_x):
        test_y =np.zeros((test_x.shape[0],2))
        for index,row in test_x.iterrows():
            phi_y = self.phi(row)
            proba = 1.0/(1.0 + math.exp(-phi_y))
            test_y[index,0] = 1 - proba
            test_y[index,1] = proba
            
        return test_y
    
    def predict(self,test_x):
        test_y =np.zeros(test_x.shape[0])
        for index,row in test_x.iterrows():
            phi_y = self.phi(row)
            test_y[index] = phi_y
            
        return test_y
        

    
    
    #训练好的权重矩阵保存           
    def save_model(self,file_name):
        np.save(file_name,self.w)
    
    
    #加载权重矩阵
    def load_model(self,file_name):
        w = np.load(file_name)
        self.w = w
        
        
        