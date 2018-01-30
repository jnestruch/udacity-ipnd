#!/usr/bin/env python2
import psycopg2


def DB_connect():
    """
    """
    db = psycopg2.connect(database=DBNAME)

    return db


def DB_get_data(conn, query):
    """
    """
    cur = conn.cursor()

    cur.execute(query)

    DATA = cur.fetchall()

    cur.close()

    return DATA


def show_articles(db_connection):
    """
    """
    db_query = '''
      SELECT articles.title,count(*) AS num
      FROM articles,log
      WHERE log.status like '2%' AND
        log.path = '/article/' || articles.slug
      GROUP BY articles.title
      ORDER BY num DESC LIMIT 3;
    '''

    db_result = DB_get_data(db_connection, db_query)

    print '- What are the most popular three articles of all time?\n'

    if db_result == []:
        print 'Ups. Query returned no results'

    for data in db_result:
        print data[0] + ' -- ' + str(data[1]) + ' views'

    print '\n'


def show_authors(db_connection):
    """
    """
    db_query = '''
      SELECT authors.name,count(*) AS num
      FROM articles,log,authors
      WHERE log.status LIKE '2%' AND
        log.path = '/article/' || articles.slug AND
        articles.author = authors.id
      GROUP BY authors.name
      ORDER BY num DESC;
      '''

    db_result = DB_get_data(db_connection, db_query)

    print '- Who are the most popular article authors of all time?\n'

    if db_result == []:
        print 'Ups. Query returned no results'

    for data in db_result:
        print data[0] + ' -- ' + str(data[1]) + ' views'

    print '\n'


def show_days_errors(db_connection):
    """
    """
    db_query = '''
      SELECT date(time),
           ROUND(count(status) filter
             (WHERE status LIKE '4%') / count(*)::dec*100,1)
      FROM log
      GROUP BY date(time)
      HAVING count(status) filter
        (WHERE status LIKE '4%' OR status LIKE '5%') /
          count(*)::dec > 0.01;
    '''

    db_result = DB_get_data(db_connection, db_query)

    print '- On which days did more than 1% of requests lead to errors?\n'
    if db_result == []:
        print 'Ups. Query returned no results'

    for data in db_result:
        print data[0].strftime('%B %d, %Y') + ' - ' + str(data[1]) + '% errors'

    print '\n'


"""
"""
DBNAME = "news"

db_connection = DB_connect()

show_articles(db_connection)

show_authors(db_connection)

show_days_errors(db_connection)

db_connection.close()
