# NetEaseMusic
NetEase music spider
网易云音乐爬虫

## table type:

存放歌单的playlist表结构
```console
mysql> desc playlist;
$+-----------------+--------------+------+-----+-------------------+----------------+
$| Field           | Type         | Null | Key | Default           | Extra          |
$+-----------------+--------------+------+-----+-------------------+----------------+
$| id              | int(11)      | NO   | PRI | NULL              | auto_increment |
$| title           | varchar(150) | YES  |     | NULL              |                |
$| link            | varchar(150) | YES  |     | NULL              |                |
$| linkid          | varchar(150) | YES  |     | NULL              |                |
$| cnt             | varchar(150) | YES  |     | NULL              |                |
$| createuser      | varchar(150) | YES  |     | NULL              |                |
$| createdate      | varchar(150) | YES  |     | NULL              |                |
$| createuserid    | varchar(150) | YES  |     | NULL              |                |
$| inserttimestamp | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |
$+-----------------+--------------+------+-----+-------------------+----------------+
```
存放歌曲的music表结构
```console
mysql> desc music;
$+--------------+--------------+------+-----+---------+----------------+
$| Field        | Type         | Null | Key | Default | Extra          |
$+--------------+--------------+------+-----+---------+----------------+
$| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
$| musicname    | varchar(200) | YES  |     | NULL    |                |
$| musiclink    | varchar(150) | YES  |     | NULL    |                |
$| musiclinkid  | varchar(150) | YES  |     | NULL    |                |
$| musicwriter  | varchar(150) | YES  |     | NULL    |                |
$| musicalbum   | varchar(150) | YES  |     | NULL    |                |
$| musicalbumid | varchar(150) | YES  |     | NULL    |                |
$| musicdur     | varchar(150) | YES  |     | NULL    |                |
$+--------------+--------------+------+-----+---------+----------------+
```
## done: 
1. 爬取全部热门歌单
2. 爬取全部热门歌单的歌曲
3. MySQL数据库存储，并去重

## to be done:
1. 丰富异常处理
2. 歌曲热门评论爬取
3. 爬取指定类别下的歌单
4. 增加标志位，防止在采集歌曲信息时，重复请求已经采集过的歌单链接
5. 增加进度条显示

# inspired by @Chengyumeng/spider163 
# thansk netease
