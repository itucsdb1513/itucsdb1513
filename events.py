import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class event:
    def __init__(self, dsn):
        self.dsn = dsn;

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS events (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NULL)"""
            cursor.execute(query)

            query = "SELECT * FROM events"
            cursor.execute(query)
            events = cursor.fetchall()
        return render_template('upcoming_events.html', events = events)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS events"""
            cursor.execute(query)

            query = """CREATE TABLE events (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NUL)"""
            cursor.execute(query)

            query = """INSERT INTO events (date, place, player1, player2)
                        VALUES
                        ('3.November', 'Tiran', 'Ira', 'Rei'),
                        ('December', 'Istanbul', 'Javid', 'Ahmet')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('upcoming_events'))

    def addevent(self, date, place, player1, player2):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO events (date, place, player1, player2)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (date, place, player1, player2)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('upcoming_events'))


    def deleteevent(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE number = '%s' """ % (number)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('upcoming_events'))
