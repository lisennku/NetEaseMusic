from netease_sql import Conn
from playlist import PlayList_Spider

headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }


pls = PlayList_Spider(headers)
n = 41
while n:
    db = Conn("localhost", "root", "123456", "test")
    print 'spiderring %d page' % (42 - n)
    pageurl = 'http://music.163.com/discover/playlist/?order=hot&cat=全部& 55limit=35&offset=' + str((41-n)*35)
    pls.crawler(db, pageurl)
    n = n - 1
