import numpy as np
    
class LR(object):
    
    #决策函数为sigmoid函数
    @staticmethod
    def fn(w,x):
        return 1.0/(1.0 + np.exp(x.dot(-w)))
    
    #交叉熵损失函数
    @staticmethod
    def loss(y,y_hat):
        return np.sum(np.nan_to_num(-y * np.log(y_hat) - (1-y) * np.log(1-y_hat)))
    
    #交叉熵损失函数对权重w的一阶导数
    @staticmethod
    def grad(y,y_hat,x):
        return (y_hat - y) * x
    
    
    
class FTRL(object):
    
    def __init__(self, dim, l1, l2, alpha, beta, decisionFunc=LR):
        self.dim = dim                    #特征维度
        self.decisionFunc = decisionFunc  #决策函数
        self.z = np.zeros(dim)
        self.n = np.zeros(dim)            #累积梯度平方和
        self.w = np.zeros(dim)
        self.l1 = l1                     #L1正则参数
        self.l2 = l2                     #L2正则参数
        self.alpha = alpha               #学习率参数α
        self.beta = beta                 #学习率参数β
        
    def predict(self, x):
        return self.decisionFunc.fn(self.w, x)
    
    
    def update(self, x, y):
        #更新每个维度的w
        self.w = np.array([0 if np.abs(self.z[i]) <= self.l1 else (np.sign(
            self.z[i]) * self.l1 - self.z[i]) / (self.l2 + (self.beta + np.sqrt(self.n[i])) / self.alpha) for i in range(self.dim)])
        #求出sigmoid预测值y_hat(用于求梯度).
        y_hat = self.predict(x)  
        #损失函数梯度
        g = self.decisionFunc.grad(y, y_hat, x)  
        sigma = (np.sqrt(self.n + g * g) - np.sqrt(self.n)) / self.alpha
        self.z += g - sigma * self.w
        self.n += g * g
        return self.decisionFunc.loss(y, y_hat)
    

    def train(self, x_train, y_train, min_loss=0.01, epochs=10,early_stop = 10,print_loss = False):
        for n in range(epochs):
            itr = 0
            for i in range(x_train.shape[0]):
                x = x_train.iloc[i]
                y = y_train.iloc[i][0]
                loss = self.update(x, y)
                if i%500 == 0 and print_loss:
                    print ("epoch: "+str(n)+" i= " + str(i) + "\tloss=" + str(loss))
                if loss < min_loss:
                    itr += 1
                else:
                    itr = 0
                if itr >= early_stop:
                    print ("loss have less than", min_loss, "  for ", itr, "iterations,early stop!")
                    return loss
        return loss
            

