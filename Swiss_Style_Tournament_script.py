
import math         # needed to calculate the number of rounds in a tournament.

from tournament import *


the_players = [
    ('Anna'), ('Bill'), ('Craig'), ('Dave'),
    ('Evan'), ('Fred'), ('Guy'), ('Haidi'),
    ('Ivan'), ('Joe'), ('Luke'), ('Kaili'),
    ('Matt'), ('Neil'), ('Oliver'), ('Patrick')
]


def registerPlayers():
    """Adds a static players to the tournament database."""
    for i in xrange (len(the_players)):
        registerPlayer(the_players[i])
    # For testing:
    # print("Registered 16 players")

if __name__ == '__main__':
    """Runs a Swiss-system tournament.
            - Clears all tables from previous tournament records.
            - Registers players for current tournament.
            - Makes appropriate number of rounds based on number of players in database. Send a notification at the beginning and end of each round.
            - Determine and declare champion. """
    # Delete all records from previous Tournament.
    deleteMatches()
    deletePlayers()
    
    # For testing. Print statements to make sure DB is clear and ready for new tournament.
    # print("countPlayers: "+ str(countPlayers()))
    # print("playerStandingsSorted " + str(playerStandings()))

    # Register the 16 players
    registerPlayers()

    # Register the 'odd' player
    registerPlayer('Mary')

    print("Welcome to a new tournamnet!")
    print("There are "+ str(countPlayers())+ " registered for this tournament. Let's begin!")

    # Set up rounds for the tournament and play them. (There are log 2 (countPlayer) rounds for each tournament. The last player of an odd number of players in DB gets left out and a notification is sent.) 
    for i in xrange(int(math.log(countPlayers(), 2))):
        print("Begin Round " + str(i))
        # Set up pairs for each round considering all players in database.
        # For each round, capture list of pairs (all players in DB considered)
        list_of_pairs_for_round = swissPairings()
        # Make each pair play. 
        for j in xrange(len(list_of_pairs_for_round)):                                      
            # Extricate their ids from tuple.
            player1 = list_of_pairs_for_round[j][0]                                         
            player2 = list_of_pairs_for_round[j][2]
            # Note: The playMatch function calls recordMatch function with appropriate winner.
            playMatch(player1, player2)
        print("End of Round " + str(i))
        
    champion = getChampion()
    # Notify who is Champion for current tournamnet.
    print("The Champion is: "+ str(champion[1]) + ". Id: " + str(champion[0])+", Wins: "+str(champion[2])+ ", Plays: "+str(champion[3])+".")

 
