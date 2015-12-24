Parts Implemented by Javid Nuriyev
==================================
Player Ratings Table
--------------------

..figure:: player_ranking.png
   :figclass: align-center

   The genaral view of leagues page
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


Countries Rating Table
----------------------
In this table countries are listed according to the average FIDE rating of Top-10 chess players of that country.
It has ten attributes. One of the attributes is not displayed on the page, this attribute is ID of countries. ID is serially generated nd it is a primary key of this table at the same time.
gm(Grand Masters) column shows the quantity of grand masters in this country, similarly im (International Masters) column shows the quantity of international masters in that country.
total_titled(Total Titled) shows the total number of titled players by FIDE in that country and the total_top (Total Number of Top 100 players) is  showing how many players representing this country are in FIDE Top-100.

+----------------+---------+----------+-------------+-----------+
| Attribute      | Type    | Not Null | Primary key | Reference |
+================+=========+==========+=============+===========+
| id             | serial  | 1        | Yes         | No        |
+----------------+---------+----------+-------------+-----------+
| country_name   | integer | 1        | No          | Yes       |
+----------------+---------+----------+-------------+-----------+
| average        | integer | 1        | No          | Yes       |
+----------------+---------+----------+-------------+-----------+
| gm             | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+
| im             | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+
| total_titled   | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+
| total_top      | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+
| country_rank   | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+
| best_player    | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+
| highest_rating | integer | 1        | No          | No        |
+----------------+---------+----------+-------------+-----------+

**SQL statement for creating the countries table : **

.. code-block:: python

            query = """CREATE TABLE countries_table (
                        id serial PRIMARY KEY,
                        country_name text UNIQUE NOT NULL,
                        average integer DEFAULT 0,
                        gm integer DEFAULT 0,
                        im integer DEFAULT 0,
                        total_titled integer DEFAULT 0,
                        total_top integer DEFAULT 0,
                        country_rank integer DEFAULT 0,
                        best_player text UNIQUE NOT NULL,
                        highest_rating integer DEFAULT 0);"""
            cursor.execute(query)

Add Country
+++++++++++
Country can be added to the table by filling the fields and cliccking on 'Add Country' button

**SQL statement for adding a country to the countries table : **
.. code-block:: python

    def add_country(self, country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO countries_table (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating)
                        VALUES
                        ('%s', %s, %s, %s, %s, %s, %s, '%s', %s )""" % (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rankings_page'))

Find Country
++++++++++++
Country and its data can be found by typing the name of the country and clicking on 'Find Country' table. After that the country that a user is searching for is displayed on a new page.

**SQL statement for finding a country in the countries table : **

.. code-block:: python

    def find_country(self, country_name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM countries_table
                        WHERE country_name LIKE '%s%%'
                        ORDER BY id """ % (country_name)
            cursor.execute(query)
            countries = cursor.fetchall()
     return render_template('findcountries.html', countries = countries)


Deleting Country
++++++++++++++++
Country can be deleted by typing the name of the country to the corresponding field and clicking 'Delete Country'. However, if the country to be deleted is referenced in the Player Rankings table(worldplayers) then this country can not be deleted as there are players representing this country.

**SQL statement for deleting countries from the table :**

.. code-block:: python

    def delete_country(self, country_name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM countries_table WHERE country_name = '%s'""" % (country_name)
            cursor.execute(query)
            connection.commit()

    return redirect(url_for('rankings_page'))

Update Country
++++++++++++++
Country data can be updated by clicking on the 'Update' button next to each country. Update here affects other tables that reference countries table so it is needed to be attentive while updating.
After we click on the button new page is opened where we can update the country data.

**SQL statement for opening update page for countries :**

.. code-block:: python

    def open_updatecountries(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM countries_table WHERE id  = %s" % (id)
            cursor.execute(query)
            countries = cursor.fetchone()
    return render_template('updatecountriespage.html', countries = countries)

**SQL statement for updating countries :**

.. code-block:: python

    def update_countriess(self, id, country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE countries_table
                        SET country_name = '%s', average = %s, gm = %s, im = %s, total_titled = %s, total_top = %s,
                            country_rank = %s, best_player = '%s', highest_rating = %s
                        WHERE id = %s""" % (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating, id)
            cursor.execute(query)
   return redirect(url_for('rankings_page'))

Player Info Table
-----------------
In this table detailed information about every player listed in the rankings table. There are eleven columns. The ID is a primary key.
Furthermore, there should be an entry per player so for this purpose name, surname pair is unique in this table to avoid duplicate appearance of the players.
There is also a foreign key pointing to the wPlayer Rankigs table(worldplayers).
+------------------------+---------+----------+-------------+-----------+
| Attribute              | Type    | Not Null | Primary key | Reference |
+========================+=========+==========+=============+===========+
| id                     | serial  | 1        | Yes         | No        |
+------------------------+---------+----------+-------------+-----------+
| name                   | integer | 1        | No          | Yes       |
+------------------------+---------+----------+-------------+-----------+
| surname                | integer | 1        | No          | Yes       |
+------------------------+---------+----------+-------------+-----------+
| country                | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| club                   | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| best_rating            | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| best_ranking           | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| best_torunament        | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| best_tournament_result | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| curr_rating            | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+
| curr_ranking           | integer | 1        | No          | No        |
+------------------------+---------+----------+-------------+-----------+

**SQL statement for creating the countries table : **

.. code-block:: python

          CREATE TABLE player_info (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        country text NOT NULL REFERENCES countries_table(country_name) ON UPDATE CASCADE ON DELETE RESTRICT,
                        club text NOT NULL,
                        best_rating integer DEFAULT 0,
                        best_ranking integer DEFAULT 0,
                        best_tournament text NOT NULL,
                        best_tournament_result text NOT NULL,
                        curr_rating integer DEFAULT 0,
                        curr_ranking integer DEFAULT 0,
                        UNIQUE(name, surname) REFERENCES worldplayers(name, surname)ON UPDATE CASCADE ON DELETE RESTRICT)
                        """
            cursor.execute(query)

Initialize Player Info
++++++++++++++++++++++
The player info table can be initialize by clicking on the button 'Initialize table'

**SQL statement for initializing player info table :**

.. code-block:: python

           query = """INSERT INTO player_info (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
                        VALUES
                        ('MAGNUS', 'CARLSEN', 'NORWAY', 'OS BADEN BADEN', 2850 , 1, 'MonteCarlo', 'Champion', 2850, 1),
                        ('TEYMOUR', 'RADJABOV', 'AZERBAIJAN','SOCAR BAKU', 2760, 8, 'Lenaries','finalist', 2739, 22),
                        ('SHAKHRIYAR', 'MAMMADYAROV', 'AZERBAIJAN', 'SOCAR BAKU',2755, 12,'Australian Open', 'Finalist' ,2746, 20)"""
             cursor.execute(query)



Add Player Info
+++++++++++++++
As the player info table points to the rankings table there can be added only players that already exist in the player rankings table by filling the data in the fields on the page and clicking the 'Add Player' button.

**SQL statement for adding a player to the player_info table :**

.. code-block:: python

    def add_player_info(self, name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO player_info (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
            cursor.execute(query)

            connection.commit()
    return redirect(url_for('rankings_page'))

Find Player Info
++++++++++++++++
The info about each player can be specifically retrieved by typing the name and surname of the required player and clicking the 'Find player' button.

**SQL statement for finding a player from the player_info table :**

.. code-block:: python

    def find_player_info(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM player_info
                        WHERE name LIKE '%s%%'
                          AND surname LIKE '%s%%'
                        ORDER BY id """ % (name, surname)
            cursor.execute(query)
            player_info = cursor.fetchall()
    return render_template('find_playerBiography.html', player_info = player_info)

Deleting Player Info
++++++++++++++++++++
The info of a player can be deleted whenever there is necessity by typing the name and surname of the player whose info is to be deleted and clicking the 'Delete Player' button.

**SQL statement for deleting a player from the player_info table :**
.. code-block:: python

       def delete_player_info(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM player_info WHERE name = '%s'
                        AND surname = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('rankings_page'))

Update Player Info
++++++++++++++++++
The info of each player can be updated. The new page opens in which new data can be entered and after clicking the button the cahnges can be noticed in the table.

**SQL statement for opening a page for updating the player info :**

.. code-block:: python

    def open_update_player_info(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM player_info WHERE id  = %s" % (id)
            cursor.execute(query)
            player_info = cursor.fetchone()
    return render_template('update_biography.html', player_info = player_info)

**SQL statement for updating the player info :**

.. code-block:: python

    def update_player(self, id, name, surname, country, club, rating, ranking, age, gender):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE worldplayers
                        SET name = '%s', surname = '%s', country = '%s', club = '%s', rating = '%s', ranking = '%s', age = '%s', gender = '%s'
                        WHERE id = %s""" % (name, surname, country, club, rating, ranking, age, gender, id)
            cursor.execute(query)
    return redirect(url_for('rankings_page'))



