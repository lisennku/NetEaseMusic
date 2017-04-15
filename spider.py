#encoding:utf-8
'''
Created on 2017/04/14

@author: Lisen
'''
class Spider(object):
    """
    Class spider is a base class for being inherited
    ATTR: headers:  HTTP requests component
    FUNC: playlist spider:  to crawler playlist info from main entrance for playlist url
          music spider:     to crawler music info from specific playlist url
          comment spider:   to crawler comment from music url
    """
    def __init__(self, headers):
        self.headers = headers
    
    def playlist_crawler(self):
        pass
    
    def music_crawler(self):
        pass
    
    def comment_crawler(self):
        pass
