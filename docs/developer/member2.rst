Parts Implemented by Javid Nuriyev
==================================
Player Ratings Table
--------------------
This table shows the rankings of top players according to FIDE. On the website this table is under the header Player Tables but in the database it is named worldplayers
The table has nine columns columns but ID is not displayed on the page to the users so only eight columns are displayed. The primary key of the table is the id of the player and it is generated serially.
The couple of name and surname is unique in this table as each player can occur only once in the rankings table.
There is also a foreign key in this table which is countries column.

+-----------+---------+----------+-------------+-----------+
| Attribute | Type    | Not Null | Primary key | Reference |
+===========+=========+==========+=============+===========+
| id        | serial  | 1        | Yes         | No        |
+-----------+---------+----------+-------------+-----------+
| name      | text    | 1        | No          | No        |
+-----------+---------+----------+-------------+-----------+
| surname   | text    | 1        | No          | No        |
+-----------+---------+----------+-------------+-----------+
| country   | text    | 1        | No          | Yes       |
+-----------+---------+----------+-------------+-----------+
| club      | text    | 1        | No          | No        |
+-----------+---------+----------+-------------+-----------+
| age       | integer | 0        | No          | No        |
+-----------+---------+----------+-------------+-----------+
| rating    | integer | 0        | No          | No        |
+-----------+---------+----------+-------------+-----------+
| ranking   | integer | 0        | No          | No        |
+-----------+---------+----------+-------------+-----------+
| gender    | text    | 1        | No          | No        |
+-----------+---------+----------+-------------+-----------+


   - *id* is the primary key
   - *name* the name of the player
   - *surname* the surname of the player
   - *country* is the country player represents
   - *club* is the club player plays for
   - *age* age of the player
   - *rating* is the FIDE rating of the player
   - *ranking* is the ranking of the player according to FIDE
   - *gender* is a gender of the player

   **SQL statement for initializing the local players table : **

.. code-block:: python

             query = """CREATE TABLE worldplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        country text NOT NULL REFERENCES countries_table(country_name) ON UPDATE CASCADE ON DELETE RESTRICT,
                        club text NOT NULL,
                        rating integer DEFAULT 0,
                        ranking integer DEFAULT 0,
                        age integer DEFAULT 0,
                        gender text NOT NULL,
                        UNIQUE (name, surname));"""
             cursor.execute(query)

Initializing the Table
++++++++++++++++++++++
The Player Rankings table can be initialized by pressing the *initialize table* button that is above the table.
When the table is initialized it shows 7 players starting with the top player Magnus Carlsen.

**SQL statement for initializing the Player Rankings table (worldplayers table) : **
.. code-block:: python

      query = """INSERT INTO worldplayers (name, surname, country, club, rating, ranking, age, gender)
                        VALUES
                        ('MAGNUS', 'CARLSEN', 'NORWAY', 'OS BADEN BADEN', 2834, 1, 25, 'MALE'),
                        ('TEYMOUR', 'RADJABOV', 'AZERBAIJAN', 'SOCAR BAKU', 2739, 22, 28, 'MALE'),
                        ('SHAKHRIYAR', 'MAMMADYAROV', 'AZERBAIJAN', 'SOCAR BAKU', 2746, 16, 30, 'MALE'),
                        ('VISWANATHAN', 'ANAND', 'INDIA', 'BADEN BADEN', 2796, 3, 46, 'MALE'),
                        ('VLADIMIR', 'KRAMNIK', 'RUSSIA', 'NAO Paris', 2796, 4, 40, 'MALE'),
                        ('HIKARU', 'NAKAMURA', 'USA', 'Obiettivo Risarcimento', 2793, 5, 28, 'MALE'),
                        ('LEVON', 'ARONIAN', 'ARMENIA', 'Mainz', 2788, 6, 33, 'MALE');"""

      cursor.execute(query)
      connection.commit()

Add Player
++++++++++
Players can be added to the ranking table by filling the fields below the ranking table and clicking 'Add Player'.
The pair of name and surname in the Player Rankings table is unique as a result a player with exacty same name and surname can not be added to the table.

**SQL statement for adding a player to the table : **

.. code-block:: python

      def add_player(self, name, surname, country, club, rating, ranking, age, gender):
         with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO worldplayers (name, surname, country, club, rating, ranking, age, gender)
                        VALUES
                        ('%s', '%s', '%s', '%s', %s, %s, %s, '%s')""" % (name, surname, country, club, rating, ranking, age, gender)
            cursor.execute(query)

            connection.commit()
         return redirect(url_for('rankings_page'))

Find Player
+++++++++++
Player can be retrieved from the Player Rankings table in two ways. One of them is to find a player by name and surname
and the other method is to list players by countries.

**SQL statement for finding player by name and surname :**
.. code-block:: python

     def find_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM worldplayers
                        WHERE name LIKE '%s%%'
                          AND surname LIKE '%s%%'
                        ORDER BY id """ % (name, surname)
            cursor.execute(query)
            player = cursor.fetchall()
      return render_template('find_player.html', player = player)

**SQL statement for finding players by country:**
.. code-block:: python

    def find_player_by_country(self, country):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM worldplayers
                        WHERE country LIKE '%s%%'
                        ORDER BY rating DESC """ % (country)
            cursor.execute(query)
            player = cursor.fetchall()
    return render_template('find_player.html', player = player)

Delete Player
+++++++++++++
Player can be deleted from the rankings table unless the player is not a member of the player_info table
To delete a player is enough to type a player name and surname to the field provided for that purpose and clicking 'Delete Player' button

SQL statement for deleting a player by name and surname from the table :

.. code-block:: python

    def delete_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM worldplayers WHERE name = '%s'
                        AND surname = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()

    return redirect(url_for('rankings_page'))

Update Player
+++++++++++++
Each player's data can be updated thanks to the buttons located on thr right-side to each player in the Player Rankings table. After that new page is opened.
After 'Update' button is pressed new data can be entered into the fields that are desired to be changed and 'Update Player' button is pushed which completes this operation.

SQL statement for opening the  update player page :

.. code-block:: python

    def open_update_player(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM worldplayers WHERE id  = %s" % (id)
            cursor.execute(query)
            player = cursor.fetchone()
            return render_template('update_player.html', player = player)

SQL statement for updating a player :

.. code-block:: python

    def update_player(self, id, name, surname, country, club, rating, ranking, age, gender):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE worldplayers
                        SET name = '%s', surname = '%s', country = '%s', club = '%s', rating = '%s', ranking = '%s', age = '%s', gender = '%s'
                        WHERE id = %s""" % (name, surname, country, club, rating, ranking, age, gender, id)
            cursor.execute(query)
        return redirect(url_for('rankings_page'))







