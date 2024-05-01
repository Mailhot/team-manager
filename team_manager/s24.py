from . import models
from . import helpers
from .data import gsheet_link as gs_link



# complete_data = gs_link.get_data('PLAYERS')
players = helpers.get_players()

league_deschamps = models.League()

league_deschamps.players = players

season_2024 = models.Season(name='2024-2025', start_date='2024-09-03', stop_date='2025-04-29')

print('players', players)
line1 = models.Line(forward_left=players[0], forward_right=players[1], center=players[2], defense_left=players[3], defence_right=players[4])
line2 = models.Line(forward_left=players[5], forward_right=players[6], center=players[7], defense_left=players[8], defence_right=players[9])
line3 = models.Line(forward_left=players[10], forward_right=players[11], center=players[12], defense_left=players[13], defence_right=players[14])
line4 = models.Line(forward_left=players[15], forward_right=players[16], center=players[17], defense_left=players[18], defence_right=players[19])


team1 = models.Team(line1=line1, line2=line2, goaler=players[19], substitution=None)
team2 = models.Team(line1=line3, line2=line4, goaler=players[18], substitution=None)

game1 = models.Game(local_team=team1, visitor_team=team2, date='2024-09-03', location='arena1', referee=None, season=season_2024)


league_deschamps.games.append(game1)

# print(complete_data)

#game1 = models.Game(local_team, visitor_team, date, location, referee=None, season=None)