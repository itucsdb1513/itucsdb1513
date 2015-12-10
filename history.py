import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class facts:
    def __init__(self, dsn):
        self.dsn = dsn;

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS history (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text ,
                        fact text NOT NULL)"""
            cursor.execute(query)

            query = "SELECT * FROM history"
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
                        ('19th century', ,'Modern tournament play began'),
                        ('1883', , 'Chess clock first used'),
                        ('1886', , 'First world chess championship')"""
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

    def updatefact(self, date, place, fact):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE history
                        SET date = '%s', place = '%s',
                            fact = %s
                        WHERE id = %s""" % (date, place, fact)

            cursor.execute(query)
            connection.commit()