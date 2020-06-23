import requests
import time, re, json
import execjs
requests.packages.urllib3.disable_warnings()

# VIP视频解析网站：https://www.f41.cc

def getRequest(vip):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Referer": "https://jx.xiaolangyun.com/jiexi/?url=%s"%vip,
        "Connection": "keep-alive",
        "Host": "jx.yaohuaxuan.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,br",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }
    
    url = "https://jx.yaohuaxuan.com/suiji1/?url=" + vip
    response = requests.get(url,headers=header,verify=False)
    response.encoding = "utf8"
    print("GET请求码：", response.status_code)
    return response.text

def findParam(response):
    Time = re.findall("var Time = (\d{10});",response, re.I)
    # Url = re.findall("var Url = \"(.+?)\";",response, re.I)
    # Ather = re.findall("var Ather = \"(.+?)\";",response, re.I)
    Vkey = re.findall("var Vkey = \"(.+?)\";",response, re.I)
    Key = re.findall("var Key = \"(.+?)\";",response, re.I)
    Ref = re.findall("var Ref = \"(.+?)\";",response, re.I)
    try:
        return Time[0],Vkey[0],Key[0],Ref[0]
    except Exception as e:
        print("参数获取失败：",e)
        exit(-1)

def call_js(time, vkey, key, ref, vip, type, decode_url=None):
    with open("./手扣js.js", "r", encoding="utf8") as fp:
        js_text = fp.read()
    js = execjs.compile(js_text)
    if type == "encode":
        return js.call("code","encode",time, vkey, key, ref, vip, "")
    elif type == "decode":
        return js.call("code", "decode", time, vkey, key, ref, vip, decode_url)

def postRequest(vip, Token, access_token, Vkey, Key, Sign, Ref, Time, uuid):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Connection": "keep-alive",
        "Host": "jx.yaohuaxuan.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,br",
        "Origin": "https://jx.yaohuaxuan.com",
        "Token": Vkey,
        "Access-Token": access_token,
        "Version": "V3.0",
        "Cookie": "uuid="+ uuid,
    }
    data = {
            'url': vip,
            'wap': "0",
            'ios': "0",
            'host': "jx.yaohuaxuan.com",
            'key': Key,
            'sign': Sign,
            'token': Token,
            'type': "",
            'referer': Ref,
            'time': Time
        }
    response = requests.post("https://jx.yaohuaxuan.com/suiji1/Api.php", headers=header, data = data, verify=False)
    response.encoding = "utf8"
    print("POST请求码：",response.status_code)
    # print(response.text)
    return response.json()

if __name__ == '__main__':
    vip = "https://v.qq.com/x/cover/r5trbf8xs5uwok1.html"    # 要解析的vip视频URL

    text = getRequest(vip)         #  获得包含Time, Vkey, Key, Ref等参数的HTML
    # print(text)
    Time, Vkey, Key, Ref = findParam(text)   # 正则匹配获取参数
    # print(Time,Vkey,Key, Ref,sep="\n")
    js_return = call_js(Time, Vkey, Key, Ref, vip, "encode")   # 调用js加密生成Sign、Token及cookie值
    js_json = json.loads(js_return)
    Sign, Token, Access_token, Uuid = js_json["Sign"], js_json["Token"], js_json["Access_token"], js_json["uuid"]
    time.sleep(2)
    response_json = postRequest(vip,Token,Access_token,Vkey,Key,Sign,Ref,Time,Uuid)   # post请求获取视频的URL
    
    get_url = call_js(Time, Vkey, Key, Ref, vip, "decode",decode_url=response_json["url"])  # 调用js解密返回的url值
    
    print(get_url)
    
    
    
    