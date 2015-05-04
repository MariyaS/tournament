-- Table definitions for the tournament project.
--

-- The players table has the player_id as Primary Key. Because it is of a Serial data type it is created automatically when one inserts a new player_name.
CREATE TABLE players (	player_id	SERIAL PRIMARY KEY,
						player_name	TEXT
);  

-- The matches table has the match_id as Primary Key.  The winner_id and loser_id are Foreign Keys which will be checked for existence against the players table.
CREATE TABLE matches  ( match_id	SERIAL PRIMARY KEY, 
						winner_id	integer references players(player_id), 
						loser_id	integer references players(player_id)
);

-- The playerStandingsSorted view has player_id, player_name, matches_won and matches_played columns. 
CREATE VIEW playerStandingsSorted as 
						select player_id, 
							   player_name,
							   (select count(*) 
							   	from matches
							   	where player_id = winner_id)  as matches_won,
							   (select count(*) 
							   	from matches
							   	where player_id in (winner_id, loser_id)) as  matches_played
						from   players  left join
							   matches 
							   ON player_id in (winner_id, loser_id)
						group by player_id
						ORDER BY matches_won DESC
;
