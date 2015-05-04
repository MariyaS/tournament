#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random       

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Deletes all rows in the table matches. 
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")      
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    # Deletes all rows in the table players.
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")      
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    # Returns a count of all the players in the table players in the database.
    db = connect()                      
    cursor = db.cursor()                
    cursor.execute("SELECT count(*) from players;")         
    # Capture the tuple returned from query.
    num_players = cursor.fetchone()             
    db.close()
    # Returns the first value of the tuple, which is the integer of the count.
    return num_players[0]                       



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Create a row in the table player of new player. This player will also automatically show up in playerStandings view.
    db = connect() 
    cursor = db.cursor()
    # Use string to avoid SQL injection attacks since we are inserting data into database.
    cursor.execute("INSERT INTO players (player_name) VALUES (%s)",(name,))      
    # The commit is needed because we are inserting.
    db.commit()                                                                  
    db.close()                    
     

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Returns a list of tuples. Each tuple has row values from playerStandingsSorted, sorted by matches_won ascending.
    db = connect() 
    cursor = db.cursor()
    cursor.execute("SELECT * FROM playerStandingsSorted;")
    # Capture the list of tuples. Each tuple has 4 values from a row in the view.
    playerStandings_win_sorted = cursor.fetchall()                              
    db.close()
    return playerStandings_win_sorted


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Create a row in the table 'matches' recording who won.
    db = connect() 
    cursor = db.cursor()
    # We use string to avoid SQL injection attacks.
    cursor.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s,%s)",(winner, loser))      
    # The commit is needed because we are inserting.
    db.commit()                                                                                     
    db.close()
    
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # We use the view playerSandingsSorted to ensure that each player appears exactly once, and the pair is made of players adjacent in standings. 
    # Capture list of players, sorted ascending by matches_won.
    list_of_all_sorted_players = playerStandings()                                  
    # Initialize an empty list of pairs.
    list_of_pairs =[]                                                                
    # Calculate number of players. Alternatively we could call countPlayers() function.
    number_of_players = len(list_of_all_sorted_players)
    # For an odd or even number of players, there will be half as many pairs. (Note: number_of_players/2 provides whole integer pairs.)
    # Notice 2*i in indexes, because a pair is made up of two players.
    for i in xrange (number_of_players/2):                                             
        temp_tuple = list_of_all_sorted_players[2*i][0] , list_of_all_sorted_players[2*i][1], list_of_all_sorted_players[2*i+1][0], list_of_all_sorted_players[2*i+1][1] 
        list_of_pairs.append(temp_tuple)        

    # If here is an odd number of players in database, user is notified which last player in list was not paired up.
    if (number_of_players%2!=0):                                                    
        print(" Last player in ranking was left out of round. Name: "+ str(list_of_all_sorted_players[number_of_players/2+1][1])
                                                         +", Id: " +  str(list_of_all_sorted_players[number_of_players/2+1][0])
                                                         +", Wins: " +  str(list_of_all_sorted_players[number_of_players/2+1][2])
                                                         +", Plays: " +  str(list_of_all_sorted_players[number_of_players/2+1][3]))                                          
    return list_of_pairs

def playMatch(player1_id, player2_id):
    """ Assigns random score to pair of players and reports match outcome."""
    # Assigns random score to each player. Whichever player has higher score is assigned as winner. If a tie, player 1 is assigned winner. Calls reportMatch function with appropriate arguments.
    player1_score = random.randint(0, 100)
    player2_score = random.randint(0, 100)
    if player1_score >= player2_score:                      
        reportMatch(player1_id, player2_id)
    else: reportMatch(player2_id, player1_id)    
             
def checkChampionTie(top_matches_won):
    """Returns list of tuples for (id, name, matches won, matches played) of players with highest matches_won"""
    db = connect() 
    cursor = db.cursor()
    cursor.execute("SELECT * FROM playerStandingsSorted where matches_won = (%s);", (top_matches_won,))   
    # Captures list of tuples of players whose matches_won equal top_matches_won argument. 
    top_players = cursor.fetchall()                                                                                          
    db.close()
    return top_players 

    
def getOpponentMatchWins( tied_champ_id):
    """Returns a tuple  (player_id, opponent_match_wins) for any provided tied_champ_id"""
    db = connect()
    cursor = db.cursor()
    query = "SELECT winner_id, sum(matches_won) as opponent_match_wins FROM (select winner_id, loser_id as opponent_id FROM players LEFT JOIN matches on player_id = winner_id WHERE player_id=(%s) GROUP BY winner_id, opponent_id)  Opponents INNER JOIN playerStandingsSorted ON opponent_id=player_id GROUP BY winner_id;"
    cursor.execute(query, (tied_champ_id, ))
    # Captures tuple (tied_champ_id, opponent_match_wins) for argument tied_champ_id after query returns.
    opponent_match_wins = cursor.fetchall()                 
    db.close()
    # Return just the value of OMW
    return opponent_match_wins[0][1]

def getChampion():
    """Returns tuple of top player (id, name, matches_won, matches_played from playerStandingSort). If there is a tie between one or more players for matches_won a check is made for top opponent_match_wins.
    If there is a tie among the wins of the opponents as well, the first player in list is consdered champion."""

    # Captures list of all players in database, sorted by matches_won.
    list_of_all_sorted_players = playerStandings()                                          

    # The variable top_matches_won captures the highest number of matches won among all players. It is initialized to the first player's matches_won value.
    top_matches_won = list_of_all_sorted_players[0][2]                                      
    
    # Check for a tie of matches_won.  Are there more than one player with the highest number of matches won?
    # Captures list of tuples of tied champion players
    list_of_top_players = checkChampionTie(top_matches_won)
    
    # The champion variable is initialized as the first player in list_of_top_players before the checks for a tie below.
    champion = list_of_top_players[0]                                                
    
    # Check if there is more than one player. If there is, there is a tie.
    if len(list_of_top_players) > 1:                                                        
        print("There are "+ str(len(list_of_top_players))+" players tied for champion based on matches won.")                         
        # Since there is a tie, we need to check opponent match wins (OMW). We initialize top opponent match win value with first sorted player's opponent match wins.
        top_opponent_matches_won =getOpponentMatchWins(list_of_top_players[0][0])

        # We loop through each of the players tied for champion to check their opponent match wins.
        for i in xrange(len(list_of_top_players)):                                        
            # We capture their opponent match wins (first loop checks first player with themselves.)
            temp = getOpponentMatchWins(list_of_top_players[i][0])
            
            # If tied even here, then first player in the DB-sorted list we captured earlier is selected
            if top_opponent_matches_won < temp:                                             
                # New value for top_opponent_matches, since greater than previous or intial value, is set to continue to be used in loop as maximum value.
                top_opponent_matches_won=temp
                # Champion is set to player of current loop since their value for OMW is highest
                # print("We've changed champions!") # For testing
                champion = list_of_top_players[i]                                           
                
    return champion

