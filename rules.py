import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Rules:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM pieces"
            cursor.execute(query)
            rules = cursor.fetchall()

            query = "SELECT * FROM rules_items"
            cursor.execute(query)
            the_rules = cursor.fetchall()



        return render_template('rules.html', rules = rules, the_rules=the_rules)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS pieces;
                       DROP TABLE IF EXISTS rules_items"""
            cursor.execute(query)

            query = """CREATE TABLE pieces (
                        id serial PRIMARY KEY,
                        piece_name text NOT NULL,
                        piece_rule text NOT NULL,
                        special_move text NOT NULL);
                       CREATE TABLE rules_items (
                        id serial PRIMARY KEY,
                        the_rule text NOT NULL,
                        made_by text NOT NULL,
                        date integer NOT NULL);"""
            cursor.execute(query)

            query = """INSERT INTO pieces (piece_name, piece_rule, special_move)
                        VALUES
                        ('King', 'Hori.,Ver.', 'Castling'),
                        ('Queen', 'H, V, Diagn.', ' ');
                        INSERT INTO rules_items (the_rule, made_by, date)
                        VALUES
                        ('Davidson', 'Bishop', '1475'),
                        ('Jacob Sarratt', 'Queen', '1972')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def add_piece(self, piece_name, piece_rule, special_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO pieces (piece_name, piece_rule, special_move)
                        VALUES
                        ('%s', '%s', '%s')""" % (piece_name, piece_rule, special_move)
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

    def delete_piece(self, piece_name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM pieces WHERE piece_name = '%s' """ % (piece_name)
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

    def delete_piece_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM pieces WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def delete_rule_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM rules_items WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))




    def update_rules(self, id, the_rule, made_by, date):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE rules_items
                        SET the_rule = '%s', made_by = '%s',
                            date = %s
                        WHERE id = %s""" % (the_rule, made_by, date, id)

            cursor.execute(query)
            connection.commit()


        return redirect(url_for('rules_page'))
