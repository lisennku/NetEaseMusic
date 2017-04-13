#encoding:utf-8
'''
Created on 2017年4月12日
@author: Lisen
歌单爬虫入口：http://music.163.com/discover/playlist/?order=hot&cat=全部limit=35&offset=0
offset作为分页偏移量 offset = (page_num - 1) * 35

'''
from bs4 import BeautifulSoup
import getconfig         
import requests
import netease_sql        



headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

playlist_prefix = 'http://music.163.com'


def playlist_spider(page_url):
    global headers
    '''
    爬取歌单信息
  Title/Link/CreateTime/CreateUser/PlayCount
  每页中歌单信息在<div class = u-cover u-cover-1>中
  Title/Link在<a class = msk>
  CreateUser在<a class = nm nm-icn f-thide s-fc3>
  PlayCount在<span class = nb>在具体歌单的页面查找
  CreateTime在具体歌单的页面查找
  @param playlist_url: the url for the website to be spiderred   
    '''
    try:
        html_content = requests.get(page_url,headers=headers).content
#         print html_content
        bs_body = BeautifulSoup(html_content,"html.parser")
#         print bs_body
        playlist_area = bs_body.find('ul', {'class':'m-cvrlst f-cb'})
        for each_playlist in playlist_area.find_all('li'):
            print 'parsing now'
            # MySQLdb.escape_string 转义字符串，使之能安全的存入MySQL数据库
            title = netease_sql.esccape_str(each_playlist.find('a',{'class':'msk'})['title'].encode('utf-8'))
            
            link = netease_sql.esccape_str(playlist_prefix + each_playlist.find('a',{'class':'msk'})['href'].encode('utf-8'))
            
            linkid = netease_sql.esccape_str(each_playlist.find('a',{'class':'msk'})['href'][13:])
            
            createuser = netease_sql.esccape_str(each_playlist.find('a',{'class':'nm nm-icn f-thide s-fc3'})['title'].encode('utf-8'))
            
            createuserid = netease_sql.esccape_str(each_playlist.find('a',{'class':'nm nm-icn f-thide s-fc3'})['href'][14:])
            
            #爬取具体歌单页，获取创建日期和播放数量
            pl_list_cont = requests.get(link, headers).content
            cnt_body = BeautifulSoup(pl_list_cont,'html.parser')
            
            cnt = netease_sql.esccape_str(cnt_body.find('strong',{'id':'play-count','class':'s-fc6'}).text.encode('utf-8'))
            
            createdate = netease_sql.esccape_str(cnt_body.find('span',{'class':'time s-fc4'}).text[0:10])
            insert_sql = "insert into neteasemusic.playlist (title, link,linkid,\
             createuser, createuserid,createdate,cnt) values ('" + title +"', \
             '"+ link +"','"+ linkid +"','"+ createuser +"', \
             '"+ createuserid +"','"+createdate+"','"+cnt+"')"
            check_sql  = "select * from neteasemusic.playlist where linkid = '"+linkid+"' "
            if not netease_sql.check_exist(check_sql):
                print 'executing insert ' + title
                netease_sql.execute_sql(insert_sql)  
            else:
                print '%s already in database' %title
    except Exception,e:
        print e

if __name__ == '__main__':
    n = 41
    while n:
        print 'spiderring %d page' % n
        pageurl = 'http://music.163.com/discover/playlist/?order=hot&cat=全部limit=35&offset=' + str((41-n)*35)
        playlist_spider(pageurl)
        n = n - 1
    print 'done'
    netease_sql.close()
