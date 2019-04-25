import requests

url = 'http://127.0.0.1:8080/examples/servlets/servlet/SessionExample'
res = requests.get(url)
if res.status_code != 200:
	pass
else:
	if '400' in res.text or '404' in res.text or '403' in res.text:
		pass
	else:
		print 'Exaple Session Vul Found!'