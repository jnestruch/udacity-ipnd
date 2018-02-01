#!/usr/bin/env python2
import psycopg2


def DB_connect():
    """ Function DB_connect

    Connects to the database returning a connection object.

    Input:
    Output:
        db --> Connection object
    """
    db = psycopg2.connect(database=DBNAME)

    return db


def DB_get_data(conn, query):
    """ Function DB_get_data

    Function to retrieve information from the database. Creates a cursor
    to be used to access the DB and closes it after being used.

    Input:
        conn --> Connection object
        query --> Query to be executed on the database
    Output:
        DATA --> List with the data returned from the Database
    """

    # Cursor creation
    cur = conn.cursor()

    # Get data from DB and close the cursor object
    cur.execute(query)

    DATA = cur.fetchall()

    cur.close()

    return DATA


def show_articles(db_connection):
    """ Function show_articles

    Code to get the most popular three articles of all time. It also
    shows the result on the terminal like plain text.

    Input:
        db_connection --> Connection object to fetch the data from DB
    """

    # Query definition to fetch the data from the DB
    db_query = '''
      SELECT articles.title,count(*) AS num
      FROM articles,log
      WHERE log.status like '2%' AND
        log.path = '/article/' || articles.slug
      GROUP BY articles.title
      ORDER BY num DESC LIMIT 3;
    '''

    # Executes the query on the DB returning the data
    db_result = DB_get_data(db_connection, db_query)

    # Shows the results on the screen as plain text (terminal)
    print '\n- What are the most popular three articles of all time?\n'
    if db_result == []:
        print 'Ups. Query returned no results'

    for data in db_result:
        print data[0] + ' -- ' + str(data[1]) + ' views'


def show_authors(db_connection):
    """ Function show_authors

    Code to get the most popular article authors of all time. Shows the
    result on the terminal as plain text.

    Input:
        db_connection --> Connection object to fetch the data from DB
    """

    # Query definition to fetch the data from the DB
    db_query = '''
      SELECT authors.name,count(*) AS num
      FROM articles,log,authors
      WHERE log.status LIKE '2%' AND
        log.path = '/article/' || articles.slug AND
        articles.author = authors.id
      GROUP BY authors.name
      ORDER BY num DESC;
      '''

    # Executes the query on the DB returning the data
    db_result = DB_get_data(db_connection, db_query)

    # Shows the results on the screen as plain text (terminal)
    print '\n- Who are the most popular article authors of all time?\n'
    if db_result == []:
        print 'Ups. Query returned no results'

    for data in db_result:
        print data[0] + ' -- ' + str(data[1]) + ' views'


def show_days_errors(db_connection):
    """ Function show_days_error

    Code to get the information on erroneous requests on a daily basis,
    showing only those with more than 1% of errors.

    Input:
        db_connection --> Connection object to fetch the data from DB
    """

    # Query definition to fetch the data from the DB
    db_query = '''
      SELECT time::date AS day,
          ROUND(count(status) filter
            (WHERE status LIKE '4%' OR status LIKE '5%') / count(*)::dec*100,1)
      FROM log
      GROUP BY day
      HAVING count(status) filter
        (WHERE status LIKE '4%' OR status LIKE '5%') /
          count(*)::dec > 0.01;
    '''

    # Executes the query on the DB returning the data
    db_result = DB_get_data(db_connection, db_query)

    # Shows the results on the screen as plain text (terminal)
    print '\n- On which days did more than 1% of requests lead to errors?\n'
    if db_result == []:
        print 'Ups. Query returned no results'

    for data in db_result:
        print data[0].strftime('%B %d, %Y') + ' - ' + str(data[1]) + '% errors'


# Main program

# Define the DB that will be used
DBNAME = "news"

# Get a connection object from DB
db_connection = DB_connect()

# Gets and process the information to answer the first question:
# - What are the most popular three articles of all time ?
show_articles(db_connection)

# Gets and process the information to answer the second question:
# - Who are the most popular article authors of all time ?
show_authors(db_connection)

# Gets and process the information to answer the third question:
# - On which days did more than 1% of requests lead to errors ?
show_days_errors(db_connection)

# Close the connection
db_connection.close()
