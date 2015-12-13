import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class event:
    def __init__(self, dsn):
        self.dsn = dsn;
        return

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()


            query = """CREATE TABLE IF NOT EXISTS tours (
                        number serial PRIMARY KEY,
                        cha text UNIQUE NOT NULL,
                        year integer NOT NULL,
                        players integer NOT NULL,
                        games integer NOT NULL)"""
            cursor.execute(query)


            query = """SELECT * FROM tours"""
            cursor.execute(query)
            tours = cursor.fetchall()


            query = """CREATE TABLE IF NOT EXISTS events (
                        number serial PRIMARY KEY,
                        date text UNIQUE NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NULL,
                        champ text NOT NULL)"""
            cursor.execute(query)

            query = """SELECT * FROM events"""
            cursor.execute(query)
            events = cursor.fetchall()

        return render_template('upcoming_events.html', events = events, tours = tours)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS events"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS tours """
            cursor.execute(query)

            query = """CREATE TABLE tours (
                        number serial PRIMARY KEY,
                        cha  text UNIQUE NOT NULL,
                        year integer NOT NULL,
                        players integer NOT NULL,
                        games integer NOT NULL)"""
            cursor.execute(query)

            query = """ CREATE TABLE events (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NULL,
                        champ text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO tours (cha, year, players, games)
                        VALUES
                        ('World', 2016, 24, 72),
                        ('European', 2017, 16, 36),
                        ('Asian', 2016, 16, 36),
                        ('Albanian', 2016, 16, 36),
                        ('Turkish', 2016, 16, 36)"""
            cursor.execute(query)

            query = """INSERT INTO events (date, place, player1, player2, champ)
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
            upevent = cursor.fetchone()
        return render_template('updateeventpage.html', upevent = upevent)


    def open_updatetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tours WHERE number  = %s" % (number)
            cursor.execute(query)
            tour_up = cursor.fetchone()
        return render_template('updatetour.html', tour_up = tour_up)


    def addevent(self, date, place, player1, player2, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO events (date, place, player1, player2, champ)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s')""" % (date, place, player1, player2, champ)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))

    def addtour(self, cha, year, players, games):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO tours (cha, year, players, games)
                        VALUES
                        ('%s', %s, %s, %s)""" % (cha, year, players, games)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))


    def deleteevent(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE number = '%s' """ % (number)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('upcoming_events'))

    def deleteevent_2(self, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE champ = '%s' """ % (champ)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('upcoming_events'))

    def deletetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM tours WHERE number = '%s' """ % (number)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))

    def delete_event(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE date = '%s'
                        AND place = '%s' """ % (date, place)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('upcoming_events'))

    def delete_tour(self, cha):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM tours WHERE cha = '%s'
                         """ % (cha)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))

    def update_event(self, number, date, place, player1, player2, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE events
                        SET date = '%s', place = '%s', player1 = '%s',
                            player2 = '%s' ,champ = '%s'
                        WHERE number = %s""" % (date, place, player1, player2, champ, number)
            cursor.execute(query)

            query = "SELECT date, place, player1, player2, champ FROM events"
            cursor.execute(query)
            event = cursor.fetchall()

            query = "SELECT cha, year, players, games FROM tours"
            cursor.execute(query)
            tours = cursor.fetchall()

            cursor.close()
        return redirect(url_for('upcoming_events'), event=event, tours=tours)


    def tour_update(self, number, cha, year, players, games):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE tours
                        SET cha = '%s', year = %s,
                            players = %s, games = %s
                        WHERE number = %s """ % (cha, year, players, games, number)
            cursor.execute(query)

            query = "SELECT cha, year, players, games FROM tours"
            cursor.execute(query)
            tours = cursor.fetchall()

            query = "SELECT date, place, player1, player2, champ FROM events"
            cursor.execute(query)
            event = cursor.fetchall()

            cursor.close()
        return redirect(url_for('upcoming_events'), tours = tours, event = event)

    def find_event(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events WHERE number = %s """ % (number)
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
        return render_template('findevent.html', events = events)

    def find_event_2(self, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events WHERE champ LIKE '%s%%' """ % (champ)
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
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
            cursor.close()
        return render_template('findevent.html', events = events)

    def find_tour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM tours WHERE number = %s """ % (number)
            cursor.execute(query)
            tours = cursor.fetchall()
            cursor.close()
        return render_template('find_tour.html', tours = tours)

    def find_tour_name(self, cha):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM tours
                        WHERE cha LIKE '%s%%'
                        ORDER BY number """ % (cha)
            cursor.execute(query)
            tours = cursor.fetchall()
            cursor.close()
        return render_template('find_tour.html', tours = tours)