#coding:utf-8
'''
Created on 2017/04/16
A main folder contains different auther
Author folder contains different excels for different music
@author: Lisen
--------------changed on 20170417--------
Modify crawler function 
Add escaping function
-----------------------------------------
--------------changed on 20170417--------
Add proxy ip
Add parse timestamp
-----------------------------------------
'''

import requests
import json
from spider import Spider
import pyExcelerator as pyex
import os
from encrypt import Enc
from netease_sql import Conn
import time
import random
from proxyip import Proxy_IP

class Commnet_Spider(Spider):
    """
    Commnet crawler class
    """
    def __init__(self, headers, store_dir, iplist):
        """
        Inherit and Overwrite base class's initial function
        Initialize comments spider
        @param store_dir: the main folder path 
        """
        super(Commnet_Spider,self).__init__(headers)
        self.ip = iplist
        if store_dir[-1] != '/':
            self.store_dir = store_dir + '/'   # ensure the path ends with '/' in case of wrong file name and file path
        else:
            self.store_dir = store_dir
        print "Initializing comments spider"
    
    def parse_timestapm(self, timestamp):
        """
        parse timestamp
        @param timestamp: comment date & time 
        """
        timestamp = timestamp / 1000
        time_array = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return dt        
    
    def file_dir(self, music_author):
        """
        examine the file and file path
        @param music_author: the auther for music 
        """
        file_dir = self.store_dir + music_author + '/'
        
        if os.path.exists(file_dir):   # if file not exists
            return file_dir
        else:
            os.makedirs(file_dir)
            return file_dir
    
    def escaping(self,strs):
        """
        some characters are illegal in the name of folders
        this function will exclude the illegal charachter in the file path or name
        @param strs: strings to be disposed for excluding illegal characters
        """
        
        illegal_char = ['/','\\','\"','\'',':','?','<','?','|','*']
        for char in illegal_char:
            if char in strs:
                strs = strs.replace(char,'')
        return strs
    
        
    def WriteExcel(self, info, music, music_author):
        """
        commnets will be written to excel files for different music
        @param info: object that contains information to be written to excel
        @param music: music name for the file name
        @param music_author: author name for making sub-folders
        """      
        # it'a a little complex for editing existed excel file.
        # and also disk-consuming for re-opening and modifying excel 
        # use list and dict type to store the hot comments and then write them
        # to excel at a time
        print 'starting writing %s' %music
        
        file_dir = self.file_dir(music_author)
        file_name = (file_dir + music + '.xls')
        excel = pyex.Workbook()
        sheet = excel.add_sheet('comment')
        #header line
        sheet.write(0,0,'user')
        sheet.write(0,1,'time')
        sheet.write(0,2,'likedCount')
        sheet.write(0,3,'content')
        row = 1
        for item in info:
            sheet.write(row,0,item['user'])         # write function won't overwrite existed value
            sheet.write(row,1,item['likedCount'])
            sheet.write(row,2,item['content'])
            sheet.write(row,3,item['time'])
            row += 1
        excel.save(file_name) 
        print 'finish writing'
     
    def crawler(self, url, music, music_author, Enc, musicid=None):
        print 'starting crawler...'
        data = {
                "params":Enc.get_params(),
                "encSecKey":Enc.get_encSecKey()                
                }
        try:
            r = requests.post(url, data = data, headers=self.headers, proxies=random.choice(self.ip))
        except Exception,e:
            print e
        else:
            if r.status_code != 200:
                print 'Status code is %d '  % r.status_code
            else:
                res = r.content
                json_text = json.loads(res)
    #             total = json_text['total']             # total comments for the song
                hotcomment = json_text['hotComments']  # hot comments area
                if len(hotcomment) == 0:
                    print 'No Hot Comments for %s !' % music
                else:
                    hclist = []
                    for item in hotcomment:
                        hcdict = {"user":'',"likedCount":'',"content":'',"time":''}
                        hcdict["user"] = item['user']['nickname']    #.encode('utf-8', 'ignore')
                        hcdict["likedCount"] = item['likedCount']
                        hcdict['content'] = item['content']          #.encode('utf-8', 'ignore')
                        hcdict['time'] = self.parse_timestapm(item['time'])
                        hclist.append(hcdict)
                    self.WriteExcel(hclist, music, music_author)
                    print 'finish crawling'
