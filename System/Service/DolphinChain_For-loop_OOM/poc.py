import requests

url='http://127.0.0.1:26657/blockchain?minHeight=-9223372036854775808&maxHeight=-9223372036854775788'
res = requests.get(url)