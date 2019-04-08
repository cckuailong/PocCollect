# -*- coding: utf-8 -*
#!/usr/bin/python
#####################################
##KILL THE NET##
##############[LIBS]###################
import requests, re, urllib2, os, sys, codecs, random				
from multiprocessing.dummy import Pool					     	
from time import time as timer	
import time				   		
from platform import system	
from colorama import Fore								
from colorama import Style								
from pprint import pprint								
from colorama import init
from urlparse import urlparse
import warnings
import subprocess
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
reload(sys)  
sys.setdefaultencoding('utf8')
init(autoreset=True)
##########################################################################################
ktnred = '\033[31m'
ktngreen = '\033[32m'
ktn3yell = '\033[33m'
ktn4blue = '\033[34m'
ktn5purp = '\033[35m'
ktn6blueblue = '\033[36m'
ktn7grey = '\033[37m'
CEND = '\033[0m'		
#####################################
##########################################################################################
try:
	with codecs.open(sys.argv[1], mode='r', encoding='ascii', errors='ignore') as f:
		ooo = f.read().splitlines()
except IOError:
	pass
ooo = list((ooo))
##########################################################################################

def wp_exp(url):
	try:
		link = url + '/wp-content/plugins/easy-wp-smtp/readme.txt'
		sss = requests.session()
		Agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}
		ktn1 = sss.get(link, headers=Agent, verify=False, timeout=20, allow_redirects=False)
		if '= 1.3.9 =' in ktn1.content:
			print (ktngreen + 'SITE VULN : ' + url + CEND)
			open('wpvuln.txt', 'a').write(url+'\n')
			pass
		else:
			print(ktnred + 'SITE NOT VULN : ' + url + CEND)


		pass
	except:
		pass
	pass

##########################################################################################
##########################################################################################
def logo():
	clear = "\x1b[0m"
	colors = [36, 32, 34, 35, 31, 37]
	x = ''' 
				 FEDERATION BLACK HAT SYSTEM | IG: @_gghost666_ 

<-.(`-')  _                      (`-')      (`-').-> (`-')  _<-. (`-')_  (`-')  _(`-')      
 __( OO) (_)      <-.      <-.   ( OO).->   (OO )__  ( OO).-/   \( OO) ) ( OO).-/( OO).->   
'-'. ,--.,-(`-'),--. )   ,--. )  /    '._  ,--. ,'-'(,------.,--./ ,--/ (,------./    '._   
|  .'   /| ( OO)|  (`-') |  (`-')|'--...__)|  | |  | |  .---'|   \ |  |  |  .---'|'--...__) 
|      /)|  |  )|  |OO ) |  |OO )`--.  .--'|  `-'  |(|  '--. |  . '|  |)(|  '--. `--.  .--' 
|  .   '(|  |_/(|  '__ |(|  '__ |   |  |   |  .-.  | |  .--' |  |\    |  |  .--'    |  |    
|  |\   \|  |'->|     |' |     |'   |  |   |  | |  | |  `---.|  | \   |  |  `---.   |  |    
`--' '--'`--'   `-----'  `-----'    `--'   `--' `--' `------'`--'  `--'  `------'   `--'    
									  KILL THE NET
									 FB: fb/KtN.1990  
			   Note! : We Accept any responsibility for any illegal usage :). '''

	for N, line in enumerate(x.split("\n")):
		sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
		time.sleep(0.05)
		pass


logo()
##########################################################################################
def Main():
	try:
		
		start = timer()
		ThreadPool = Pool(50)
		Threads = ThreadPool.map(wp_exp, ooo)
		print('TIME TAKE: ' + str(timer() - start) + ' S')
	except:
		pass


if __name__ == '__main__':
	Main()
