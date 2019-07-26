#coding=utf8
import requests
import re
from flask.sessions import SecureCookieSessionInterface
import sys
import time
import string,random
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
    
def gen_str(i):
    text = randomString(i)
    v = sum(map(ord, text))
    while 1020 < v < 1028:
        text = randomString(i)
        v = sum(map(ord, text))
    return text, (v%2 == 0)
def checker(host, port):
    try:
        url = "http://"+host+":"+str(port)
        for i in list(range(40))+list(range(40,20,-2)):
            text, expected = gen_str(i)
            r = requests.post(url+'/post',data={'title':randomString(30),'author':randomString(8),'content':text},timeout=3,headers={'User-Agent':'checker'}).text
            if expected and 'reject' not in r:
                raise Exception('网站功能逻辑错误')
            elif not expected and text not in r:
                raise Exception('网站功能逻辑错误')
        # check WAF
        text, expected = gen_str(i)
        r = requests.post(url+'/post',data={'title':randomString(30),'author':randomString(8),'content':text},timeout=3,headers={'User-Agent':randomString(50)}).text
        if expected and 'reject' not in r:
            raise Exception('疑似通用防御(UA)')
        elif not expected and text not in r:
            raise Exception('疑似通用防御(UA)')
            
        r = requests.post(url+'/admin',headers={'User-Agent':randomString(50)}).text
        if 'Not a admin' not in r:
            raise Exception('疑似通用防御(/admin不符合预期)')
            
        return (True,"IP: "+host+" OK")
    except Exception as e:
        return (False, "IP: "+host+" is down, "+str(e))

if __name__ == '__main__':
    # print(checker("192.168.8.10", 10001))
    ip=sys.argv[1]
    port=int(sys.argv[2])
    print(checker(ip,port))