import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Turkah:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS localplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        win integer DEFAULT 0,
                        lose integer DEFAULT 0)"""
            cursor.execute(query)

            query = "SELECT * FROM localplayers"
            cursor.execute(query)
            players = cursor.fetchall()
        return render_template('localtournaments.html', players = players)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS localplayers"""
            cursor.execute(query)

            query = """CREATE TABLE localplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        win integer DEFAULT 0,
                        lose integer DEFAULT 0)"""
            cursor.execute(query)

            query = """INSERT INTO localplayers (name, surname, win, lose)
                        VALUES
                        ('MUSTAFA', 'ALP', 3, 1),
                        ('EKMEL', 'UYAR', 2, 2),
                        ('MERT', 'BAYKARA', 1, 3)"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))

    def add_player(self, name, surname, win, lose):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO localplayers (name, surname, win, lose)
                        VALUES
                        ('%s', '%s', %s, %s)""" % (name, surname, win, lose)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))

    def delete_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM localplayers WHERE name = '%s'
                        AND surname = '%s' """ % (name, surname)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))

    def delete_player_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM localplayers WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))
