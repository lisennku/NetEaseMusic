import requests
from bs4 import BeautifulSoup
import json
from spider import Spider

class Music_Spider(Spider):

    music_prefix = 'http://music.163.com/song?id='
    
    def __init__(self,headers):
        super(Music_Spider,self).__init__(headers)
        print 'Initializing music spider...'
        
    def crawler(self,Conn,url):
        '''
        Main method for crawling  data from netease music web-site
        @param Conn: object of Conn class
        @param url:  netease music web-site 
        '''
        parse = BeautifulSoup(requests.get(url,self.headers).content,'html.parser')
        musicarea = json.loads(parse.find('textarea',{'style':'display:none;'}).text)
        print 'start of parsing'
        for music in musicarea:
            print 'parsing ' + music['name']
            #should use exception because some musics have missing value on album name
            #if not will cause ATTRIBUTE ERROR
            musictitle = Conn.escaping(music['name'].encode('utf-8'))
            musiclinkid = Conn.escaping(str(music['id']).encode('utf-8'))
            musiclink = Conn.escaping((Music_Spider.music_prefix+str(music['id'])).encode('utf-8'))
            musicwriter = Conn.escaping(music['artists'][0]['name'].encode('utf-8'))
            musicdur = Conn.escaping(str(music['duration']))
            albumname = Conn.escaping(music['album']['name'].encode('utf-8'))
            albumid = Conn.escaping(str(music['album']['id']).encode('utf-8'))
        
        # customize sql 
            insert_sql = "insert neteasemusic.music (musicname, musiclinkid,\
              musicwriter, musicalbum, musicalbumid, musicdur,musiclink) values \
                                              ('"+musictitle+"', '"+musiclinkid+\
         "', '"+musicwriter+"', '"+albumname+"', '"+albumid+"', '"+musicdur+"', \
                                                                 '"+musiclink+"')"
            check_sql = "select * from neteasemusic.music where musiclinkid =\
                                                        '"+ musiclinkid +"'"
            
            if not Conn.check_exist(check_sql):
                print 'inserting %s' % musictitle
                Conn.exec_sql(insert_sql)
            else:
                print "%s has already been inserted" % musictitle
        Conn.close()
        print 'end of parsing'
