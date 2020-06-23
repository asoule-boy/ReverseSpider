import torch, os
from torchvision import transforms
from PIL import Image
torch.nn.Module.dump_patches = True

class CNN(torch.nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(  # batch * 100 * 50
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),
            torch.nn.BatchNorm2d(16),
            torch.nn.ReLU(),  # batch * 16 * 100 * 50
            torch.nn.MaxPool2d(
                kernel_size=2,
            )  # batch * 16 * 50 * 25
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 128, 5, 1, 2),  # batch * 128 * 50 * 25
            torch.nn.BatchNorm2d(128),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)  # batch * 128 * 25 * 12
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(128, 512, 5, 1, 2),  # batch * 128 * 25 * 12
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)  # batch * 512 * 12 * 6
        )
        self.out = torch.nn.Linear(512 * 12 * 6, 36 * 4)
    
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


def verifycode():
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    #构造字体对象
    font = ImageFont.truetype(r'C:\Windows\Fonts\bgothl.ttf', 40)
    #构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    # request.session['verify'] = rand_str
    #内存文件操作
    # import io
    # buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save("./VerifyCode/test/%s.png"%rand_str, 'png')
    return "./VerifyCode/test/%s.png"%rand_str
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    # return HttpResponse(buf.getvalue(), 'image/png')

def restore_cnn():
    cnn = torch.load("./VerifyCode/cnn.pkl")
    return cnn

def gen_data(path):
    transform = transforms.Compose([transforms.ToTensor()])
    
    img = Image.open(path)
    img = img.convert("L")
    img = transform(img)
    target = os.path.basename(path).split(".")[0]
    return img, target

def tensor_convert_target(predict):
    predict = predict.view(-1, 36)
    predict = torch.nn.functional.softmax(predict, dim=1)
    predict = torch.argmax(predict, dim=1)
    predict = predict.view(-1, 4)
    allChar = "0123456789abcdefghijklmnopqrstuvwsyz"
    string = ""
    for i in torch.squeeze(predict):
        char = allChar[i]
        string += char
    return string
    

if __name__ == '__main__':
    cnn = restore_cnn()
    acc = 0
    for i in range(100):
        code_path = verifycode()
        img, target = gen_data(code_path)
        predict = cnn(torch.unsqueeze(img, dim=1))
        prediction = tensor_convert_target(predict)
        print("真实值：%s | 预测值：%s"%(target, prediction))
        if target.lower() == prediction:
            acc += 1
    print("-------------经以上测试正确率：%d%%---------------"%acc)