# 数据处理
import os,time
import torch
from torch.utils import data
from PIL import Image
import numpy as np
from torchvision import transforms
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

EPOCH = 20
BATCH_SIZE = 100
LR = 0.001

transform = transforms.Compose([
    transforms.ToTensor(),  # 将图片转换为Tensor,归一化至[0,1]
    # transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5])  # 标准化至[-1,1]
])

#定义自己的数据集合
class FlameSet(data.Dataset):
    def __init__(self, root, augment=None):
        # 所有图片的绝对路径
        self.image_files = np.array([x.path for x in os.scandir(root) if x.name.endswith(".jpg") or x.name.endswith(".png") or x.name.endswith(".JPG")])
        self.transforms=augment
        self.target = self.__get_target(self.image_files)

    def __getitem__(self, index):
        if self.transforms:
            image = Image.open(self.image_files[index])
            image = image.convert("L")
            image = self.transforms(image)  # 这里对图像进行了增强
            target = self.__code_convert_array(self.target[index])
            # target = self.transforms(target)
            return image, torch.Tensor(target) # 将读取到的图像变成tensor再传出
        else:
            # 如果不进行增强，直接读取图像数据并返回
            # 这里的open_image是读取图像函数，可以用PIL、opencv等库进行读取
            return Image.open(self.image_files[index])

    def __len__(self):
        return len(self.image_files)
    
    def __get_target(self, file_path_array):
        return np.array([os.path.basename(path).split(".")[0].lower() for path in file_path_array])
    
    def __code_convert_array(self, code):
        target = []
        allCode = "0123456789abcdefghijklmnopqrstuvwsyz"
        for char in code:
            vec = [0] * 36
            vec[allCode.find(char)] = 1
            target += vec
        return target
    
dataSet=FlameSet('./VerifyCode/train_data/', transform)
# print(dataSet[0],len(dataSet))
train_loader = data.DataLoader(
    dataset=dataSet,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=4
)

test_data = FlameSet("./VerifyCode/test_data/", transform)
test_loader = data.DataLoader(dataset=test_data,batch_size=BATCH_SIZE,shuffle=True)


class CNN(torch.nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(  #  batch * 100 * 50
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),
            torch.nn.BatchNorm2d(16),
            torch.nn.ReLU(), # batch * 16 * 100 * 50
            torch.nn.MaxPool2d(
                kernel_size=2,
            )   #  batch * 16 * 50 * 25
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 128, 5, 1, 2),  # batch * 128 * 50 * 25
            torch.nn.BatchNorm2d(128),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)    # batch * 128 * 25 * 12
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(128, 512, 5, 1, 2),  # batch * 128 * 25 * 12
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)  # batch * 512 * 12 * 6
        )
        self.out = torch.nn.Linear(512 * 12 * 6, 36*4)
    
    def forward(self, x):
        # print(x.size())
        x = self.conv1(x)
        # print(x.size())
        x = self.conv2(x)
        # print(x.size())
        x = self.conv3(x)
        # print(x.size())
        x = x.view(x.size(0), -1)
        # print(x.size())
        output = self.out(x)
        # print(output.size())
        # exit(0)
        return output

def claculat_acc(predict, real):
    predict, real = predict.view(-1,36), real.view(-1,36)
    predict = torch.nn.functional.softmax(predict, dim=1)
    predict = torch.argmax(predict, dim=1)
    real = torch.argmax(real, dim=1)
    predict, real = predict.view(-1,4), real.view(-1, 4)
    correct_list = []
    for i , j in zip(predict, real):
        if torch.equal(i,j):
            correct_list.append(1)
        else:
            correct_list.append(0)
    acc = sum(correct_list)/len(correct_list)
    return acc


def run_CNN():
    cnn = CNN()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
    loss_func = torch.nn.MultiLabelSoftMarginLoss()
    
    _start = time.time()
    loss_history = []
    acc_history = []
    for epoch in range(EPOCH):
        cnn.train()
        for step, (x_batch, y_batch) in enumerate(train_loader):
        
            # print(x_batch.size())
            output = cnn(x_batch)
            loss = loss_func(output, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print("epoch: %d | step: %d | loss: %.4f"%(epoch, step, loss.item()))

        
        cnn.eval()
        step_acc = []
        for img, target in test_loader:
            output = cnn(img)
            
            acc = claculat_acc(output, target)
            step_acc.append(acc)
            
        
        mean_acc = sum(step_acc)/len(step_acc)
        loss_history.append(loss.item())
        acc_history.append(mean_acc)
        print("===> Epoch: %d | Time: %d s | Loss: %.4f | Accuray: %.2f"%(epoch, int(time.time()-_start), loss.item(), mean_acc))
    torch.save(cnn, "./VerifyCode/cnn.pkl")
    print(acc_history, loss_history)
    
    # plt.show()


if __name__ == "__main__":
    run_CNN()
    
    


    
    
    