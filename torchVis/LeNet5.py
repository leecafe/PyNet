import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import os
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")   #若检测到GPU环境则使用GPU，否则使用CPU

if not os.path.exists('E:\\models\\'):#保存模型文件
    os.mkdir('E:\\models\\')
 
class LeNet5(nn.Module): #定义网络
    def __init__(self):
        super(LeNet5,self).__init__()
        #输入:(6*28*28);输出：(6*14*14)
        self.conv1 = nn.Sequential(     
            nn.Conv2d(in_channels=1,out_channels=6,kernel_size=5,stride=1,padding=2), #新建卷积层,kernel_size表示卷积核大小,stride表示步长,padding=2，图片大小变为 28+2*2 = 32 (两边各加2列0)，保证输入输出尺寸相同
            nn.ReLU(),
            #可以选择取最大值池化MaxPool2d,也可以选择取平均值池化AvgPool2d,两者参数相同
            nn.MaxPool2d(kernel_size = 2,stride = 2,padding=0)   #input_size=(6*28*28)，output_size=(6*14*14)
        )
        #输入:(6*14*14);输出：(16*5*5)
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=6,out_channels=16,kernel_size=5,stride=1,padding=0), #input_size=(6*14*14)，output_size=16*10*10
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2,stride = 2,padding=0)    ##input_size=(16*10*10)，output_size=(16*5*5)
        )
        #全连接层
        self.fc1 = nn.Sequential(
            nn.Linear(16*5*5,120),
            nn.ReLU()
        )
        #全连接层
        self.fc2 = nn.Sequential(
            nn.Linear(120,84),
            nn.ReLU()
        )
        #全连接层
        self.fc3 = nn.Linear(84,10)
 
    #网络前向传播过程
    def forward(self,x):
        x = self.conv1(x)
        x = self.conv2(x)
 
        x = x.view(x.size(0), -1) #全连接层均使用的nn.Linear()线性结构，输入输出维度均为一维，故需要把数据flatten成一维
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x

#查看网络
myNet = LeNet5()
print(myNet) 
 
#load data
transform = torchvision.transforms.ToTensor()   #定义数据预处理方式：转换 PIL.Image 成 torch.FloatTensor
 
train_data = torchvision.datasets.MNIST(root="G:\\python_mnist\mnist\\train",    #数据目录，这里目录结构要注意。
                                        train=True,                                     #是否为训练集
                                        transform=transform,                            #加载数据预处理
                                        download=False)                                 #是否下载
test_data = torchvision.datasets.MNIST(root="G:\\python_mnist\mnist\\train",
                                        train=False,
                                        transform=transform,
                                        download=False)
#数据加载器:组合数据集和采样器；batch_size=64:同时并行处理64张图片 
train_loader = torch.utils.data.DataLoader(dataset = train_data,batch_size = 64,shuffle = True) 
test_loader = torch.utils.data.DataLoader(dataset = test_data,batch_size = 64,shuffle = False)

#展示数据/图像
import numpy as np
import matplotlib.pyplot as plt
def imshow(img):
     img = img / 2 + 0.5 # unnormalize
     npimg = img.numpy()
     plt.imshow(np.transpose(npimg, (1, 2, 0)))
     plt.show()
# torchvision.utils.make_grid 将图片进行拼接
imshow(torchvision.utils.make_grid(iter(train_loader).next()[0]))


#define loss
net = LeNet5().to(device)    #实例化网络，有GPU则将网络放入GPU加速
loss_fuc = nn.CrossEntropyLoss()    #多分类问题，选择交叉熵损失函数
optimizer = optim.SGD(net.parameters(),lr = 0.001,momentum = 0.9)   #选择SGD，学习率取0.001
 
#开始训练
EPOCH = 8   #迭代次数
loss_list = []#

for epoch in range(EPOCH):
    sum_loss = 0
    #数据读取
    for i,data in enumerate(train_loader):
        inputs,labels = data
        inputs, labels = inputs.to(device), labels.to(device)   #有GPU则将数据置入GPU加速
 
        # 梯度清零
        optimizer.zero_grad()
 
        # 传递损失 + 更新参数
        output = net(inputs)
        loss = loss_fuc(output,labels)
        loss.backward()
        optimizer.step()


        # 每训练100个batch打印一次平均loss
        sum_loss += loss.item()
        if i % 100 == 99:
            print('[Epoch:%d, batch:%d] train loss: %.03f' % (epoch + 1, i + 1, sum_loss / 100))
            loss_list.append(sum_loss/100)
            sum_loss = 0.0
            


    correct = 0 # 预测正确数
    total = 0   #总图片数
 
    for data in test_loader:
        test_inputs, labels = data
        test_inputs, labels = test_inputs.to(device), labels.to(device)
        outputs_test = net(test_inputs)
        _, predicted = torch.max(outputs_test.data, 1)  #输出得分最高的类
        total += labels.size(0) #统计50个batch 图片的总个数
        correct += (predicted == labels).sum()  #统计50个batch 正确分类的个数
 
    print('第{}个epoch的识别准确率为：{}%'.format (epoch + 1, 100*correct.item()/total))

#模型保存
torch.save(net.state_dict(),'E:\\models\\ckpt.mdl') 

#模型加载
#net.load_state_dict(torch.load('ckpt.mdl'))

# 打印损失值变化曲线
import matplotlib.pyplot as plt
plt.plot(loss_list)
plt.title('traning loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.show()
