#!/usr/bin/env

# psycopg2 is a database module.
import psycopg2
import time


# Connection to database news
def connect(database_name="news"):
    """Connect to the PostgreSQL database. Returns a database connection """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except ConnectionError:
        print("Unable to connect to the database")


def popular_article():
    db, cursor = connect()
    popular_articles = '''
    select title, views from view_popular_articles limit 3
    '''
    # executes the psql statement.
    cursor.execute(popular_articles)
    print("Most popular articles:")
    for (title, count) in cursor.fetchall():
        print("    {} - {} views".format(title, count))


def popular_authors():
    db, cursor = connect()
    query = "select * from view_popular_authors"
    cursor.execute(query)
    print("Most popular authors:")
    # fetches all the results from psql statement.
    results = cursor.fetchall()
    for i in range(len(results)):
        name = results[i][0]
        views = results[i][1]
        print("    %s - %d views " % (name, views))


def error_percent():
    db, cursor = connect()
    query = "select to_char(date,'Mon,DD,YYYY') as date,err_p from view_err\
     where err_p>1.0"
    cursor.execute(query)
    print("Days with more than 1% errors:")
    results = cursor.fetchall()
    for i in range(len(results)):
        date = results[i][0]
        err_prc = results[i][1]
        print("    %s - %.1f%% errors " % (date, err_prc))


if __name__ == "__main__":
    # prints the answer for what are the most popular 3 articles.
    popular_article()
    # after every answer a line is printed
    print('-' * 70)
    # prints the answer for what are the most popular article authors.
    popular_authors()
    print('-' * 70)
    # prints days with more than 1% errors.
    error_percent()
