Parts Implemented by Murşit Sezen
=================================

Movement Table
--------------
* This table shows the pieces of the chess game. On the website this table is under the header *Movement of the Pieces*;
  however, in the database it is named as *pieces*.
* The table has four columns. The primary key of the table is the id of the piece and it is generated serially.
* The piece names are unique in this table as each piece can occur only once in the movement table.

+--------------+--------+----------+-------------+-----------+
| Attribute    | Type   | Not Null | Primary key | Reference |
+==============+========+==========+=============+===========+
| id           | serial | 1        | Yes         | No        |
+--------------+--------+----------+-------------+-----------+
| piece_name   | text   | 1        | No          | No        |
+--------------+--------+----------+-------------+-----------+
| piece_move   | text   | 1        | No          | No        |
+--------------+--------+----------+-------------+-----------+
| special_move | text   | 0        | No          | No        |
+--------------+--------+----------+-------------+-----------+


   - *id* is the primary key
   - *piece_name* is the name of the piece
   - *piece_move* is the rule of movement of the relevant piece
   - *special_move* is the special move of the relevant piece

  **SQL statement for creating the Movement Table : **

.. code-block:: python

   class Rules:

      def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

             query = """CREATE TABLE pieces (
                        id serial PRIMARY KEY,
                        piece_name text UNIQUE NOT NULL,
                        piece_move text NOT NULL,
                        special_move text);"""

            cursor.execute(query)
            connection.commit()

Initializing the Table
++++++++++++++++++++++
* The Movement Table can be initialized by pressing the *Initialize Table* button that is below of the tables.
* When the table is initialized it shows 6 pieces.

  **SQL statement for initializing the Movement Table **

.. code-block:: python

   class Rules:

      def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

         query = """INSERT INTO pieces (piece_name, piece_move, special_move)
                        VALUES
                        ('King', 'H,V,D', 'Castling'),
                        ('Rook', 'H,V', 'Castling'),
                        ('Bishop', 'D', ' '),
                        ('Knight', 'L', ' '),
                        ('Pawn', 'S.F. ,D', 'en Passant'),
                        ('Queen', 'H, V, D', ' ');"""

         cursor.execute(query)
         connection.commit()

Adding Piece
++++++++++++
* Pieces can be added to the movement table by filling the fields below the movement table and clicking 'Add Piece'.
* User should give values for Piece Name and Piece Move attributes since these attributes can not be empty.
* While adding a new piece, the user should take in considerance that the new piece can not have the same name with any other
  piece in the table since the name attribute is unique.

  **SQL statement for adding a piece to the table : **

.. code-block:: python

   class Rules:

      def add_piece(self, piece_name, piece_move, special_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO pieces (piece_name, piece_move, special_move)
                        VALUES
                        ('%s', '%s', '%s')""" % (piece_name, piece_move, special_move)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

Find Piece
++++++++++
* Pieces can be retrieved from the Movement table in two ways. One of them is to find a piece by piece name and piece move
  and the other method is just clicking *Find Piece* button and it lists all pieces in the table.

  **SQL statement for finding piece by piece name and piece move : **

.. code-block:: python

   class Rules:

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

Delete Piece
++++++++++++
* Piece can be deleted from the Movement table unless the piece is not a member of the Capture table.
* To delete a piece, the user should enter both piece name and piece move to relevant places and push *Delete Piece* button.

  **SQL statement for deleting a piece by piece name and piece move from the table : **

.. code-block:: python

   class Rules:

      def delete_piece(self, piece_name, piece_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM pieces WHERE piece_name = '%s'
                        AND piece_move = '%s' """ % (piece_name, piece_move)

            cursor.execute(query)
            connection.commit()
        return redirect(url_for('rules_page'))

Update Piece
++++++++++++
* Each piece's data can be updated thanks to the buttons located on the right-side to each piece in the Movement table. After that new page is opened.
* After *Update* button is pressed new data can be entered into the fields that are desired to be changed
  and *Update* button is pushed which completes this operation.

  **SQL statement for opening the update piece page : **

.. code-block:: python

   class Rules:

      def open_updatepieces(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM pieces WHERE id  = %s" % (id)

            cursor.execute(query)
            the_pieces = cursor.fetchone()
        return render_template('updatepiecespage.html', the_pieces = the_pieces)

**SQL statement for updating a piece :**

.. code-block:: python

   class Rules:

      def update_pieces(self, id, piece_name, piece_move, special_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE pieces
                        SET piece_name = '%s', piece_move = '%s',
                            special_move = '%s'
                        WHERE id = %s""" % (piece_name, piece_move, special_move, id)

            cursor.execute(query)
        return redirect(url_for('rules_page'))


Capture and Place Table
-----------------------
* In this table pieces are listed with their capture directions and starting points.
* On the website this table is under the header *Capture and Place Table*; however, in the database it is named as *piece_captures*.
* The table has five columns. The primary key of the table is the id of the piece and it is generated serially.
* The table has a foreign key. The *name* attribute is referenced from *piece_name* attribute of Movement table.

+-------------------+--------+----------+-------------+-----------+
| Attribute         | Type   | Not Null | Primary key | Reference |
+===================+========+==========+=============+===========+
| id                | serial | 1        | Yes         | No        |
+-------------------+--------+----------+-------------+-----------+
| name              | text   | 1        | No          | Yes       |
+-------------------+--------+----------+-------------+-----------+
| capture_direction | text   | 1        | No          | No        |
+-------------------+--------+----------+-------------+-----------+
| starting_place    | text   | 1        | No          | No        |
+-------------------+--------+----------+-------------+-----------+
| can_start         | text   | 1        | No          | No        |
+-------------------+--------+----------+-------------+-----------+

   - *id* is the primary key
   - *name* is the name of the piece
   - *capture_direction* is the capture direction of the piece
   - *starting_place* is starting point of the piece
   - *can_start* is the attribute shows if the piece can start at the beginning of the game or not

  **SQL statement for creating the Capture Table : **

.. code-block:: python

   class Rules:

      def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE piece_captures (
                        id serial PRIMARY KEY,
                        name text NOT NULL REFERENCES pieces(piece_name) ON DELETE RESTRICT,
                        capture_direction text NOT NULL,
                        starting_place text NOT NULL,
                        can_start text NOT NULL);"""

            cursor.execute(query)
            connection.commit()

Initializing the Table
++++++++++++++++++++++
* The Capture Table can be initialized by pressing the *Initialize Table* button that is below of the tables.
* When the table is initialized it shows 6 pieces.

  **SQL statement for initializing the Capture Table **

.. code-block:: python

   class Rules:

      def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

         query = """INSERT INTO piece_captures (name, capture_direction, starting_place, can_start)
                        VALUES
                        ('King', 'H, V, D', 'E1', 'No'),
                        ('Rook', 'H, V', 'A1, H1', 'No'),
                        ('Bishop', 'D', 'C1, F1', 'No'),
                        ('Knight', 'L, jump', 'B1, G1', 'Yes'),
                        ('Pawn', 'D', 'A2,B2,...H2', 'Yes'),
                        ('Queen', 'H, V, D', 'D1','No')"""

            cursor.execute(query)
            connection.commit()

Adding Piece
++++++++++++
* Pieces can be added to the capture table by filling the fields below the capture table and clicking *Add Capture*.
* Every user can add an piece into the table. User should give values for all the attributes since none of them can be empty.
* However, when a user wants to add a new piece, the user should consider that the piece has to be in the Movement table because of foreign key.

  **SQL statement for adding a piece to the capture table : **

.. code-block:: python

   class Rules:

      def add_capture(self, name, capture_direction, starting_place, can_start):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO piece_captures (name, capture_direction, starting_place, can_start)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (name, capture_direction, starting_place, can_start)

            cursor.execute(query)
            connection.commit()
        return redirect(url_for('rules_page'))

Find Piece
++++++++++
* Piece and its data can be found by typing the name of the piece and clicking on *Find Capture* button on the table.
* After that the piece that a user is searching for is displayed on a new page.

**SQL statement for finding a piece in the capture table : **

.. code-block:: python

   class Rules:

      def find_captures(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM piece_captures
                        WHERE name LIKE '%s%%'
                        ORDER BY id """ % (name)

            cursor.execute(query)
            upcaptures = cursor.fetchall()
        return render_template('findcaptures.html', upcaptures = upcaptures)


Delete Piece
++++++++++++
* Piece can be deleted by typing the name of the piece to the corresponding field and clicking *Delete Capture* button.
* However, if the piece to be deleted is referenced in the Movement Table then this piece can not be deleted;
  since the piece is also placed in the Movement Table.

  **SQL statement for deleting piece from the capture table : **

.. code-block:: python

   class Rules:

      def delete_capture(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM piece_captures WHERE name = '%s' """ % (name)

            cursor.execute(query)
            connection.commit()
        return redirect(url_for('rules_page'))

Update Piece
++++++++++++
* Each piece's data can be updated thanks to the buttons located on the right-side to each piece in the Capture Table. After that new page is opened.
* After *Update* button is pressed new data can be entered into the fields that are desired to be changed
  and *Update* button is pushed which completes this operation.

  **SQL statement for opening the update capture page : **

.. code-block:: python

   class Rules:

      def open_updatecaptures(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM piece_captures WHERE id  = %s" % (id)

            cursor.execute(query)
            upcaptures = cursor.fetchone()
        return render_template('updatecapturespage.html', upcaptures = upcaptures)

**SQL statement for updating a capture :**

.. code-block:: python

   class Rules:

      def update_captures(self, id, name, capture_direction, starting_place, can_start):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE piece_captures
                        SET name = '%s', capture_direction = '%s',
                            starting_place = '%s', can_start = '%s'
                        WHERE id = %s""" % (name, capture_direction, starting_place, can_start, id)

            cursor.execute(query)
        return redirect(url_for('rules_page'))


Rule History Table
------------------
* In this table piece rules are listed with their founder and date.
* On the website this table is under the header *Rule History Table*; however, in the database it is named as *rule_items*.
* The table has four columns. The primary key of the table is the id of the piece and it is generated serially.
* *the_rule* attribute is unique in this table as each rule can occur only once in the rule history table.
* This table is seperated from other two tables. It has no references to other tables.

+-----------+--------+----------+-------------+-----------+
| Attribute | Type   | Not Null | Primary key | Reference |
+===========+========+==========+=============+===========+
| id        | serial | 1        | Yes         | No        |
+-----------+--------+----------+-------------+-----------+
| the_rule  | text   | 1        | No          | No        |
+-----------+--------+----------+-------------+-----------+
| made_by   | text   | 1        | No          | No        |
+-----------+--------+----------+-------------+-----------+
| date      | text   | 1        | No          | No        |
+-----------+--------+----------+-------------+-----------+

   - *id* is the primary key
   - *the_rule* is the name of the rule
   - *made_by* is the person who found the rule
   - *date* is date of finding the rule

  **SQL statement for creating the Rule History Table : **

.. code-block:: python

   class Rules:

      def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE rules_items (
                        id serial PRIMARY KEY,
                        the_rule text UNIQUE NOT NULL,
                        made_by text NOT NULL,
                        date text NOT NULL);"""

            cursor.execute(query)
            connection.commit()

Initializing the Table
++++++++++++++++++++++
* The Rule History Table can be initialized by pressing the *Initialize Table* button that is below of the tables.
* When the table is initialized it shows 8 rules.

  **SQL statement for initializing the Rules History Table **

.. code-block:: python

   class Rules:

         query = """INSERT INTO rules_items (the_rule, made_by, date)
                        VALUES
                        ('Queen, Bishop', 'Hooper&Whyld', '15th century'),
                        ('Time limit', 'Sunnuck', '1861'),
                        ('Queen', 'Jacob Sarrart', '1828'),
                        ('Bishop', 'Davidson', '1949'),
                        ('Captured', 'Francois-Andre Danican Philidor', '1749'),
                        ('Threefold Repetition', 'Unknown', '19th century'),
                        ('Fifty-move Rule', 'Unknown', '20th century'),
                        ('The board', 'Hooper&Whyld', '1992');"""

            cursor.execute(query)
            connection.commit()

Adding Rule
+++++++++++
* Rules can be added to the rule history table by filling the fields below the rule history table and clicking 'Add Rule'.
* Every user can add an rule into the table. User should give values for all the attributes since none of them can be empty.

  **SQL statement for adding a rule to the Rule History Table : **

.. code-block:: python

   class Rules:

      def add_rule(self, the_rule, made_by, date):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO rules_items (the_rule, made_by, date)
                        VALUES
                        ('%s', '%s', '%s')""" % (the_rule, made_by, date)

            cursor.execute(query)
            connection.commit()
        return redirect(url_for('rules_page'))

Find Rule
+++++++++
* The rule and its data can be found by typing the name of the rule and clicking on *Find Rule* button on the table.
* After that the rule that a user is searching for is displayed on a new page.

**SQL statement for finding a rule in the Rule History Table : **

.. code-block:: python

   class Rules:

      def find_rules(self, the_rule):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM rules_items
                        WHERE the_rule LIKE '%s%%'
                        ORDER BY id """ % (the_rule)

            cursor.execute(query)
            uprules = cursor.fetchall()
        return render_template('findrules.html', uprules = uprules)


Delete Rule
+++++++++++
* Rules can be deleted by typing the name of the rule to the corresponding field and clicking *Delete Rule* button.

  **SQL statement for deleting rule from the Rule History Table : **

.. code-block:: python

   class Rules:

      def delete_rule(self, the_rule):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM rules_items WHERE the_rule = '%s' """ % (the_rule)

            cursor.execute(query)
            connection.commit()
        return redirect(url_for('rules_page'))

Update Rule
+++++++++++
* Each rule's data can be updated thanks to the buttons located on the right-side to each rule in the Rule History Table.
  After that new page is opened.
* After *Update* button is pressed new data can be entered into the fields that are desired to be changed
  and *Update* button is pushed which completes this operation.

  **SQL statement for opening the update rule page : **

.. code-block:: python

   class Rules:

      def open_updaterules(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM rules_items WHERE id  = %s" % (id)

            cursor.execute(query)
            uprules = cursor.fetchone()
        return render_template('updaterulespage.html', uprules = uprules)

**SQL statement for updating a rule :**

.. code-block:: python

   class Rules:

      def update_rules(self, id, the_rule, made_by, date):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE rules_items
                        SET the_rule = '%s', made_by = '%s',
                            date = '%s'
                        WHERE id = %s""" % (the_rule, made_by, date, id)

            cursor.execute(query)
        return redirect(url_for('rules_page'))

