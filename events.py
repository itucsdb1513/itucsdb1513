import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class event:
    def __init__(self, dsn):
        self.dsn = dsn;

    def open_page(self, sort = "number"):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS events (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NULL,
                        champ text NOT NULL)"""
            cursor.execute(query)

            query = "SELECT * FROM events"
            cursor.execute(query)
            events = cursor.fetchall()

            query = """CREATE TABLE IF NOT EXISTS tours (
                        number serial PRIMARY KEY,
                        cha text NOT NULL,
                        year integer NOT NULL,
                        players integer NOT NULL,
                        games integer NOT NULL)"""
            cursor.execute(query)

            query = "SELECT * FROM tours"
            cursor.execute(query)
            tours = cursor.fetchall()
        return render_template('upcoming_events.html', events = events, tours = tours)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS events;
                       DROP TABLE IF EXISTS tours"""
            cursor.execute(query)

            query = """CREATE TABLE events (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NULL,
                        champ text NOT NULL,
                        UNIQUE (player1, player2));

                        CREATE TABLE tours (
                        number serial PRIMARY KEY,
                        cha text NOT NULL,
                        year integer NOT NULL,
                        players integer NOT NULL,
                        games integer NOT NULL);"""
            cursor.execute(query)

            query = """INSERT INTO events (date, place, player1, player2, champ)
                        VALUES
                        ('3.November', 'Tiran', 'Ira', 'Rei', 'Albanian'),
                        ('4.December', 'Istanbul', 'Javid', 'Ahmet', 'Turkish'),
                        ('10.December', 'Ankara', 'Mursit', 'Soner', 'European'),
                        ('15.December', 'Istanbul', 'Mehmet', 'Elif', 'World');

                        INSERT INTO tours (cha, year, players, games)
                        VALUES
                        ('World', 2016, 24, 72),
                        ('European', 2017, 16, 36),
                        ('Asian', 2016, 16, 36);"""
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

    def open_updatetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tours WHERE number  = %s" % (number)
            cursor.execute(query)
            tour_up = cursor.fetchone()
        return render_template('update_event.html', tour_up = tour_up)

    def addevent(self, date, place, player1, player2, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO events (date, place, player1, player2, champ)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s')""" % (date, place, player1, player2, champ)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('upcoming_events'))

    def addetour(self, cha, year, players, games):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO tours (cha, year, players, games)
                        VALUES
                        ('%s', %s, %s, %s)""" % (cha, year, players, games)
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

    def deletetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM tours WHERE number = '%s' """ % (number)
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

    def delete_tour(self, cha, year):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM tours WHERE cha = '%s'
                        AND year = %s """ % (cha, year)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('upcoming_events'))

    def update_event(self, number, date, place, player1, player2, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE events
                        SET date = '%s', place = '%s',
                            player1 = '%s', player2 = '%s', champ = '%s'
                        WHERE number = %s""" % (date, place, player1, player2, champ, number)
            cursor.execute(query)
        return redirect(url_for('upcoming_events'))

    def update_tour(self, number, cha, year, players, games):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE tours
                        SET cha = '%s', year = %s,
                            player = %s, games = %s
                        WHERE number = %s""" % (cha, year, players, games, number)
            cursor.execute(query)
        return redirect(url_for('upcoming_events'))

    def find_event(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events WHERE number = %s """ % (number)
            cursor.execute(query)
            events = cursor.fetchall()
        return render_template('findevent.html', events = events)

    def find_tour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM tours WHERE number = %s """ % (number)
            cursor.execute(query)
            tours = cursor.fetchall()
        return render_template('findtour.html', tours = tours)

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

    def find_tour_name(self, cha, date):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM tours
                        WHERE cha LIKE '%s%%'
                          AND year =% s
                        ORDER BY number """ % (cha, year)
            cursor.execute(query)
            tours = cursor.fetchall()
        return render_template('findtour.html', tours = tours)





