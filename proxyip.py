#coding:utf-8
'''
Created on 2017��4��17��

@author: Lisen
'''

import requests
from bs4 import BeautifulSoup
import random

class Proxy_IP(object):
    
    def get_random_url(self):
        """
        Random compose a free ip url
        """
        i = random.randint(1,100)
        url = 'http://www.kuaidaili.com/free/inha/%s/' % str(i)
        return url 
    
    def get_ip_list(self):
        """
        return the free ip as a list
        """
        url = self.get_random_url()
        try:
            r = requests.get(url).content
            r = BeautifulSoup(r,'html.parser')
        except Exception,e:
            print e
        else:
            tbody = r.find('tbody')
            iplist = []
            for tr in tbody.find_all('tr'):
                iplist.append(tr.find('td',{'data-title':'IP'}).text)
            return iplist
