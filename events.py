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
                        player2 text NOT NULL,
                        championship text NOT NULL)"""
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
                        player2 text NOT NULL,
                        championship text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO events (date, place, player1, player2, championship)
                        VALUES
                        ('3.November', 'Tiran', 'Ira', 'Rei', 'Albanian'),
                        ('4.December', 'Istanbul', 'Javid', 'Ahmet', 'Turkish'),
                        ('10.December', 'Ankara', 'Mursit', 'Soner', 'European'),
                        ('15.December', 'Istanbul', 'Mehmet', 'Elif', 'World')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('upcoming_events'))



    def open_updateevent(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM events WHERE number  = %s" % (number)
            cursor.execute(query)
            event_up = cursor.fetchone()
        return render_template('update_event.html', event_up = event_up)

    def addevent(self, date, place, player1, player2, championship):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO events (date, place, player1, player2, championship)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s')""" % (date, place, player1, player2, championship)
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

    def delete_event(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE date = '%s'
                        AND place = '%s' """ % (date, place)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('upcoming_events'))

    def update_event(self, number, date, place, player1, player2, championship):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE events
                        SET date = '%s', place = '%s',
                            player1 = '%s', player2 = '%s', championship = '%s'
                        WHERE number = %s""" % (date, place, player1, player2, championship, number)
            cursor.execute(query)
        return redirect(url_for('upcoming_events'))

    def find_event(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events WHERE number = %s """ % (number)
            cursor.execute(query)
            events = cursor.fetchall()
        return render_template('findevent.html', events = events)

    def find_event_name(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM events
                        WHERE date LIKE '%s%%'
                          AND place LIKE '%s%%'
                        ORDER BY number """ % (date, place)
            cursor.execute(query)
            events = cursor.fetchall()
        return render_template('findevent.html', events = events)





