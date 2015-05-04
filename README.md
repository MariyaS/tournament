# tournament
README for Tournament Results

A Python module that uses the PostgreSQL database to keep track of players, rank the players, and pair them for matches in a game tournament. The game tournament uses the Swiss system for pairing up players in each round where no player is eliminated and the pairing of players is based on the same number of wins or the closest number of wins.


I. File list
---------------
tournament.py				- contains the module methods
tournament_test.py			- Python file used for testing
tournament.sql				- Table and View definitions for the tournament database
Swiss_Style_Tournament_script.py	- Python file that runs the tournament


II. Steps to Run the Tournament Application
-----------------------------------------------

II.i Set up the Database in your vagrant environment.

	It is assumed that you will have the same vagrant environment as provided in the Udacity course 'Introduction to Relational Databases'.
	It is assumed that there is no database tournament and all previous version have been deleted.

1.  In GIT Bash, navigate to the following location:
	cd Desktop/fullstack/vagrant
2.  Run the following command to start up vagrant.
	vagrant up
3.  Run the following command to enter Linux shell prompt.
	vagrant ssh
4.  Navigate to the tournament folder within the vagrant environment
	cd /vagrant/tournament
5.  Run the following command to interact with the PostgreSQL database from Linux shell prompt
	psql
5.  If a database of the same name already exists (check with \l command), drop it. You should see confirmation.
	DROP DATABASE tournament; 
6.  Create database by the name of tournament.  You should see confirmation.
	CREATE DATABASE tournament;
7.  Connect to the new database you just created as user vagrant. You should see confirmation.
	\c tournament
9.  Run the \i command on the .sql file which contains the definitions for the table and views for the tournament database:
	\i tournament.sql
10. You should see confirmation that two Tables and one View have been created.
11. Exit with \q



II.ii 	Run Python module
1. Run the following command to make sure the tests provided pass
	python tournament_test.py
2. Run the Swiss style tournament
	python Swiss_Style_Tournament_script.py
3. Make changes to this file as you desire.



III. Design Decisions 
---------------------

The module has been designed to follow the simple form of the Swiss style tournament where there are no eliminations and there is only one champion based on the highest number of matches won.  

The database schema supports only one tournament per run of the program and all matches and players are deleted before a tournament begins.

Out of all the players that exist in the database, pairs are made based on the player's wins - either players with the same number of wins are paired or the players with the closest number of wins. The players are paired based on their ranking of matches_won during the tournament.  There are no ties possible for matches at the moment. If there is a tie in a match then the first player in the pair is made a winner. 

The number of rounds is calculated based on the number of players in the database: log of count of players base 2.  Any players left out of a round is pointed out by having their name and information printed to the console. They simply 'sit-out' of the round. 

The champion is calculated at the end of the last round. The first player in the ranking is taken based on the highest matches-won. If there is more than one player with the same high matches-won value then the Opponent Match Win (OMW) value is compared for the tied-for-champion players. The player with the highest OMW value is made champion. If there is a tie for champion in both the matches_won and OMW value, then the first player in the set is made champion.  


Future improvements to this module and database schema can include
	- supporting more than one tournament
	- supporting a tie between players or make them play again if there is a tie
	- for the players not paired up in rounds, the player gets a free win (allowed one time per tournamnet) rather than sitting out
	- if there is a tie for the champion spot and there is also a tie for Opponent Match Wins (OMW), find alternative for third comparison
	- systems other than the Swiss style tournament where eliminations are possible

