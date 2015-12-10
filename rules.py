import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Rules:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self, sort = "id"):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM pieces
                        ORDER BY %s""" % sort
            cursor.execute(query)
            rules = cursor.fetchall()

            query = """SELECT * FROM rules_items
                        ORDER BY %s""" % sort
            cursor.execute(query)
            the_rules = cursor.fetchall()

            query = """SELECT * FROM piece_captures
                        ORDER BY %s""" % sort
            cursor.execute(query)
            capture = cursor.fetchall()

        return render_template('rules.html', rules = rules, the_rules=the_rules, capture=capture)

    def open_updatepieces(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM pieces WHERE id  = %s" % (id)
            cursor.execute(query)
            the_pieces = cursor.fetchone()
        return render_template('updatepiecespage.html', the_pieces = the_pieces)

    def open_updaterules(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM rules_items WHERE id  = %s" % (id)
            cursor.execute(query)
            uprules = cursor.fetchone()
        return render_template('updaterulespage.html', uprules = uprules)

    def open_updatecaptures(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM piece_captures WHERE id  = %s" % (id)
            cursor.execute(query)
            upcaptures = cursor.fetchone()
        return render_template('updatecapturespage.html', upcaptures = upcaptures)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS pieces;
                       DROP TABLE IF EXISTS rules_items;
                       DROP TABLE IF EXISTS piece_captures"""
            cursor.execute(query)

            query = """CREATE TABLE pieces (
                        id serial PRIMARY KEY,
                        piece_name text UNIQUE NOT NULL,
                        piece_move text NOT NULL,
                        special_move text);

                       CREATE TABLE rules_items (
                        id serial PRIMARY KEY,
                        the_rule text UNIQUE NOT NULL,
                        made_by text NOT NULL,
                        date text NOT NULL);

                       CREATE TABLE piece_captures (
                        id serial PRIMARY KEY,
                        name text NOT NULL REFERENCES pieces(piece_name),
                        capture_direction text NOT NULL,
                        starting_place text NOT NULL,
                        can_start text NOT NULL);"""
            cursor.execute(query)

            query = """INSERT INTO pieces (piece_name, piece_move, special_move)
                        VALUES
                        ('King', 'H,V,D', 'Castling'),
                        ('Rook', 'H,V', 'Castling'),
                        ('Bishop', 'D', ' '),
                        ('Knight', 'L', ' '),
                        ('Pawn', 'S.F. ,D', 'en Passant'),
                        ('Queen', 'H, V, D', ' ');

                        INSERT INTO rules_items (the_rule, made_by, date)
                        VALUES
                        ('Queen, Bishop', 'Hooper&Whyld', '15th century'),
                        ('Time limit', 'Sunnuck', '1861'),
                        ('Queen', 'Jacob Sarrart', '1828'),
                        ('Bishop', 'Davidson', '1949'),
                        ('Captured', 'Francois-Andre Danican Philidor', '1749'),
                        ('Threefold Repetition', 'Unknown', '19th century'),
                        ('Fifty-move Rule', 'Unknown', '20th century'),
                        ('The board', 'Hooper&Whyld', '1992');

                        INSERT INTO piece_captures (name, capture_direction, starting_place, can_start)
                        VALUES
                        ('King', 'H, V, D', 'E1', 'No'),
                        ('Rook', 'H, V', 'A1, H1', 'No'),
                        ('Bishop', 'D', 'C1, F1', 'No'),
                        ('Knight', 'L, jump', 'B1, G1', 'Yes'),
                        ('Pawn', 'D', 'A2,B2,...H2', 'Yes'),
                        ('Queen', 'H, V, D', 'D1','No')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def add_piece(self, piece_name, piece_move, special_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO pieces (piece_name, piece_move, special_move)
                        VALUES
                        ('%s', '%s', '%s')""" % (piece_name, piece_move, special_move)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def add_rule(self, the_rule, made_by, date):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO rules_items (the_rule, made_by, date)
                        VALUES
                        ('%s', '%s', '%s')""" % (the_rule, made_by, date)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def add_capture(self, name, capture_direction, starting_place, can_start):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO piece_captures (name, capture_direction, starting_place, can_start)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (name, capture_direction, starting_place, can_start)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def delete_piece(self, piece_name, piece_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM pieces WHERE piece_name = '%s'
                        AND piece_move = '%s' """ % (piece_name, piece_move)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def delete_rule(self, the_rule):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM rules_items WHERE the_rule = '%s' """ % (the_rule)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def delete_capture(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM piece_captures WHERE name = '%s' """ % (name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def update_pieces(self, id, piece_name, piece_move, special_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE pieces
                        SET piece_name = '%s', piece_move = '%s',
                            special_move = '%s'
                        WHERE id = %s""" % (piece_name, piece_move, special_move, id)
            cursor.execute(query)
        return redirect(url_for('rules_page'))

    def update_rules(self, id, the_rule, made_by, date):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE rules_items
                        SET the_rule = '%s', made_by = '%s',
                            date = '%s'
                        WHERE id = %s""" % (the_rule, made_by, date, id)
            cursor.execute(query)
        return redirect(url_for('rules_page'))

    def update_captures(self, id, name, capture_direction, starting_place, can_start):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE piece_captures
                        SET name = '%s', capture_direction = '%s',
                            starting_place = '%s', can_start = '%s'
                        WHERE id = %s""" % (name, capture_direction, starting_place, can_start, id)
            cursor.execute(query)
        return redirect(url_for('rules_page'))

    def find_pieces(self, piece_name, piece_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM pieces
                        WHERE piece_name LIKE '%s%%'
                          AND piece_move LIKE '%s%%'
                        ORDER BY id """ % (piece_name, piece_move)
            cursor.execute(query)
            the_pieces = cursor.fetchall()
        return render_template('findpieces.html', the_pieces = the_pieces)

    def find_rules(self, the_rule):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM rules_items
                        WHERE the_rule LIKE '%s%%'
                        ORDER BY id """ % (the_rule)
            cursor.execute(query)
            uprules = cursor.fetchall()
        return render_template('findrules.html', uprules = uprules)

    def find_captures(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM piece_captures
                        WHERE name LIKE '%s%%'
                        ORDER BY id """ % (name)
            cursor.execute(query)
            upcaptures = cursor.fetchall()
        return render_template('findcaptures.html', upcaptures = upcaptures)
