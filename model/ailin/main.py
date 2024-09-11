import datetime
import json
import sys
import requests
import hashlib
from .AbstractApi import ApiException
import time
from .RsaUtil import *


def __post_file(url, media_file):
    return requests.post(url, file=media_file).json()


def __httpGet(url):
    realUrl = url
    return requests.get(realUrl).json()


def __httpPost(url, args):
    realUrl = url
    return requests.post(realUrl, data=args).json()


def encrypt_data(publickey, msg):
    Rsa = RsaUtil()
    cipHypertext = Rsa.long_encrypt(publickey, msg)
    return cipHypertext


class AiApiAPI(object):
    httpHost = "http://43.192.61.92:8086"
    httpUrlUUID = "/v3/getUuid"
    httpAiTextImgUrl = "/v3/texttoimage"
    httpAiTextVideoUrl = "/v3/texttovideo"
    httpUrlDownload = "/v5/downLoad"

    data_list = [
        {"pkgName": "com.energysh.quickarte", "appId": "TX009", "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCgMZPYhCj0Q1KiPzeJpANL2dn0Owxi6SsJq7Xj4dGjwHa2yM7aDKYuVgz5h2qcuPiK7fxRQbzp+JdDLwofOorlnkljPB9H/C7nUQsQuK0rQk9LoJyXd0wQBNB3XIDrCSgel+SsWYnjFqAR7PTMQ4MfNT2cyI03bRugT0EdWJRXswIDAQAB"},
        {"pkgName": "com.dt.test1", "appId": "DT001", "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUbEM4IE7DCfc9FswhWSKGmVVix8AQiCqETEJerzqCeVPZ9V6Q7dCg+y/1KC7nap19y9eWyY5c62KDBiWeLdcGkMJO/Beqqi8QpJPEpVEEB98gslXeyX3JEUfuIL+LmGx99Qz5i2n1qYhAetW8pj8t2uGmdatMmkemWsB6wWq3KQIDAQAB"},
        {"pkgName": "com.dt.test2", "appId": "DT002", "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4mn/e5Xj39CaKPHbRBrjNtN42F20Ls5kx39l5gjOoUKIDe6TI9EDoGyVHokadQ/Zi/wxy6vlurY2xfAquYWMCcoRW0TvjSwlHLhgYjuY1f3ECjj+Qs3gv1Px1CBBmJkZXCOBLmKD2jOhOybDK02Nj7brNPoSnlbljrQF+2qD+yQIDAQAB"},
        {"pkgName": "com.dt.test3", "appId": "DT003", "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCWEwZvyDwtp+vcWcFG72NnK3T3Zer/r5QNSgUtOo9oAcCLEIBbIzWW0xLXsoligo8XctcZDLlhFpOD04BM+BbViG+YZajiylGcMxd+YaksR9Z6cGNx9oJiXzVaIr/BRCYinLMA8awvpmQsFr9ckaAILqER+d44iX4j8nI0WbntPQIDAQAB"},
        {"pkgName": "com.dt.test4", "appId": "DT004", "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCl5s0/hya3wX9fU7KVHiDwE6SecJ4I5G05vrW5V4z0I9Ds9/M6t77p01lpJzX9Q2cCmy4NRYO8EHzVDF/yYIcnO5Hx4A7rp5o7bjoA4SA3wVN6bzz6Pvj/K864Gl3BHeHO12PJ4Vm6rV2qNuB1dYXSlC3CUlq97MTazDELue9rTQIDAQAB"},
        {"pkgName": "com.dt.test5", "appId": "DT005", "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVAeEp0d04FP/q8ZMr82ayEyd615aFID6YVJUiKAaZlL6rJflDhDAukRruAhwssv1MJNPAdE36W7ob5R9f78w3K1c/vKPwZubQ/bMgHAtVlxWaxHDCxi74tVUi3WVe7flgQK2izbrIKmDu/5VMZRfjJ0w+y0DA1OFx+s3fdr9v/wIDAQAB"}
    ]

    isVip = True
    functionTag = "texttoimage"

    def getAppInfo(self,key):
        for data in self.data_list:
            if key == data["key"]:
                return data
        assert "密钥不存在、确认密钥是否存在！"

    def __init__(self):
        self.keyUUid = None
        self.keyUUidTime = None

    def getUUid(self):
        if self.keyUUid is None:
            self.refUuid()
        elif self.keyUUidTime is None or (datetime.datetime.now() - self.keyUUidTime).seconds >= 1800:
            self.refUuid()
        return self.keyUUid

    def callAI(self, prompt, fun,key):
        self.getUUid()
        curtime = int(datetime.datetime.now().timestamp() * 1000)
        uuid = self.getUUid()
        md5Str = self.getAppInfo(key)['pkgName'] + uuid + str(curtime)
        md5 = hashlib.md5()
        md5.update(md5Str.encode('utf-8'))
        str_md5 = md5.hexdigest()
        # print(str_md5)

        tinyDict = {"appTime": curtime, "priority": 10, "uId": uuid, "pkgName": self.getAppInfo(key)['pkgName'],
                    "platFormId": "Modeltest"}

        destroy = json.dumps(tinyDict)
        # print(destroy)
        destroy = encrypt_data(key, destroy)
        # print(destroy)
        content = {
            "prompt": prompt,
            "negative_prompt": ""
        }
        content_json = json.dumps(content)
        url = AiApiAPI.httpAiTextImgUrl
        if fun == "texttovideo":
            url = AiApiAPI.httpAiTextVideoUrl
        params = {'decrypt': destroy, 'pkgName': self.getAppInfo(key)['pkgName'], 'sign': str_md5, 'content': content_json, "uId": uuid}
        response = self.httpCall([url, 'POST'], params)
        # print(response)
        if response is not None and response.get('success'):
            if fun == "texttovideo":
                return self.getDownloadData(response.get('data'), 1000)
            else:
                return self.getDownloadData(response.get('data'), 30)

        else:
            pass
        pass

    def getDownloadData(self, dataID, times):
        for i in range(0, times):
            try:
                response = self.httpCall([AiApiAPI.httpUrlDownload + "/" + dataID, 'POST'], {})
                print(response)
                return response.get('data')
            except ApiException as e:
                if e.errCode == 409:
                    print("\r", end="")
                    print("进度: {}%: ".format(i), "▓" * (2 // times), end="|")
                    sys.stdout.flush()
                    time.sleep(1)
                else:
                    print("请注意：" + e.errMsg + " 程序暂停，请重新发起请求")
                    return

    def __httpPost(self, url, args):
        realUrl = url
        return requests.post(realUrl, data=args).json()

    def __httpGet(self, url):
        realUrl = url
        return requests.get(realUrl).json()

    def httpCall(self, urlType, args=None):
        shortUrl = urlType[0]
        method = urlType[1]
        response = {}
        for retryCnt in range(0, 1):
            if 'POST' == method:
                url = self.__makeUrl(shortUrl)
                response = self.__httpPost(url, args)
            elif 'GET' == method:
                url = self.__makeUrl(shortUrl)
                url = self.__appendArgs(url, args)
                response = self.__httpGet(url)
            else:
                raise ApiException(-1, "unknown method type")

            if self.__tokenExpired(response.get('code')):
                self.__refreshToken(shortUrl)
                retryCnt += 1
                continue
            else:
                break
        return self.__checkResponse(response)

    @staticmethod
    def __appendArgs(url, args):
        if args is None:
            return url

        for key, value in args.items():
            if '?' in url:
                url += ('&' + key + '=' + value)
            else:
                url += ('?' + key + '=' + value)
        return url

    @staticmethod
    def __makeUrl(shortUrl):
        base = AiApiAPI.httpHost
        if shortUrl[0] == '/':
            return base + shortUrl
        else:
            return base + '/' + shortUrl

    def refUuid(self,key):
        params = {'appId': self.getAppInfo(key)['appId'], 'isVip': self.isVip, "pkgName": self.getAppInfo(key)['pkgName'], 'functionTag': self.functionTag,
                  "country": "zh"}
        response = self.httpCall([AiApiAPI.httpUrlUUID, 'POST'], params)
        print(response)
        if response is not None and response.get('success') is not None:
            self.keyUUid = response.get('data')
            self.keyUUidTime = datetime.datetime.now()

    @staticmethod
    def __tokenExpired(errCode):
        if errCode == 1000:
            return True
        else:
            return False

    @staticmethod
    def __checkResponse(response):
        errCode = response.get('success')
        errMsg = response.get('message')
        if errCode:
            return response
        else:
            raise ApiException(response.get('code'), errMsg)

    def __refreshToken(self):
        self.refUuid()

    def exe(self,key,fun,content):
        api = AiApiAPI()
        api.refUuid(key)
        response = api.callAI(content, fun,key)
        return response



if __name__ == '__main__':
    api = AiApiAPI()
    # 参数1:密钥
    # 参数2：texttoimage为文生图功能、texttovideo 为文生视频功能
    # 参数3：提示词
    key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVAeEp0d04FP/q8ZMr82ayEyd615aFID6YVJUiKAaZlL6rJflDhDAukRruAhwssv1MJNPAdE36W7ob5R9f78w3K1c/vKPwZubQ/bMgHAtVlxWaxHDCxi74tVUi3WVe7flgQK2izbrIKmDu/5VMZRfjJ0w+y0DA1OFx+s3fdr9v/wIDAQAB"
    api.exe(key,"texttoimage","猫捉老鼠")
