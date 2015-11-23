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
            query = "SELECT * FROM localplayers"
            cursor.execute(query)
            players = cursor.fetchall()
            query = "SELECT * FROM localgames"
            cursor.execute(query)
            games = cursor.fetchall()
        return render_template('localtournaments.html', players = players, games = games)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS localgames;
                       DROP TABLE IF EXISTS localplayers;"""
            cursor.execute(query)

            query = """CREATE TABLE localplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        win integer DEFAULT 0,
                        lose integer DEFAULT 0,
                        draw integer DEFAULt 0);
                       CREATE TABLE localgames (
                        id serial PRIMARY KEY,
                        playerone integer NOT NULL references localplayers(id),
                        playertwo integer NOT NULL references localplayers(id),
                        result integer NOT NULL);"""
            cursor.execute(query)

            query = """INSERT INTO localplayers (name, surname, win, lose, draw)
                         VALUES
                          ('MUSTAFA', 'ALP', 23, 12, 4),
                          ('EKMEL', 'UYAR', 36, 2, 1),
                          ('MERT', 'BAYKARA', 10, 26, 3);
                       INSERT INTO localgames (playerone, playertwo, result)
                         VALUES
                          (1, 2, 1),
                          (2, 3, 2),
                          (1, 3, 0);"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))

    def add_player(self, name, surname, win, lose, draw):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO localplayers (name, surname, win, lose, draw)
                        VALUES
                        ('%s', '%s', %s, %s, %s)""" % (name, surname, win, lose, draw)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))
    
    def add_game(self, playerone, playertwo, result):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO localgames (playerone, playertwo, result)
                        VALUES
                        (%s, %s, %s)""" % (playerone, playertwo, result)
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

            query = """DELETE FROM localplayers WHERE id = %s """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))
    
    def delete_game(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM localgames WHERE id = %s """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))
