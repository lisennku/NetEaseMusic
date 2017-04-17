#coding:utf-8
'''
Created on 2017/04/16
A main folder contains different auther
Author folder contains different excels for different music
@author: Lisen
'''

import requests
import json
from spider import Spider
import pyExcelerator as pyex
import os
from encrypt import Enc



class Commnet_Spider(Spider):
    """
    Commnet crawler class
    """
    def __init__(self, headers, store_dir):
        """
        Inherit and Overwrite base class's initial function
        Initialize comments spider
        @param store_dir: the main folder path 
        """
        super(Commnet_Spider,self).__init__(headers)
        if store_dir[-1] != '/':
            self.store_dir = store_dir + '/'   # ensure the path ends with '/' in case of wrong file name and file path
        else:
            self.store_dir = store_dir
        print "Initializing comments spider"
    
    
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
    
    def WriteExcel(self, info, music, music_author):
        """
        commnets will be written to excel files for different music
        @param info: object that contains information to be written to excel
        @param music: music name for the file name
        """      
        # it'a a little complex for editing existed excel file.
        # and also disk-consuming for re-opening and modifying excel 
        # use list and dict type to store the hot comments and then write them
        # to excel at a time
        print 'starting writing'
        
        file_dir = self.file_dir(music_author)
        file_name = (file_dir + music + '.xls')
        excel = pyex.Workbook()
        sheet = excel.add_sheet('comment')
        #header line
        sheet.write(0,0,'user')
        sheet.write(0,1,'likedCount')
        sheet.write(0,2,'content')
        row = 1
        for item in info:
            sheet.write(row,0,item['user'])         # write function won't overwrite existed value
            sheet.write(row,1,item['likedCount'])
            sheet.write(row,2,item['content'])
            row += 1
        excel.save(file_name) 
        print 'done'
        
     
    def crawler(self, url, music, music_author, Enc, musicid=None):
        print 'starting crawler...'
        data = {
                "params":Enc.get_params(),
                "encSecKey":Enc.get_encSecKey()                
                }
        res = requests.post(url, data = data, headers=self.headers).content
        json_text = json.loads(res)
        total = json_text['total']             # total comments for the song
        hotcomment = json_text['hotComments']  # hot comments area
        hclist = []
        for item in hotcomment:
            hcdict = {"user":'',"likedCount":'',"content":'',"time":''}
            hcdict["user"] = item['user']['nickname']    #.encode('utf-8', 'ignore')
            hcdict["likedCount"] = item['likedCount']
            hcdict['content'] = item['content']          #.encode('utf-8', 'ignore')
            hclist.append(hcdict)
        self.WriteExcel(hclist, music, music_author)
        
        

        
# if __name__ == '__main__':    
#     headers = {
#     'Cookie': 'appver=1.5.0.75771;',
#     'Referer': 'http://music.163.com/'
# }
#     store_dir = 'C:/Users/Lisen/Desktop/test'
#     # make sure to post data to the link like below
#     url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_186016/?csrf_token="     
#     first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
#     second_param = "010001"
#     third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
#     forth_param = "0CoJUm6Qyw8W8jud"
#     enc = Enc(first_param, second_param, third_param, forth_param)
#     cs = Commnet_Spider(headers, store_dir)
#     music = u'晴天'
#     music_author = u'Jay'
#     print enc.get_encSecKey()
#     print enc.get_params()
#     cs.crawler(url=url, music = music, music_author=music_author, Enc = enc)
