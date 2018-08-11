from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd 


#获取特征-域字典。格式：{feature_index1:field_index1,......}
def onehot_get_dict(train_x,test_x):
    #未onehot编码前，原特征数，即域的个数
    m = len(train_x.columns)
    
    #onehot
    x_all = np.concatenate([train_x, test_x])
    enc = OneHotEncoder(sparse = False)
    enc.fit(x_all)
    x_all = enc.transform(x_all)
    train_x = enc.transform(train_x)
    test_x = enc.transform(test_x)
    
    #one-hot后的特征数
    n = x_all.shape[1]
    del x_all
    
    #m_list为one-hot后，每个特征的取值数目(即每个原特征分解成多少个子特征)
    #格式为[n1,n2,n3....],size为m原始特征数。即第一个特征(域)one-hot编码后,有n1种不同取值.....
    m_list = list(enc.n_values_)
    
    dic = dict()
    h = 0
    #循环每个域
    for i in range(m):
        #循环每个域中的特征数,更新字典
        for j in range(m_list[0]):
            dic[h] = i
            h = h+1
        m_list.pop(0)
    
    #稀疏矩阵转换成dataFrame
    
    train_x = pd.DataFrame(train_x)
    test_x = pd.DataFrame(test_x)
    
    return train_x,test_x,n,m,dic