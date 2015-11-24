import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Turkah:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self, sort = "id"):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM localplayers
                        ORDER BY %s""" % sort
            cursor.execute(query)
            players = cursor.fetchall()
            query = """SELECT localgames.id, CONCAT(s1.name, ' ', s1.surname),
                            CONCAT(s2.name, ' ', s2.surname) , result
                        FROM localgames, localplayers AS s1, localplayers AS s2
                        WHERE (playerone = s1.id)
                          AND (playertwo = s2.id)
                        ORDER BY localgames.id"""
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
                         draw integer DEFAULt 0,
                         UNIQUE (name, surname));
                       
                       CREATE TABLE localgames (
                         id serial PRIMARY KEY,
                         playerone integer NOT NULL references localplayers(id),
                         playertwo integer NOT NULL references localplayers(id),
                         result integer NOT NULL);"""
            cursor.execute(query)

            query = """INSERT INTO localplayers (name, surname, win, lose, draw)
                         VALUES
                          ('ISMET', 'SANCAK', 2, 1, 0),('CAN', 'MIHCIYAZGAN', 1, 1, 0),
                          ('MUSTAFA', 'YILMAZ', 1, 0, 1),('SERHAT', 'TUNCA', 0, 1, 1),
                          ('AHMET', 'SAYKAN', 1, 1, 0),('GENCAY', 'IGDIR', 1, 2, 0),
                          ('MEHMET', 'TURK', 1, 1, 0),('CEM', 'BERK', 1, 1, 0),
                          ('HASAN', 'BOLAT', 0, 1, 1),('ALPTEKIN', 'AVCI', 0, 0, 1),
                          ('GORKEM', 'AKPINAR', 1, 0, 0),('TANJU', 'SARI', 1, 1, 0),
                          ('NACI', 'ELMALI', 2, 2, 0),('CELAL', 'OZBEK', 1, 1, 0),
                          ('FARUK', 'CELIK', 1, 0, 0), ('FADIL', 'CELIK', 0, 2, 0),
                          ('SUAT', 'UGURLU', 0, 0, 1),('DENIZ', 'SIMSEK', 1, 2, 0),
                          ('HULYA', 'KONAK', 1, 1, 0),('KAZIM', 'ATAKAN', 1, 1, 0),
                          ('ERDAL', 'YILMAZER', 1, 0, 1),('AHMET', 'AYDIN', 1, 0, 0),
                          ('MUSTAFA', 'YILDIZ', 0, 2, 0),('MEHMET', 'KARACA', 1, 0, 0),
                          ('SONGUL', 'TERLEMEZ', 0, 1, 0);
                       INSERT INTO localgames (playerone, playertwo, result)
                         VALUES
                          (14, 2, 1),(3, 13, 1),(1, 25, 1),(2, 23, 1),
                          (19, 21, 2),(20, 19, 2),(8, 18, 1),(6, 1, 2),
                          (4, 10, 0),(22, 5, 1),(21, 17, 0),(16, 18, 2),
                          (13, 6, 1),(18, 20, 2),(4, 7, 2),(23, 13, 2),
                          (5, 16, 1),(24, 8, 1),(3, 9, 0),(1, 15, 2),
                          (12, 14, 1),(9, 11, 2),(6, 12, 1),(7, 13, 0);"""
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
                        (%s, %s, %s);""" % (playerone, playertwo, result)
            cursor.execute(query)
            
            if int(result) == 1:
                queryOne = """UPDATE localplayers
                            SET win = win + 1
                            WHERE id = %s;""" % playerone
                queryTwo = """UPDATE localplayers
                            SET lose = lose + 1
                            WHERE id = %s;""" % playertwo            
            elif int(result) == 2:
                queryOne = """UPDATE localplayers
                            SET win = win + 1
                            WHERE id = %s;""" % playertwo
                queryTwo = """UPDATE localplayers
                            SET lose = lose + 1
                            WHERE id = %s;""" % playerone 
            else:
                queryOne = """UPDATE localplayers
                            SET draw = draw + 1
                            WHERE id = %s;""" % playerone
                queryTwo = """UPDATE localplayers
                            SET draw = draw + 1
                            WHERE id = %s;""" % playertwo
            cursor.execute(queryOne)
            cursor.execute(queryTwo)
             
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

    def open_updatelp(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM localplayers WHERE id  = %s" % (id)
            cursor.execute(query)
            player = cursor.fetchone()
        return render_template('updatelp.html', player = player)

    def update_player(self, id, name, surname, win, lose, draw):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE localplayers
                        SET name = '%s', surname = '%s',
                            win = %s, lose = %s, draw = %s
                        WHERE id = %s""" % (name, surname, win, lose, draw, id)
            cursor.execute(query)
        return redirect(url_for('localtour_page'))

    def open_updatelg(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM localgames WHERE id  = %s" % (id)
            cursor.execute(query)
            game = cursor.fetchone()
            query = """SELECT id, name, surname
                        FROM localplayers
                        ORDER BY id"""
            cursor.execute(query)
            players = cursor.fetchall()
        return render_template('updatelg.html', game = game, players = players)

    def update_game(self, id, playerone, playertwo, result):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE localgames
                        SET playerone = %s, playertwo = %s, result = %s
                        WHERE id = %s""" % (playerone, playertwo, result, id)
            cursor.execute(query)
        return redirect(url_for('localtour_page'))

    def find_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM localplayers
                        WHERE name LIKE '%s%%'
                          AND surname LIKE '%s%%'
                        ORDER BY id """ % (name, surname)
            cursor.execute(query)
            player = cursor.fetchall()
        return render_template('findlp.html', player = player)

    def find_player_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM localplayers WHERE id = %s """ % (id)
            cursor.execute(query)
            player = cursor.fetchall()
        return render_template('findlp.html', player = player)

    def find_game_by_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT localgames.id, CONCAT(s1.name, ' ', s1.surname),
                            CONCAT(s2.name, ' ', s2.surname) , result
                        FROM localgames, localplayers AS s1, localplayers AS s2
                        WHERE (playerone = s1.id)
                          AND (playertwo = s2.id)
                          AND (localgames.id = %s)""" % (id)
            cursor.execute(query)
            game = cursor.fetchall()
        return render_template('findlg.html', game = game)

    def find_game_by_player(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT localgames.id, CONCAT(s1.name, ' ', s1.surname),
                            CONCAT(s2.name, ' ', s2.surname) , result
                        FROM localgames, localplayers AS s1, localplayers AS s2
                        WHERE (playerone = s1.id)
                          AND (playertwo = s2.id)
                          AND localgames.id = ANY (SELECT id
                                                    FROM localgames
                                                    WHERE playerone = %s
                                                       OR playertwo = %s
                                                    ORDER BY id) """ % (id, id)
            cursor.execute(query)
            game = cursor.fetchall()
        return render_template('findlg.html', game = game)
