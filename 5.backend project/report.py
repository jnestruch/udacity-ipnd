#!/usr/bin/env python2
import psycopg2

"""Return all posts from the 'database', most recent first."""
conn = psycopg2.connect("dbname=news")

cur = conn.cursor()
  	
sql_get_posts = "SELECT content,time from posts order by time desc"
 
db_query = "select articles.title,count(*) as num \
from articles,log \
where log.status like '2%' and log.path = '/article/' || articles.slug \
group by articles.title \
order by num desc limit 3;"

#cur.execute("select path,count(*) as num from log where status like '2%' group by path")
cur.execute(db_query)

DATOS = cur.fetchall()
for data in DATOS:
	print 'Article: '+data[0] + ' -- views: ' + str(data[1])

conn.close()