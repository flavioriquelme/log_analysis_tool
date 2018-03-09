#!/usr/bin/env python3

""" DB Log Analysis Tool Project for Udacity Full Stack Nanodegree

This log analysis tool written in python connects to a PostgreSQL
database to collect data for analysis.

How to run this DB Log Analysis Tool:
$ python loganalysis.py

"""
import datetime
import psycopg2


def db_connect(db_name="news"):
    # Connect to the Database
    try:
        db = psycopg2.connect("dbname={}".format(db_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Problems to connect to DB")


def now():
    # Return current timestamp
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def report_one(cursor):
    """report_one() collects data from DB to answer the question:
       1. What are the most popular three articles of all time?
    """
    cursor.execute("SELECT a.title, count(l.id) AS PAGE_VIEWS \
                     FROM articles a, log l \
                    WHERE substring(l.path, 10) = a.slug \
                    GROUP BY a.title \
                    ORDER BY PAGE_VIEWS DESC \
                    LIMIT 3;")
    return cursor.fetchall()


def report_two(cursor):
    """report_two() collects data from DB to answer the question:
       2. Who are the most popular article authors of all time?
    """
    cursor.execute("SELECT au.name, count(l.id) AS PAGE_VIEWS \
                      FROM authors au, articles a, log l \
                     WHERE au.id = a.author \
                       AND substring(l.path, 10) = a.slug \
                     GROUP BY au.name \
                     ORDER BY PAGE_VIEWS DESC;")
    return cursor.fetchall()


def report_three(cursor):
    """report_three() collects data from DB to answer the question:
       3. On which days did more than 1% of requests lead to errors?
    """
    cursor.execute("SELECT e.date, e.errors, v.views \
                     FROM date_errors e, date_views v \
                    WHERE e.date = v.date \
                      AND e.errors > (0.01 * v.views);")
    return cursor.fetchall()


def generate_report(cursor):
    """Create output report."""
    filename = "log_analysis_report_%s" %\
               datetime.datetime.now().\
               strftime("%Y-%m-%d")

    with open(filename, 'w') as f:
        # Report Header with timestamp
        f.write("Log Analysis Report generated on: " + now() + "\n\n")

        # Report number one
        f.write("== Most popular three articles of all time ==\n")
        i = 0
        for row in report_one(cursor):
            i += 1
            f.write("%s) \"%s\", with %s page views." %
                    (i, str(row[0]), str(row[1])))
            f.write("\n")
        f.write("\n")

        # Report number two
        f.write("== Most popular article authors of all time ==\n")
        i = 0
        for row in report_two(cursor):
            i += 1
            f.write("%s) %s, with %s page views." %
                    (i, str(row[0]), str(row[1])))
            f.write("\n")
        f.write("\n")

        # Report number three
        f.write("== Days with more than 1% of HTTP request errors ==\n")
        i = 0
        for row in report_three(cursor):
            i += 1
            f.write("%s) %s, with %s HTTP request errors," %
                    (i, str(row[0]), str(row[1])))
            f.write(" out of %s total requests.\n" % str(row[2]))

        # Report trailer
        f.write("\nEnd of Report")
        f.close()


if __name__ == '__main__':
    """Main loganalysis_db.py was called"""
    print "Log Analysis Tool Started at " + now()
    db, cursor = db_connect()
    print "Generating Report..."
    generate_report(cursor)
    db.close()
    print "Log Analysis Tool Finished at " + now()
