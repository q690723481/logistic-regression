# -*- coding: UTF-8 -*-  
#4567654
import numpy as np     
import pandas as pd
from sklearn.linear_model import SGDClassifier
from matplotlib import pyplot as plt

#��ȡ����(�����б�׼������)
def dataloading1():
    #��ȡ����ļ��ĵ�1�е���57�У��ӵ�0�е�0�п�ʼ����0�е���3999��
    data = pd.read_csv("D:/AI/income.csv",usecols=range(1,58),header=None)#�ļ���income.csv��������D�̵�AI�ļ��¡�
    print(data.head(5)) #�鿴��ȡ���ݵ�ǰ����
    data =  np.array(data)
    #��ȡ����ļ��ĵ�58�У�Ҳ�������ݵı�ǩ��0/1
    label = np.array(pd.read_csv("D:/AI/income.csv",usecols=[58],header=None))
    traindata = data[:3000]#ȡǰ3000�У��ӵ�0�е���2999����Ϊѵ�����ݣ�
    trainlabel = label[:3000]#ȡǰ3000�еı�ǩ
    testdata = data[3000:]#ȡ��1000����Ϊ��������
    testlabel = label[3000:]#ȡ��1000�еı�ǩ
    return traindata,testdata,trainlabel,testlabel

#��ȡ���ݣ����������ݵ�������н��б�׼������������������ֱ�Ӷ�ȡ��
def dataloading2():
    label = np.array(pd.read_csv("D:/AI/income.csv",usecols=[58],header=None))
    trainlabel = label[:3000]#ȡǰ3000�еı�ǩ
    testlabel = label[3000:]#ȡ��1000�еı�ǩ
    #��ȡ����ļ��ĵ�1�е���55�У��ӵ�0�е�0�п�ʼ��,Ҳ������ֵ�������0-1֮���
    data = np.array(pd.read_csv("D:/AI/income.csv",usecols=range(1,55),header=None))
    #��ȡ������ֻ��ȡֵ��1��ģ����ʹ���0-1֮������ݲ����б�׼������
    data2 = np.array(pd.read_csv("D:/AI/income.csv",usecols=range(55,58),header=None))

    #��ֵ�ͷ��ֻ���ѵ�����ݡ�����д�ľ�ֵ�뷽�����������ε�ģ��
    average = np.sum(data2[:3000],axis=0)/3000 #���ֵ
    averages = np.tile(average,(3000,1))
    variance = ( np.sum ( ( averages-data2[:3000] )**2,axis=0 ) /3000 )**0.5 #�󷽲������
    averages = np.tile(average,(4000,1))

    #���۲������ݻ���ѵ�����ݶ���Ҫ����ֵ��׼��
    data2 -= averages
    data3 = []
    for i in range(len(variance)):
        if variance[i] == 0:#�жϷ����Ƿ�Ϊ0������ǣ�������������1�����򰴱�׼����ʽx=(x-average)/variance
            data3.append(np.ones(4000))
        else:
            data3.append(data2[:,i]/variance[i])
        data = np.column_stack((data,data3[i])) #����һ������
    
    traindata = data[:3000]#ȡǰ3000�У��ӵ�0�е���2999����Ϊѵ�����ݣ�
    testdata = data[3000:]#ȡ��1000����Ϊ��������
    return traindata,testdata,trainlabel,testlabel

"""
����������
    predicterror:ͨ��sdg��predict_proba������á�
                 ��m��2�ľ���ÿ�е�һ�����������ݵı�ǩΪ0�ĸ��ʣ��ڶ��������Ǳ�ǩΪ1�ĸ��ʣ�������m�����ݸ�����
    testlabel:m��1�ľ���ÿ�д���һ�����ݵ�ʵ�ʱ�ǩ��
��������ֵ��
    loss:��ʧ������ֵ
"""
def loss(predicterror,testlabel):
    m,n = np.shape(testlabel) #m��ʾ���ݸ���
    loss = 0.0
    # ������ʱ�0.00000001(���ֵֻ���������һ������)С����ʱ��ȡ�����Ľ��Ϊ-inf,������󣬺���ļ����޷�����
    # �����ָ��ʣ�������������ʸ�ֵΪ0.00000001������㷨������ȷ�����ֵ��ֵΪ���ٶ���ʧ����Ӱ�첻��
    # ����㷨�������0.00000001ȡ���������-18���ң�Ҳ�Ƚϴ󣬿���������ʧ�������㡣
    for i in range(m):
        if predicterror[i][0] < 1e-8:
            log0 = np.log(1e-8)
        else: 
            log0 = np.log(predicterror[i][0])
        if predicterror[i][1] < 1e-8:
            log1 = np.log(1e-8)
        else:
            log1 = np.log(predicterror[i][1])
        loss += (1-testlabel[i])*log0 + testlabel[i]*log1
    loss = (-1)*loss/m
    return loss

"""#��ͬѧϰ��ʱ��ȷ�ʺ���ʧ��������������ı仯���
����������
    traindata��ѵ�����ݵ��������ݼ���3000��57�ľ���ÿ�д���һ��������������
    trainlabel��ѵ�����ݵ�ʵ�ʱ�ǩ��3000��1�ľ���ÿ�д���һ�����ݵı�ǩ
    testdata���������ݵ��������ݼ���1000��57�ľ���ÿ�д���һ��������������
    testlabel���������ݵ�ʵ�ʱ�ǩ��1000��1�ľ���ÿ�д���һ�����ݵı�ǩ
    eta��ѧϰ��
��������ֵ��
    iter1��[300,600,1000,1400,1700,2000,2500,3000,3400,3800,4200,4600,5000,5500,6000]
    testloss��15�β�ͬ���������µ���ʧ����ֵ
    rightrate��15�β�ͬ���������µĲ������ݵ���ȷ��
"""
def rightrate_loss(traindata,trainlabel,testdata,testlabel,eta=1e-1):
    rightrate=[]
    testloss=[]
    m,n = np.shape(testdata)
    iter1 = [300,600,1000,1400,1700,2000,2500,3000,3400,3800,4200,4600,5000,5500,6000]
#eta=[1e-1,1e-2,1e-3,1e-4,1e-5]
    for j in range(15):
        # SGDC������ݶ��½�����lossѡ��log����ʾ�߼��ع�ģ�ͣ�
	    # max_iter��������������eta0��ѧϰ�ʣ�Ҳ����ÿ�����ݶȸ��µĳ̶�
        sgdc=SGDClassifier(loss='log',max_iter=iter1[j],eta0=eta)
        sgdc.fit(traindata, np.ravel(trainlabel))#�����
        rightrate.append(1-sum((sgdc.predict(testdata)-np.ravel(testlabel))**2)/m)#����ȷ��
        predicterror = sgdc.predict_proba(testdata)#�����
        loss1 = np.array(loss(predicterror,testlabel))
        testloss.append(loss1)#����ʧ����
    return iter1,testloss,rightrate

#ͼ����ʾ
def display(_ter,rightrate1,rightrate2,rightrate3,rightrate4,rightrate5,testloss1,testloss2,testloss3,testloss4,testloss5):
    plt.figure()
    ax1 = plt.subplot(2,1,1) #��һ�е�һ��,��ʾ��ͬѧϰ���������ȷ������������仯�����
    ax2 = plt.subplot(2,1,2) #�ڶ��е�һ�У���ʾ��ͬѧϰ������²���������ʧ��������������ı仯���
    plt.sca(ax1)
    plt.plot(_iter,rightrate1,color='skyblue',label='eta0=0.1')
    plt.plot(_iter,rightrate2,color='red',label='eta0=0.01')
    plt.plot(_iter,rightrate3,color='blue',label='eta0=0.001')
    plt.plot(_iter,rightrate4,color='green',label='eta0=0.0001')
    plt.plot(_iter,rightrate5,color='yellow',label='eta0=0.00001')
    plt.ylabel('rightrate')
    plt.legend()
    plt.sca(ax2)
    plt.plot(_iter,testloss1, color='skyblue', label='eta0=0.1')
    plt.plot(_iter,testloss2, color='red', label='eta0=0.01')
    plt.plot(_iter,testloss3, color='blue', label='eta0=0.001')
    plt.plot(_iter,testloss4, color='green', label='eta0=0.0001')
    plt.plot(_iter,testloss5, color='yellow', label='eta0=0.00001')
    plt.xlabel('max_iter')
    plt.ylabel('testdata_loss')
    plt.legend()
    plt.show()

#������
#1.���ݶ�ȡ(�����б�׼������)
traindata,testdata,trainlabel,testlabel = dataloading1()

#2.�о�ѧϰ�ʺ͵�������������ݶ��½��㷨��ȷ�ʺͲ�������
_iter,testloss1,rightrate1 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-1)
_iter,testloss2,rightrate2 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-2)
_iter,testloss3,rightrate3 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-3)
_iter,testloss4,rightrate4 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-4)
_iter,testloss5,rightrate5 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-5)
display(_iter,rightrate1,rightrate2,rightrate3,rightrate4,rightrate5,testloss1,testloss2,testloss3,testloss4,testloss5)

#3.���������ȷ�ʣ����ݱ�׼��
# ��ʵҲ��֪������ô��ߣ��������ҵ�����Ҳ��˵�߼��ع鱾����ȷ�ʾͲ���̫�ߣ�
# Ȼ���뵽��knn�㷨����һ�����ص��ֵ�����۲���ε���������ݣ����������ݷ�Χ����0-1�����Կ��ǽ����Ǳ�׼����0-1��������
# ���õķ�����z-score��Ҳ�������ֵ�ͷ��Ȼ����������Ա任��0-1
traindata,testdata,trainlabel,testlabel = dataloading2()

# 4.���Ա�׼�������ݵ���ȷ��
_iter,testloss1,rightrate1 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-1)
_iter,testloss2,rightrate2 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-2)
_iter,testloss3,rightrate3 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-3)
_iter,testloss4,rightrate4 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-4)
_iter,testloss5,rightrate5 = rightrate_loss( traindata, trainlabel, testdata, testlabel,eta=1e-5)
display(_iter,rightrate1,rightrate2,rightrate3,rightrate4,rightrate5,testloss1,testloss2,testloss3,testloss4,testloss5)

#5.��ͬ���򻯲���ʱ��ȷ�ʺͲ�������/ѵ������(��׼��������)����ʧ�����ڽ�Ϊ����������ѧϰ��Ϊ0.001������������Ϊ1700���ı仯���
rightrate = []
testloss = []
trainloss = []
alpha1 = [0.5,0.1,0.09,0.06,0.01,0.0009,0.0006,0.0003,0.0001,0.00009,0.00005,0.00001]
massage = []
m,n = np.shape(testdata)
print("alpha rightrate testloss trainloss")
for j in range(12):
    # SGDC������ݶ��½�����lossѡ��log����ʾ�߼��ع�ģ�ͣ�
	# max_iter��������������eta0��ѧϰ�ʣ�Ҳ����ÿ�����ݶȸ��µĳ̶�
    sgdc=SGDClassifier(loss='log',alpha=alpha1[j],max_iter=1500,eta0=0.001)
    sgdc.fit(traindata, np.ravel(trainlabel))#�����
    right = 1-sum((sgdc.predict(testdata)-np.ravel(testlabel))**2)/m #����ȷ��
    rightrate.append(right)
    predicterror = sgdc.predict_proba(testdata)#���ǩ�ĸ���
    loss1 = loss(predicterror,testlabel)#�������ݵ���ʧ����
    loss2 = loss(sgdc.predict_proba(traindata),trainlabel)#ѵ�����ݵ���ʧ����
    testloss.append(loss1)
    trainloss.append(loss2)
    print([alpha1[j],right,loss1,loss2])
plt.figure()
ax1 = plt.subplot(2,1,1) #��һ�е�һ��,��ʾ��ȷ�������򻯲����仯�仯�ı仯���
ax2 = plt.subplot(2,1,2) #�ڶ��е�һ�У���ʾ��������/ѵ��������ʧ���������򻯲����ı仯���
plt.sca(ax1)
plt.plot(alpha1,rightrate,color='skyblue',label="test_rightrate")
plt.ylabel('rightrate')
plt.xlim(0, 0.5)
plt.legend()
plt.sca(ax2)
plt.plot(alpha1,testloss, color='skyblue', label='testloss')
plt.plot(alpha1,trainloss, color='red', label='trainloss')
plt.xlabel('alpha')
plt.ylabel('loss')
plt.xlim(0, 0.5)
plt.legend()
plt.show()



















    
