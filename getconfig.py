#coding:utf-8
'''
Created on 2017年4月7日

@author: Lisen
'''
import ConfigParser

#获取配置信息
cf = ConfigParser.ConfigParser()
cf.read('NetEaseMusicSpiderConf.conf')
host = cf.get('db','host')
user = cf.get('db','user')
pwd = cf.get('db','pass')
schema = cf.get('db','schema')
