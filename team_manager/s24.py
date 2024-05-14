from . import models
from . import helpers
from .data import gsheet_link as gs_link
import config



# complete_data = gs_link.get_data('PLAYERS')
players = helpers.get_players()

league_deschamps = models.League()

league_deschamps.players = players

season_2024 = models.Season(name='2024-2025', start_date='2024-09-03', stop_date='2025-04-29')	

print('players', players)
line1 = models.Line(name='Ligne 1', forward_left=players[0], forward_right=players[1], center=players[2], defense_left=players[3], defence_right=players[4])
line2 = models.Line(name='Ligne 2', forward_left=players[5], forward_right=players[6], center=players[7], defense_left=players[8], defence_right=players[9])
line3 = models.Line(name='Ligne 3', forward_left=players[10], forward_right=players[11], center=players[12], defense_left=players[13], defence_right=players[14])
line4 = models.Line(name='Ligne 4', forward_left=players[15], forward_right=players[16], center=players[17], defense_left=players[18], defence_right=players[19])

league_deschamps.lines = {0: line1, 1: line2, 2: line3, 3:line4}

league_deschamps.generate_games(season=season_2024, weekday=1, time='20:00')
print(league_deschamps.games)
league_deschamps.games[34].location = 'St-Tim'
# league_deschamps.games[33].local_team.line1.players['forward_left'] = None
league_deschamps.replace_player(player='Mathieu', games=3)



for game_key in league_deschamps.games.keys():
	print(game_key, league_deschamps.games[game_key])
	league_deschamps.games[game_key].print()

print('total: ', len(league_deschamps.games), 'games')

league_deschamps.find_spare()


# # generate a game
# team1 = models.Team(line1=line1, line2=line2, goaler=players[19], substitution=None)
# team2 = models.Team(line1=line3, line2=line4, goaler=players[18], substitution=None)

# game1 = models.Game(local_team=team1, visitor_team=team2, date='2024-09-03', location=config.default_location, referee=None, season=season_2024)


# league_deschamps.games.append(game1)

# print(complete_data)

#game1 = models.Game(local_team, visitor_team, date, location, referee=None, season=None)