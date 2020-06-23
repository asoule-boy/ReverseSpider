import requests
import json,re
import time
from PIL import Image, ImageChops
requests.packages.urllib3.disable_warnings()

class TDCRequest(object):
    def __init__(self):
        self.session = requests.session()
        self.config = {
            "aid": "2100049389"
        }
        self.ts = int(time.time()*1000)

    def getRequest(self, url, param):
        header = {
            "user-agent": "Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        response = self.session.get(url, params=param,headers=header, verify = False)
        response.encoding = "utf8"
        if response.status_code == 200:
            return response
        print("[%s]%d 请求出错"%(url, response.status_code))
        exit(-2)

    def getSessSid(self):
        param = {
            "aid": "2100049389",
            "protocol": "https",
            "accver": "1",
            "showtype": "popup",
            "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OS4wLjM0OTcuMTAwIFNhZmFyaS81MzcuMzY=",
            "noheader": "1",
            "fb": "1",
            "enableDarkMode": "0",
            "fpinfo": "fpsig=1100F99BB518CB896AD4B677A6AD206D6EA7583E3009700528E37E274D461B416E14B3CBE405F71A64223643673180ABE40C",
            "tkid": "1676214933",
            "grayscale": "1",
            "clientype": "2",
            "cap_cd": "",
            "uid": "",
            "wxLang": "",
            "subsid": "1",
            "callback": "_aq_999838",
            "sess": ""
        }
        response = self.getRequest("https://ssl.captcha.qq.com/cap_union_prehandle", param)
        jsonText = re.findall('\{.+\}',response.text, re.S)
        jsonDict = json.loads(jsonText[0])
        self.config["sess"] = jsonDict["sess"]
        self.config["sid"] = jsonDict["sid"]
        self.config["subcapclass"] = jsonDict["subcapclass"]

    def getWebsigVsig(self):
        param = {
            "aid": self.config["aid"],
            "protocol": "https",
            "accver": "1",
            "showtype": "popup",
            "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OS4wLjM0OTcuMTAwIFNhZmFyaS81MzcuMzY=",
            "noheader": "1",
            "fb": "1",
            "enableDarkMode": "0",
            "fpinfo": "fpsig=1100F99BB518CB896AD4B677A6AD206D6EA7583E3009700528E37E274D461B416E14B3CBE405F71A64223643673180ABE40C",
            "tkid": "1676214933",
            "grayscale": "1",
            "clientype": "2",
            "subsid": "2",
            "sess": self.config["sess"],
            "fwidth": "0",
            "sid": self.config["sid"],
            "forcestyle": "undefined",
            "wxLang": "",
            "tcScale": "1",
            "uid": "",
            "cap_cd": "",
            "rnd": "199764",
            "TCapIframeLoadTime": "undefined",
            "prehandleLoadTime": 127,
            "createIframeStart": str(self.ts)
        }
        response = self.getRequest("https://ssl.captcha.qq.com/cap_union_new_show",param=param)
        jsonStr = re.findall('function\(\)\{window.captchaConfig=(\{.*?\})', response.text, re.S)
        # print(jsonStr)
        self.config["websig"] = re.findall(',websig:"(.*?)"',jsonStr[0],re.S)[0]
        self.config["vsig"] = re.findall(',vsig:"(.*?)"',jsonStr[0],re.S)[0]
        self.config["collectdata"] = re.findall(',collectdata:"(.*?)"',jsonStr[0],re.S)[0]
        self.config["spt"] = re.findall(',spt:"(.*?)"',jsonStr[0],re.S)[0]
        # exit(0)

    def downloadImg(self):
        param = {
            "aid": self.config["aid"],
            "protocol": "https",
            "accver": "1",
            "showtype": "popup",
            "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OS4wLjM0OTcuMTAwIFNhZmFyaS81MzcuMzY=",
            "noheader": "1",
            "fb": "1",
            "enableDarkMode": "0",
            "fpinfo": "fpsig=1100F99BB518CB896AD4B677A6AD206D6EA7583E3009700528E37E274D461B416E14B3CBE405F71A64223643673180ABE40C",
            "tkid": "1676214933",
            "grayscale": "1",
            "clientype": "2",
            "subsid": "3",
            "sess": self.config["sess"],
            "fwidth": "0",
            "sid": self.config["sid"],
            "forcestyle": "undefined",
            "wxLang": "",
            "tcScale": "1",
            "uid": "",
            "cap_cd": "",
            "rnd": "199764",
            "TCapIframeLoadTime": "undefined",
            "prehandleLoadTime": 127,
            "createIframeStart": str(self.ts),
            "rand": "2894593",
            "websig": self.config["websig"],
            "vsig": self.config["vsig"],
            "img_index": "1"
        }
        with open("img001.jpg","wb") as fp:
            fp.write(self.getRequest("https://ssl.captcha.qq.com/cap_union_new_getcapbysig",param).content)
        param["img_index"] = "0"
        with open("img002.jpg","wb") as fs:
            fs.write(self.getRequest("https://ssl.captcha.qq.com/cap_union_new_getcapbysig",param).content)
        return "./img001.jpg","./img002.jpg"

    def compare_images(self, img_one_path, img_two_path):
        img_one = Image.open(img_one_path)
        img_two = Image.open(img_two_path)
        img_one_ = img_one.crop((0,10,img_one.width, img_one.height-20))
        img_two_ = img_two.crop((0,10,img_two.width, img_two.height-20))
        try:
            diff = ImageChops.difference(img_one_, img_two_)
            
            if diff.getbbox() is None:
                print("【+】We are the same!")
            else:
                diff = Image.eval(diff.convert("L"), lambda x: 0 if x < 20 else 255)
                diff.save("different2.jpg")
                print("验证码滑块的坐标：", diff.getbbox())
                return diff.getbbox()[0]
        except ValueError as e:
            print("【{0}】{1}".format(e, "比较过程中出现异常"))

    def callJs(self, x):
        data = {
            "distance": int(x/2-37.5),
            "ts": self.ts
        }
        res = requests.post("http://127.0.0.1:8080/tx",data=data)
        return json.loads(res.text)["w"]


    def postVerify(self, encryptData, X):
        header = {
            "user-agent": "Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        data = {
            "aid": self.config["aid"],
            "protocol": "https",
            "accver": "1",
            "showtype": "popup",
            "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82OS4wLjM0OTcuMTAwIFNhZmFyaS81MzcuMzY=",
            "noheader": "1",
            "fb": "1",
            "enableDarkMode": "0",
            "fpinfo": "fpsig=1100F99BB518CB896AD4B677A6AD206D6EA7583E3009700528E37E274D461B416E14B3CBE405F71A64223643673180ABE40C",
            "tkid": "1676214933",
            "grayscale": "1",
            "clientype": "2",
            "subsid": "3",
            "sess": self.config["sess"],
            "fwidth": "0",
            "sid": self.config["sid"],
            "forcestyle": "undefined",
            "wxLang": "",
            "tcScale": "1",
            "uid": "",
            "cap_cd": "",
            "rnd": "199764",
            "TCapIframeLoadTime": "undefined",
            "prehandleLoadTime": 127,
            "createIframeStart": str(self.ts),
            "ans": "%d,%s;"%(X,self.config["spt"]),
            "websig": self.config["websig"],
            "vsig": self.config["vsig"],
            "cdata": "90",
            "subcapclass": self.config["subcapclass"],
            self.config["collectdata"]: encryptData,
            "eks":"",
            "tlg":"2112",
            "vlg":"0_1_1"
        }
        response = self.session.post("https://ssl.captcha.qq.com/cap_union_new_verify",headers=header,data=data,verify=False)
        response.encoding = "utf8"
        print(response.json())
        return response.json()

if __name__ == "__main__":
    tdc = TDCRequest()
    success = 0
    for i in range(50):
        tdc.getSessSid()
        tdc.getWebsigVsig()
        path1, path2 = tdc.downloadImg()
        X = tdc.compare_images(path1, path2)
        encryData = tdc.callJs(X)
        jsonData = tdc.postVerify(encryData,X)
        if jsonData["errorCode"] == "0":
            success += 1
        time.sleep(1)
    print("成功率：%f"%(success*2),"%")
    