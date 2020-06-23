from PIL import Image, ImageChops
import requests
import random, js2py
import time, re, json, gc
requests.packages.urllib3.disable_warnings()
success = 0

def reImg(path):  # js扣出来的图片还原过程
    img1 = Image.open(path)
    SEQUENCE = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17];
    img2 = Image.new(mode="RGB",size=(260,160))
    for _ in range(52):
        u = SEQUENCE[_] % 26 * 12 + 1
        c = 80 if 25 < SEQUENCE[_] else 0
        # print(u,c,10,80)
        tmp = img1.crop( box = (u, c, u + 10, c + 80) )
        img2.paste(tmp,(_ % 26 * 10, 80 if 25<_ else 0))

    return img2

def downloadImg(url,type):  # 下载滑块图片
    header = {
        "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url,headers=header,verify=False)
    path = type + "_download_old.jpg"
    with open(path,"wb") as fp:
        fp.write(response.content)
    return path

def getGtChallenge():  # 获取gt，challenge参数
    header = {
        "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Referer": "https://passport.bilibili.com/login",
    }
    response = requests.get("https://passport.bilibili.com/web/captcha/combine?plat=6",headers=header,verify=False)
    response.encoding="utf8"
    json = response.json()
    gt = json["data"]["result"]["gt"]
    challenge = json["data"]["result"]["challenge"]
    #print("gt = ",gt,"\nchallenge = ",challenge)
    return gt,challenge

def getImgUrlOnce(gt,challenge):
    url = "https://api.geetest.com/get.php"
    header = {
        "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Referer": "https://passport.bilibili.com/login",
        "Cookie": "GeeTestUser=28743cc209789205ac04d0601e566e71; GeeTestAjaxUser=0520a5ef896f5649e71a299d83fbe733",
        "Host": "api.geetest.com"
    }
    param = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt":0,
        "w":"Ni7uKMv6v0haadfMMsJJ4yRjiGVSKOTabFLHKGWvp)eBrxeqm03pLYxiSLpVmejX4YJ0Qm73oH)2yg1wBMBg)VuLfKLVkzYsL32jOCJbMFYX39KzMr1O)uBsI62enJ20OpnRgmhe6ANiHgn)0ZYgr0i1q7tQEuWnnlVT6QaG)6mCqIaGIBcNoGUpB)PnRxFodAVMZ(qlDhYxFYBgwJvrsVykqota2iRNG8SfEK4qPLLiOKWbfYJYxve3qmPG7sp5WWmn)YupGO2EOt1bFNwhPTFJHkGFHH17IXsKyf1hwiTqBMtf88RvrrLZOPc82GxXO9GLQqz2pS3g9BeZy3yIGASTPu698n7VnKrxDzh8rsgKyz09zLW9N90O6gZY5eOLaeLIVgCgaWenl6ql6c9tTm8)6wRfr7z0hC7ETCqAo1tGOHmYQC5UBzvfB2zsug7R(0XSXAlvk4KOvj)d)CODDw6gDZRGsvjSvWad2rhY5hb9i415m8mNZLndNVCqI9euzCkQ47)kZuz6ed2wCHKxGOtT10wIHGQKcWJ3m2VWTWbbH9jZafxfrebBmjRqxnegyKUM5PO4VgfTQgNujnljr43gvBug8vIO3sjY3KnffIh0MwpWYqt5FMgVsMWnp6WYI3TbebZ1oj0Xa8j10mnOOzmzfs4Eqj)VoJpft7hTN2bKHTimVJ(5TN7gKhUzvejBiGEfSUV6DXg08PYYWC3M6w88o45CyLg4hgn28DniIn6cD8TZ8Mu7r2pZIBq5JK5TSUaKoXMxTRGC5kPn9mEKN6rKAmWySd7dHUNmr8R3iP6Lq2x(IgZgJ3QyA5vdTJqWy7OwAI74MUmOEDiVLj9hci(koeg4RteDZuAEKyViF8FgaSpbKfFQbmI5436VO5gt4M59sFhQKVZe1LnBo3ktbUnEaw8B2cTMaqb2M(8kgCqFD43DytgxnXCs4w7qaClrVs61IvFKkjADIzkamYjbAy2rXiZCKcbZ3MuiulpYKvkBCWJlKsyc4xDn2u3e59mTZLU6yyHgpaoEhSPYd93WmnSywEtnsT)Mg2FZ(4fR3lkaElrr)vD08hBQFoeeWNuopbtaEw7XCThOYgioermUMxyuahD)hlvhufhxHuKeuHWkekjAkMHoCjKTl2NmVJRLeiQoDJuoNtSpDxmxp)H(618dEM23QgK882z55GOmasOam1gvvA3ObMYjRJPhGPtckYmm7bgmtG8hMdjimhqw51MD4mJns3x)H7iJ0c7FsYtiiUd)88GYBQ8x0eK57clpOtlxaDKdEe2KNAyojbQ1v7dCoKrM6r51KAsjXAKpUzsSs6nRsrQFbws8i5(YTu7zZ0On637kt9NDfP3cbHl5EyWAhgv(on(mZS4f(aObh00PREOqLtiGh1rQRtQnwJEwSfIGaJM30)j0qnriDVCfZJRUq7Y6DIzdKBOaaVF0qKzlXjf2jJgj8xBGFlEMWUeCVAMTdTljIKeeWrBlVUpiBpuDCbmREdgCKsbmeFRQDa2QVLB0wmw4iF6qu6uUpoTjRZtcgGvkpd(V6m61tfmAroUlJbGvrPZCb62z5ge)kpyuDXSXuRqnVbsv22QI(YO)X7BRsUauhYdQ(hHNXX69U30ldm9Wg6(fkzI3yeAwTsAUQrm7O)sco4nP5AKs0YWhQCQbqMCD9qr0rZHwZmH1u8wMeaQK4GzWrYe9FDVUIZFDUG(iIbd9IRX(ACdn8Tv2LhFudk3HXnK0FG1rF6i1A0AyDfLJ3y2wseKav)HcBO6KB87ZXVh9j3Cb6)LzYKPn1nMD(gey(hnQxv)kWNOnNqvoVA0evRjJ4Jz9QhwL)2frNPT9j4cIZY9COPHAir4BwcgPQGxJeTCY6Eg8fzGv38FFCErLMLFy)Zb9ykCpG0vPkPkTaAwlN0XF(Fb0zmvopPQ217vv9ZNhPrl49FB)6jef0rXf3f1Cj0eBU0f76smicocWtIsyEc)AFq9x2)LZ5Xdo0taRF4tDVFlNPCz0N(sD7(96p0ASPBNy1GlIP5DuENFNzmlDUpkOVsxMlIJZ1kvBcVEFAkYOFA9gUXVHqmlvWPcz2ha4PENx2(QfoUpb9Kdo3DdDz)nB2)nH3Unb8adrVBEpd7Uj8ukrjC5)LQGS8ArWdJFWDuxJjSnZcweEdHaUAHzqGZANX4YNkI)fag9eE7X9DpGtXV17QVTa5gP5T5BWbzG5D0mbAXQX7v)27BwBh5iIhq3mI81HHWoTgPJkCV(hXL(ZvukjhJS0DMgxbEXDXqGBcoNgBswsvm4Zk)ZkC2)qGeJRTv3DzTimgFgJ22wCNNMNCSZUPYpcIyravybt)BmLXTg(I0JrXC7uQFn5AWEG59s54UdK93q9WCGgsonx3WtauXOffWUJW)OAQLASKlz4Gfr(wu9uo0MSl6HwbLFI)4Ide5uso2eXB)q(N57ZKTG3VyxpoafRmpO(pseKdJ2d(lAo6JW(iXh8QIs(dEr7xqmDG9cezS9oanyBvHDlNBUXmRFRCmMPQQ3wMtIK7GSztvXn8tZMdMwKg55)q(2Fzmw6yzYFnNMAuYaxDUjGiPHhCrOulhreO0oqiz9uDrwd8jH4jIt7(qxBe(sHoVUL2aaDu2vdJiLVsuJeO6Bv0SE1bxMi6SD2gAMsRjok(nWdB5sTKS6H(8s83KF3d0dWh0ZgrUrNR9107t5T8lJclkjiBHvgMuqI2KgTo9yVK3z5IuNM)SCGelk.5614294925184f8de9a81528b613fac834c098da1e27e099a06b6584054c0650be2bfaa057006af5cbbf6bfe8a1c53ccf1c2becb49767fe18854f8b8e3411937f54efe3dcfa6d766a6bda31f39e858582ed377361358092d0e401bf3e5ebfea9568ff69d5c6724de009d9eeea0ca9df7d2cd7cc62d51136bc450b3aa881d856f",
        "callback": "geetest_" + str(int(time.time()*1000))    #1584360356918
    }
    response = requests.get(url, params=param, headers=header, verify=False)
    response.encoding = "utf8"
    jsonString = re.findall(r"\{.+\}",response.text,re.S)
    jsonDict = json.loads(jsonString[0])
    #print("第一次get请求：",jsonDict["status"])

def getImgUrlAjax(gt,challenge,w):  # 第一次ajax请求验证，一般返回slide
    url = "https://api.geetest.com/ajax.php"
    header = {
        "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Referer": "https://passport.bilibili.com/login",
        "Cookie": "GeeTestUser=28743cc209789205ac04d0601e566e71; GeeTestAjaxUser=0520a5ef896f5649e71a299d83fbe733",
        "Host": "api.geetest.com"
    }
    param = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt":0,
        "w":w,
        "callback": "geetest_" + str(int(time.time()*1000))    #1584360356918
    }
    response = requests.get(url, params=param, headers=header, verify=False)
    response.encoding = "utf8"
    jsonString = re.findall(r"\{.+\}",response.text,re.S)
    jsonDict = json.loads(jsonString[0])
    #print("第二次ajax请求：",jsonDict)
    return jsonDict


def getImgUrl(gt,challenge):  # 获取滑块图片URL
    url = "https://api.geetest.com/get.php"
    header = {
        "UserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Referer": "https://passport.bilibili.com/login",
        "Cookie": "GeeTestUser=28743cc209789205ac04d0601e566e71; GeeTestAjaxUser=0520a5ef896f5649e71a299d83fbe733",
        "Host": "api.geetest.com"
    }
    param = {
        "is_next": "true",
        "type": "slide3",
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "https": "false",
        "protocol": "https://",
        "offline": "false",
        "product": "embed",
        "api_server": "api.geetest.com",
        "isPC": "true",
        "area": "#geetest-wrap",
        "width": "100%",
        "callback": "geetest_" + str(int(time.time()*1000))    #1584360356918
    }
    response = requests.get(url, params=param, headers=header, verify=False)
    response.encoding = "utf8"
    jsonString = re.findall(r"\{.+\}",response.text,re.S)
    jsonDict = json.loads(jsonString[0])
    if jsonDict["theme"] == "ant":
        #print("第三次get请求：success")
        fullbg = jsonDict["fullbg"]
        bg = jsonDict["bg"]
        s = jsonDict["s"]
        newChallenge = jsonDict["challenge"]
        #print("s = ",s)
        return bg, fullbg, newChallenge,s
    
    print("第三次get请求：error")
    exit(10)

def compare_images(img_one, img_two):  # 图片对比，寻找缺口位置坐标
    try:
        diff = ImageChops.difference(img_one, img_two)
        
        if diff.getbbox() is None:
            print("【+】We are the same!")
        else:
            diff = Image.eval(diff.convert("L"), lambda x: 0 if x < 20 else 255)
            # print("验证码滑块的坐标：",diff.getbbox())
            return diff.getbbox()[0]
            diff.save("different.jpg")
    except ValueError as e:
        print("【{0}】{1}".format(e, "比较过程中出现异常"))

def createMoveArray(maxX):   # 根据缺口x坐标，伪造轨迹数据
    clickPosition = [-random.randint(28,35),-random.randint(28,36),0]
    x,y,t = 0,0,0
    array = [clickPosition,[0,0,0]]
    flag = random.choice([-1,1])   # 决定y的移动方向
    while(x<maxX):
        if x <= maxX/3:
            x = x + random.randint(8,17)-int(10*x/maxX)
            y = y + flag*random.choice([0,1,0,0,0,0,1,1,0,1,0,1])
            if len(array)==2:
                t = t + random.randint(60,100)
            t = t + random.randint(15,19)
        elif maxX/3 < x < 4*maxX/5:
            x = x + random.randint(5,9) + random.choice([-1,0,0,-1,1,1,1,1,1,0,1])
            y = y + flag*random.choice([0,1,0,0,0,0,1,0,0,1])
            t = t + random.randint(15,19)
        elif x >= 4*maxX/5:
            x = x + random.choice([1,1,1,1,0,1,0,1,1,1,1,0,2])
            y = y + flag*random.choice([0,1,0,0,0,0,1,0,1,0])
            t = t + random.randint(15,19) + 40*random.choice([1,0,1.2,1.3,0])
        array.append([x,y,t])
        gc.collect()
    array[-1][-1] += random.randint(150,230)
    return array

def main():
    gt,challenge = getGtChallenge()
    getImgUrlOnce(gt, challenge)
    w = "awagksfZsemQNbK48rxjZOH0m41GWoZ(lcQpM(TUTlgaD7kdrz224QXUbUtrpeosfebolNgP6Xl5GBxrghy699rKRe8E9rW)iRghd9KlUk4Rp5swbSrrIHeH8Pjvbt89kp4NlpDOY0n5QlwM90D6)SHG0Cb7qzgK)mOOHQ0(GXhJEryh7KvsZr0IwkjinnZyJiLcHXPpe3yvw1)r35xJd3KhiKJGuss8HI48cTBnOTiFLt2pKQdjF)BhS82tQAVWZaUnVLJw349qjsd)J8TDIk4ISnDMYWcsc1CiVqAKSOjVWH6836XCvHGEvF0Lx6JXOrswD1nDUClBAEBJTuB(CvDNIXWIVpsI)gT6OG)uo((zxl5d6Jk7hjPUS6m(U01Yso1sj7xscW9H5BA1n(VxNXSe7PDMZ9NEF6bPy9odFqNhmkLXHGQVHQiH6dEq91DiY97NdkjwA74aIyogKT4NbAq4M0yQhTphN4Ya27)72snQ02GXxMQHtzh7a5ODiVj0agobVgCV3gnO3irS9QS7vS3nVwFVervYGVBu6srbQ8zQXESlisKrC3SKD4rec3(3KgGTyXtQm9wnhqzmIMHKw52UU64egujL()0pVoWBpWmqAty1wApDmQZ5gYlzpvFQ4muCdrydfvds(c9M)75yei4NbsBMf728f7usJsQBGvKRRPFuAxCe5x79cSlwuNiwCcMnGB)yYwL)6)7Is)5SE907VpW4BQbg5DQOKx2qjZ8WyHRBcAwOyvhpIjdh)qInP8SsUs8kndzeKOskRggD75OrRLls7fyzRFr6FaisVIOawXLJAffraGo1Jm3Z9c3RiLG1Y)8BB9zEllZ9nMiT6IiJJXL3UteSfI)Fn1apZ8amImheDsHESuvidHpX7LLOlCbJ)lQsoklvAI0gZYPU6)OwBfXsMF4eGDjaTInGp0nbjiCfF2ZZoNA5ut30bHJd8gLP8NIzl2MzZoP1eeE80lyKwnjiVC(jJKuU278AeWwoT4prw4TnJIhjYlf)QEPkffsmmD(tujqQdCcdQlhN7Cg(uuHlVE)wBM1KvC8lk9qaHVpzijF)zNsmeanzE99wJUvYSga4NjkhT2Uo3xxXqiFMiAgiSwznbKwPT5y5W6lbaulwlmV3bCFYqrC27jK(ynzNdClAbVQsyvOo9R3mfZVB635V5usNvEvoOH5dB3uJkjSAbBrXPzIgF0TubJzrY3l96JvSwGySlp1zyiUZcnXNg6mXrnoBpgNZpUBlrjVXC0fc2VaAGIdWQkKyIng2mXBILoicCNCJZd3kWK4S9BbOEQirNBs3yYZJK4gD7Wsij3VNX5(u9lcxKH23cnSHRPKSh652TP4bh7kWwOJwoLXDZeojhmw30LH5ldhAi24(FqOsnO2eQ)oQ5NG1k2xjnKgdjFU02SVEnFUDpsxd(YQjbeHO7g81p0oltBHXmUNWACQECrqsO0AHFrvjS4v3JQ2sTrXtZjGQANTXd1mdsg6nmgK5b7t1C)DZT4(j2zeFxDzZY3CxA(mDRV4OAPiWvJ3Bc34sr2zND1orBjyjiXewyUftoTx2YIq2l7)22anwonLaRPu5KBLHvtCAOqOLhWj6FTNwux)lRcO8mjPl41ybVDVMVfGiWsbvSzz9O6QSTbmB3jhj(HT(PuF3Ga4HHnE8SS4ZPqth(INJdSCWpqrUZjJVXkKM5ijsfS9RJgO8d9b0DceL66Hm3pVsHe8nJEmzkuQ6as5QrF)e94ZoZ0nbYmNte2qwl1YDLh5)0tnrSbOzUS1OWxHjjnomPWrh9jpb6FKHimT2rcOqwoej7QoYaVIGUFSoj1sJK5bEi(nsy09XQJ870DhB3L86M9ov9xcr7viMI9fYZ64UUaqMez3UR7JBb(RzKXUIDAOrBYeYdg93mdJ1OXpGFBu(1QOlUhsweaC(8dYVhu2LaGf7u9D7dqbcF9j)HqjfidPeATPOj2G)SP8X)SykIn6i4YiwOotNQQaKc0CilHNp9DJ921NyELOo7MRgvnIbjU904(lztZJ8W0Ly(J5Mzr0vteJBd9k)EQi9Bo2yYhXxYTDDT2r14VwIJmQDy8Aqz57K(CQF0xY6xvivwe0qZaIPXfsmSBjTRutns2Qii2go2JwdCLquwY6Ro4BJQZKyff0o7lz(O0nyAprbH8c4jL5SEDpn"
    getImgUrlAjax(gt, challenge,w)
    bg, fullbg, challenge,s = getImgUrl(gt, challenge)  # challenge会变化
    bg_url = "https://static.geetest.com/" + bg
    fullbg_url = "https://static.geetest.com/" + fullbg
    imgObj1 = reImg(downloadImg(bg_url,"bg"))
    imgObj2 = reImg(downloadImg(fullbg_url,"fullbg"))

    x = compare_images(imgObj1,imgObj2)
    t = int(time.time()*1000-15000)
    #print("new challenge = ",challenge)
    array = createMoveArray(x-7)
    data = {
        "gt":gt,
        "challenge":challenge,
        "s":s,
        "t":t,
        "mouseMoveArray": array
    }
    res = requests.post("http://127.0.0.1:8080/token",data=data)
    response = getImgUrlAjax(gt, challenge, json.loads(res.text)["w"])
    print(response)
    global success
    if response["message"] == "success":
        success += 1

if __name__ == "__main__":
    for i in range(50):
        try:
            main()
        except Exception as e:
            continue
        time.sleep(1)
    print("成功率：",success*2,"%")
