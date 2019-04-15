#!/usr/bin/python

import shodan
#uesr configer

API_KEY = "YokRfOEDBGu4jmxY8dbVJM9DU1KQ29jl"
api = shodan.Shodan(API_KEY)

try:
    results = api.search('ipcamera country:CN port:81 200 ok')
    print 'Results found %s' % results['total']
    for result in results['matches']:
        print 'IP: %s' % result['ip_str']
        #print result['ip_str']
        #print ''
        f = open('targetAddr.txt', 'a')
        f.writelines(result['ip_str']+'\n')
        f.close
except shodan.APIError, e:
    print 'Error: %s' % e
