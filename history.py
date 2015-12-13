import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class facts:
    def __init__(self, dsn):
        self.dsn = dsn;

    def open_page(self, sort = "number"):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS history (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text ,
                        fact text NOT NULL)"""
            cursor.execute(query)

            query = """SELECT * FROM history
                         ORDER BY %s""" % sort
            cursor.execute(query)
            history = cursor.fetchall()
        return render_template('history.html', history = history)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS history"""
            cursor.execute(query)

            query = """CREATE TABLE history (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text ,
                        fact text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO history (date, place, fact)
                        VALUES
                        ('6th century AD', 'India', 'Game generated'),
                        ('15th century', 'Europe', 'Move of pieces changed'),
                        ('19th century', '..' ,'Modern tournament play began'),
                        ('1883', '..' , 'Chess clock first used'),
                        ('1886', '..', 'First world chess championship')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('history'))



    def addfact(self, date, place, fact):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO history (date, place, fact)
                        VALUES
                        ('%s', '%s', '%s')""" % (date, place, fact)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('history'))


    def deletefact(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM history WHERE number = '%s' """ % (number)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('history'))

    def delete_fact(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM history WHERE date = '%s'
                        AND place = '%s' """ % (date, place)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('history'))

    def findfact(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM history WHERE number = %s """ % (number)
            cursor.execute(query)
            history = cursor.fetchall()
        return render_template('findfact.html', history = history)

    def find_fact(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM history
                        WHERE date LIKE '%s%%'
                          AND place LIKE '%s%%'
                        ORDER BY number """ % (date, place)
            cursor.execute(query)
            history = cursor.fetchall()
        return render_template('findfact.html', history = history)

    def open_updatefact(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM history WHERE number  = %s" % (number)
            cursor.execute(query)
            fact_up = cursor.fetchone()
        return render_template('updatefact.html', fact_up = fact_up)

    def fact_update(self, number, date, place, fact):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE history
                        SET date = '%s', place = '%s',
                            fact = '%s'
                        WHERE number = %s""" % (date, place, fact, number)
            cursor.execute(query)
        return redirect(url_for('history'))

