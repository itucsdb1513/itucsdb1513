Parts Implemented by Ahmet Türk
===============================
Local Players table
-------------------
This table shows the local players.
The table has six columns. The primary key of the table is the id, which is generated serially.
The couple of name and surname is unique.

+------------+---------+----------+-------------+-----------+
| Attribuite | Type    | Not Null | Primary key | Reference |
+============+=========+==========+=============+===========+
| id         | serial  | 1        | Yes         | No        |
+------------+---------+----------+-------------+-----------+
| name       | text    | 1        | No          | No        |
+------------+---------+----------+-------------+-----------+
| surname    | text    | 1        | No          | No        |
+------------+---------+----------+-------------+-----------+
| win        | integer | 0        | No          | No        |
+------------+---------+----------+-------------+-----------+
| lose       | integer | 0        | No          | No        |
+------------+---------+----------+-------------+-----------+
| draw       | integer | 0        | No          | No        |
+------------+---------+----------+-------------+-----------+

   - *id* is the primary key
   - *name* the name of the player
   - *surname* the surname of the player
   - *win* how many times the player won
   - *lose* how many times the player lost
   - *draw* how many times the player drawn

**SQL statement for initializing the local players table : **

.. code-block:: python

      query = """CREATE TABLE localplayers (
                         id serial PRIMARY KEY,
                         name text NOT NULL,
                         surname text NOT NULL,
                         win integer DEFAULT 0,
                         lose integer DEFAULT 0,
                         draw integer DEFAULt 0,
                         UNIQUE (name, surname));"""
      cursor.execute(query)

Initializing the Table
++++++++++++++++++++++
The local players table can be initialized by pressing the *initialize table* button that is below the page.
When the table is initialized it shows 25 players.

**SQL statement for initializing the local players table : **

.. code-block:: python

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
                          ('SONGUL', 'TERLEMEZ', 0, 1, 0);"""
   cursor.execute(query)
   connection.commit()


Add Player
++++++++++
Every user can add a player into the table. User should give values for at least name and surname attributes since they cannot be empty.
While adding a new player, the user should take in considerance that the new player cannot have the same couple of name and surname with any other
player in the table since the couple of name and surname attribute is unique.

**SQL statement for aadding a player to the table : **

.. code-block:: python

   def add_player(self, name, surname, win, lose, draw):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO localplayers (name, surname, win, lose, draw)
                        VALUES
                        ('%s', '%s', %s, %s, %s)""" % (name, surname, win, lose, draw)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))

Find Player
+++++++++++
For the local players table there are two ways in which user can find a player. First way is to find
it by the id on the table. Second way is to find it by entering name and surname of the player.

SQL statement for finding player by the id on the table :

.. code-block:: python

   def find_player_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM localplayers WHERE id = %s """ % (id)
            cursor.execute(query)
            player = cursor.fetchall()
        return render_template('findlp.html', player = player)

SQL statement for finding player by name and surname :

.. code-block:: python

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

Delete Player
+++++++++++++
The user can choose one of the two ways for deleting a player from the table.
They can delete a player by its id, by name and surname. However user cannot delete a player who belongs to local games table.

SQL statement for deleting a player by the id on the table :

.. code-block:: python

   def delete_player_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM localplayers WHERE id = %s """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))



SQL statement for deleting a player by name and surname :

.. code-block:: python

   def delete_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM localplayers WHERE name = '%s'
                        AND surname = '%s' """ % (name, surname)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))

Update Player
+++++++++++++
A player can be updated by pressing the name of the player that the user wants to update.

SQL statement for opening the  update player page :

.. code-block:: python

   def open_updatelp(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM localplayers WHERE id  = %s" % (id)
            cursor.execute(query)
            player = cursor.fetchone()
        return render_template('updatelp.html', player = player)


SQL statement for updating a player :

.. code-block:: python

   def update_player(self, id, name, surname, win, lose, draw):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE localplayers
                        SET name = '%s', surname = '%s',
                            win = %s, lose = %s, draw = %s
                        WHERE id = %s""" % (name, surname, win, lose, draw, id)
            cursor.execute(query)
        return redirect(url_for('localtour_page'))


Local Games Table
-----------------
This table shows the local games. It has four attributes which are id, playerone, playertwo,
result. The primary key of this table is id which is serially generated. Playerone and playertwo are foreign keys for the
local players table. They references id of local players table. Result shows the result of the game.


+-----------+---------+----------+-------------+-----------+
| Attribute | Type    | Not Null | Primary key | Reference |
+===========+=========+==========+=============+===========+
| id        | serial  | 1        | Yes         | No        |
+-----------+---------+----------+-------------+-----------+
| playerone | integer | 1        | No          | Yes       |
+-----------+---------+----------+-------------+-----------+
| playertwo | integer | 1        | No          | Yes       |
+-----------+---------+----------+-------------+-----------+
| result    | integer | 1        | No          | No        |
+-----------+---------+----------+-------------+-----------+


**SQL statement for initializing the local games table : **

.. code-block:: python


   query = """CREATE TABLE localgames (
                         id serial PRIMARY KEY,
                         playerone integer NOT NULL references localplayers(id),
                         playertwo integer NOT NULL references localplayers(id),
                         result integer NOT NULL);"""
   cursor.execute(query)


Initialize Table
++++++++++++++++
User can initialize the local games table to its initial values by pressing the initialize table button.
When the table is initialized it shows the information for 24 different games.

**SQL statement for initializing the local games table : **

.. code-block:: python

   query = """INSERT INTO localgames (playerone, playertwo, result)
                         VALUES
                          (14, 2, 1),(3, 13, 1),(1, 25, 1),(2, 23, 1),
                          (19, 21, 2),(20, 19, 2),(8, 18, 1),(6, 1, 2),
                          (4, 10, 0),(22, 5, 1),(21, 17, 0),(16, 18, 2),
                          (13, 6, 1),(18, 20, 2),(4, 7, 2),(23, 13, 2),
                          (5, 16, 1),(24, 8, 1),(3, 9, 0),(1, 15, 2),
                          (12, 14, 1),(9, 11, 2),(6, 12, 1),(7, 13, 0);"""
   cursor.execute(query)


Add Local Game
++++++++++++++
The users can add a new local game on the table by entering all the values that are required since none of them can be
NULL. User can select players who also in local players table by helping of dropdown list. The new added game affects
win, lose and draw points of players according to result of the game.

SQL statement for adding a local game :

.. code-block:: python

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


Find Local Game
+++++++++++++++
There are two ways by which a user can find a local game, either by its id on the table or by the id of the player.

 SQL statement for finding local game by the id on the table :

.. code-block:: python

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

 SQL statement for finding local game by the id of player :

.. code-block:: python

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


Deleting Local Game
+++++++++++++++++++
There is one way for deleting a local game, which is by the id on the table.

 SQL statement for deleting local game by the id on the table :

.. code-block:: python

   def delete_game(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM localgames WHERE id = %s """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('localtour_page'))
