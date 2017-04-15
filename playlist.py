#encoding:utf-8
'''
Created on 2017年4月12日
@author: Lisen
--------change date 2017/04/15-----------
change to OOP method
-----------------------------------------
'''

from bs4 import BeautifulSoup       
import requests 
from spider import Spider   

class PlayList_Spider(Spider):
    
    playlist_prefix = 'http://music.163.com'
    
    def __init__(self, headers):
        """
        Inherit and Overwrite base class's initial function
        Initialize Playlist Spider 
        """
        super(PlayList_Spider,self).__init__(headers)
        print "initializing PlayList Spider"
    
    
    def crawler(self,Conn,url):
        """
        Main method for crawling  data from netease music web-site
        @param Conn: object of Conn class
        @param url:  netease hot playlist main entrance  
        """
        try:
            parse = BeautifulSoup((requests.get(url,self.headers).content),"html.parser")
        except requests.exceptions.ConnectionError:
            print 'ConnectionError'
        except requests.exceptions.InvalidURL:
            ValueError = True
            print 'InvalidURL'
        except requests.exceptions.InvalidSchema:
            ValueError =True
            print 'InvalidSchema'
        else:
            print 'start of parsing'
            playlist_area = parse.find('ul', {'class':'m-cvrlst f-cb'})
            for each in playlist_area.find_all('li'):
                '''
            Title/Link/LinkId exists in <a class = msk>
            CreateUser/CreateUserId exists in <a class = nm nm-icn f-thide s-fc3>
            PlayCount/CreateDate exists in playlist's url at <span class = nb>
                '''
                title = Conn.escaping(each.find('a',{'class':'msk'})['title'].encode('utf-8'))
        #playlist_prefix is a class attribute. calling as cls.attr 
                link = Conn.escaping(PlayList_Spider.playlist_prefix + each.find('a',{'class':'msk'})['href'].encode('utf-8'))
                linkid = Conn.escaping(each.find('a',{'class':'msk'})['href'][13:])
                createuser = Conn.escaping(each.find('a',{'class':'nm nm-icn f-thide s-fc3'})['title'].encode('utf-8'))
                createuserid = Conn.escaping(each.find('a',{'class':'nm nm-icn f-thide s-fc3'})['href'][14:])

        # parsing playlist url to fetch cnt and createdate 
                parse2 = BeautifulSoup(requests.get(link,self.headers).content,'html.parser')
                cnt = Conn.escaping(parse2.find('strong',{'id':'play-count','class':'s-fc6'}).text.encode('utf-8'))
                createdate = Conn.escaping(parse2.find('span',{'class':'time s-fc4'}).text[0:10])
        
        # check duplication first and then insert into database
                check_sql = "select * from neteasemusic.playlist where linkid =\
                                                                     '"+linkid+"' "
                
                insert_sql = "insert into neteasemusic.playlist (title, link,linkid,\
                             createuser, createuserid,createdate,cnt) values ('" + title +"', \
                             '"+ link +"','"+ linkid +"','"+ createuser +"', \
                             '"+ createuserid +"','"+createdate+"','"+cnt+"')"
                
                if not Conn.check_exist(check_sql):
                    print 'inserting now ' + title
                    Conn.exec_sql(insert_sql)
                else:
                    print title + " already in database"
            Conn.close()
            print 'end of parsing'
