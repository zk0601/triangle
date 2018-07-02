# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类

# import http.client
# import urllib
import json
import hashlib
import requests

def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    return  hashlib.md5(data.encode("utf8")).hexdigest().upper()

def httpGet(url,resource,params=''):
    # conn = http.client.HTTPSConnection(url, timeout=10)
    # conn.request("GET",resource + '?' + params)
    # response = conn.getresponse()
    # data = response.read().decode('utf-8')
    # return json.loads(data)
    request_url = url + resource + '?' + params
    try:
        conn = requests.get(request_url, timeout=10)
    except Exception as e:
        print(e)
        return None
    return json.loads(conn.content)

def httpPost(url,resource,params):
     # conn = http.client.HTTPSConnection(url, timeout=10)
     # temp_params = urllib.parse.urlencode(params)
     # conn.request("POST", resource, temp_params, headers)
     # response = conn.getresponse()
     # data = response.read().decode('utf-8')
     # params.clear()
     # conn.close()
     # return data
     headers = {
         "Content-type": "application/x-www-form-urlencoded",
     }
     request_url = url + resource
     try:
        conn = requests.post(request_url, data=params, headers=headers, timeout=10)
     except Exception as e:
         print(e)
         return None
     return conn.text

