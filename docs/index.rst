Welcome to Chess's documentation!
=================================

:Team: CHESS

:Members:

   * Ahmet Turk
   * Javid Nuriyev
   * Ira Shyti
   * Mursit Sezen
   * Ahmet Gulum

Project description
-------------------
We have created a webpage with its own database. The webpage is about the chess game.
You can find information for local tournaments, upcoming events, international ranking of players, history of chess, rules of chess and benefits.
There are 14 tables in total. In all the tables user can add,delete, find and update the data.
Membership is not required for our site. It is thought to be a sharing platform for everybody who is interested in chess.


Work Sharing
------------
**Ahmet Türk**
   - Local Players table
   - Local Games table

**Javid Nuriyev**
   - Player Rankings table
   - Countries table
   - Player Info table

**Ira Shyti**
   - Upcoming Events table
   - Championships table
   - History of chess table

**Murşit Sezen**
   - Movement table
   - Capture and Place table
   - Rule History table

**Ahmet Gülüm**
   - Benefit table
   - Relation table
   - People table

.. literalinclude:: ../server.py
    :language: python
    :lines: 12-40
    :emphasize-lines: 2



.. figure:: chess.jpg
   :scale: 30 %
   :alt: map to buried treasure


Contents:

.. toctree::
   :maxdepth: 1

   user/index
   developer/index
