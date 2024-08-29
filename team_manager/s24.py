from datetime import datetime
from . import models
from . import helpers
from .data import gsheet_link as gs_link
import config



# complete_data = gs_link.get_data('PLAYERS')
players = helpers.get_players()

league_deschamps = models.League() 

league_deschamps.players = players

season_2024 = models.Season(name='2024-2025', start_date='2024-09-03', stop_date='2025-04-29')	

# print('players', players)
line1 = models.Line(name='Ligne 1', forward_left=players[4], forward_right=players[2], center=players[3], defense_left=players[0], defence_right=players[1])
line2 = models.Line(name='Ligne 2', forward_left=players[8], forward_right=players[9], center=players[7], defense_left=players[5], defence_right=players[6])
line3 = models.Line(name='Ligne 3', forward_left=players[14], forward_right=players[13], center=players[12], defense_left=players[11], defence_right=players[10])
line4 = models.Line(name='Ligne 4', forward_left=players[18], forward_right=players[19], center=players[17], defense_left=players[16], defence_right=players[15])

league_deschamps.lines = {0: line1, 1: line2, 2: line3, 3:line4}

league_deschamps.generate_games(season=season_2024, weekday=1, time='21:00')
print(league_deschamps.games)
#league_deschamps.games[35].location = 'St-Tim'
# league_deschamps.games[33].local_team.line1.players['forward_left'] = None

league_deschamps.replace_player(request_datetime=datetime(year=2024, month=8, day=29), player='Patrick', games=1, spare='Renaud a')
league_deschamps.replace_player(request_datetime=datetime(year=2024, month=8, day=29), player='James', games=1)



for game_key in league_deschamps.games.keys():
	print(game_key, league_deschamps.games[game_key])
	league_deschamps.games[game_key].print()

print('total: ', len(league_deschamps.games), 'games')

league_deschamps.find_spare()
#league_deschamps.find_spare() # run every 5 minutes
league_deschamps.set_spare_availability('15147728092', False) # Martin replied as non available
#league_deschamps.set_spare_availability('1234560060', True) # Fred replied as available
#league_deschamps.check_and_confirm() # Check spare, and confirm available, other in stanby (run every 2 minutes)
print('checking again')
#league_deschamps.check_and_confirm() # Check spare, and confirm available, other in stanby (run every 2 minutes)

league_deschamps.print_game_sheet(2)

#league_deschamps.line_recap()
league_deschamps.print_year_sheet()
# # generate a game
# team1 = models.Team(line1=line1, line2=line2, goaler=players[19], substitution=None)
# team2 = models.Team(line1=line3, line2=line4, goaler=players[18], substitution=None)

# game1 = models.Game(local_team=team1, visitor_team=team2, date='2024-09-03', location=config.default_location, referee=None, season=season_2024)


# league_deschamps.games.append(game1)

# print(complete_data)

#game1 = models.Game(local_team, visitor_team, date, location, referee=None, season=None)