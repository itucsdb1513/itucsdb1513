Parts Implemented by Murşit Sezen
=================================

* To access Rules page from home page of *Chess*, click *Rules* bar as shown below picture. 

.. figure:: mursit_picture/main.JPG
      :scale: 50 %
      :alt: Main

      *Home page of Chess*

Movement Table
--------------

* Movement table of Rules Page and its features.

.. figure:: mursit_picture/movement.JPG
      :scale: 50 %
      :alt: Movement

      *Movement of Pieces*
      
* The attributes which they have abbreviations are explained under the table header.

+--------------+--------+---------------------------+
| Attribute    | Type   | Explanation               |
+==============+========+===========================+
| id           | serial | id of the piece           |
+--------------+--------+---------------------------+
| Piece Name   | string | Name of the Piece         |
+--------------+--------+---------------------------+
| Piece Move   | string | Movement in the board     |
+--------------+--------+---------------------------+
| Special Move | string | Special movement in board |
+--------------+--------+---------------------------+

Movement Table has 4 attributes.
In this table *id* is primary key and its type is serial.
Other attributes are in text type and related with the *piece name*.
The user can do four operations in this table. Those are:
- Add Piece
- Delete Piece
- Find Piece
- Update Piece


Adding Piece
++++++++++++

* At the same page where the table is displayed below the table there are fields which should be filled.
* If the user wants to add a piece to the table the user should fill the fields shown below and click on the button *Add Piece*.
* While adding a new piece, the user should take in considerance that the new piece can not have the same name with any other
  piece in the table since the name attribute is unique. 

.. figure:: mursit_picture/add_mov.JPG
      :scale: 50 %
      :alt: Add Movement

      *Adding part of movement table*

After the user fills the fields and clicks on the "Add Piece" the added piece is added to the table and displayed in it.

Delete Piece
++++++++++++

* The piece can be deleted from the list. To delete a piece from the list a user needs to write the name and move 
  of the piece to be deleted ito the necessary box.
* While deleting piece from table, the user should take in considerance that the piece can not be in the Capture Table, 
  since Capture Table is referenced to Movement Table and a shared data can not be deleted from movement table.
* After entering the name and the move of the piece to be deleted *Delete Piece* button is clicked.

.. figure:: mursit_picture/del_find_mov.JPG
      :scale: 50 %
      :alt: Delete Piece

      *Removing piece from table*

Find Piece
++++++++++

* The piece can be searched by typing name and move of the piece which the user wants to display.
* After the name and move is typed into the fields the *Find Piece* button should be clicked to perform the action.
* The fields where the name and the move of the piece should be written are located below the *Adding Piece* part as shown below.

.. figure:: mursit_picture/del_find_mov.JPG
      :scale: 50 %
      :alt: Find Piece

      *Finding Movement of the Pieces by name and move*

- After the piece name and move is typed into the fields and the button is clicked a new page opens in which the piece
  whose name and move was typed is displayed with all the data of this piece displayed.

.. figure:: mursit_picture/find_mov.JPG
      :scale: 50 %
      :alt: Finding piece in a new page

       *Displaying found piece*

      
Initialize Table
++++++++++++++++
    
      - To initialize the table you can click *Initialize Table*  button under the delete and find piece table as shown 
        above in the screenshot of delete and find piece table .

Update Piece
++++++++++++

* To update the data of the piece there are *Update* buttons to the right of each piece in the Movement. 
  These buttons can be noticed in the image of the Movement Table illustrated above.
* When the user wants to update the data of the piece in the Movement Table it is enough to click 
  on the corresponding *Update* button as shown below.

.. figure:: mursit_picture/movement_up.jpg
      :scale: 50 %
      :alt: Clicking to update a Piece

       *Clicking on the "Update" button to update a piece*

* After clicking on the "Update" button a new page is opened. On the new page data of the piece that was chosen to be updated by the user is displayed.
* Each field can be updated by modifying the data written in the fields and clicking *Update* button.
* The page mentioned above is illustrated in the figure below.

.. figure:: mursit_picture/up_move.JPG
      :scale: 50 %
      :alt: Update the data

       *Updating player data*

* If the data is exist in the Capture Table, the name of the piece can not be changed;
  since Capture Table is referenced from Movement Table with attribute *piece name*. 
  
