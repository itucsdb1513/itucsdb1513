Parts Implemented by Javid Nuriyev
==================================

First thing that the user faces when accessing our site is the main page which is shown below.
When the user clicks at "Rankings" bar in the main page, rankings of the players and related data is shown on that page.

.. figure:: jav_picture/main.png
      :scale: 50 %
      :alt: Main

      *This is the main page*

1. Player Rankings
==================
Click at the Rankings bar

.. figure:: jav_picture/ranking.png
      :scale: 50 %
      :alt: Player Rankings

      *This is the Player Rankings page*

On the screenshot shown above the player rankings data is displayed.
In this table there are 8 columns displayed to the user. Those columns display the notable data about each top player.
In this table there are countries from another countries page so when doing operations and changing countries data that should be taken into account.
This table can be considered as a generator table because if the user wants to add a player or upate some player data the player name have to be present in this table.
Other than the attributes displayed as columns of the table there is also ID attribute which is used for background operations.
The players are ordered in the table according to their ratings from the player with tp rating to the player with the lowest rating.
There are five operations that can be carried on the table. Those are:
1. Add Player
2. Find Player
3. Find Players by Country
4. Delete Player
5. Update Player

1.1 Add Player
--------------

At the same page where the table is displayed below the table there are fields which should be filled.
If the user wants to add a player to the table the user should fill the fields shown below and click on the button "Add Player".

.. figure:: jav_picture/add_player.png
      :scale: 50 %
      :alt: Add Player to Player Rankings Table

      *Add button is shown at the bottom of the fields*

After the user fills the fields and clicks on the "Add Player" the added player is added to the table and displayed in it.


