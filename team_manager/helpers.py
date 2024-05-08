from .data import gsheet_link as gs_link
from . import helpers
from . import models


numeric_rank_dict = {'AAA': 1,
       				'AA':2, 
       				'BB':3,
       				'CC':4, 
       				'A': 5,
       				'B': 6,
       				'C': 7, 
       				'D': 8,
       				'E': 9, 
       				'F': 10,
       				}

def get_players():
	"""get all player list from gsheet"""
	df_data = gs_link.get_data(value='PLAYERS')
	print('df_data', df_data)
	data_dict = df_data.to_dict('records')
	df_phones = df_data[['Grouped Name', 'Numero']]
	print(df_phones.to_json(orient="records"))
	
	players_out = []
	for value in data_dict:
		print(value['Numero'])
		player1 = models.Player(mobile=value['Numero'], first_name=value['Prenom'], last_name=value['Nom'], positions=value['Positions'].split(','), rank=value['Rank'], jersey_number=None, language='fr')
		players_out.append(player1)

	# print(players_out)
	return players_out

def get_rank_diff(player_rank, spare_rank):
	# convert rank to numeric value
	spare_rank_number = numeric_rank_dict[spare_rank]
	player_rank_number = numeric_rank_dict[player_rank]
	# calculate difference with player rank
	return player_rank_number - spare_rank_number

def position_match(player_positions, spare_positions):
	# takes a player position list and a spare position list and will return if there is a position match or not.
	print(player_positions, spare_positions)
	return any(b in player_positions for b in spare_positions)


def get_spares(player=None):
	''' get spares list from gsheet '''
	df_data = gs_link.get_data(value='SPARE')
	df_data['Positions'] = df_data['Positions'].apply(lambda x: x.split(','))
	# sort dataframe by rank and position
	df_data['rank_diff'] = df_data.apply(lambda x: get_rank_diff(player_rank=player.rank, spare_rank=x['Rank']), axis=1)
	df_data['position_match'] = df_data.apply(lambda x: position_match(player.position, x['Positions']), axis=1)
	df_data = df_data.sort_values(['position_match', 'rank_diff'], ascending=False)
	# print(df_data)
	# df_data['rank_diff'] = numeric_rank_dict[player.rank] - df_data['Rank']
	data_dict = df_data.to_dict('records')
	print('df_data', df_data)
	players_out = []
	for value in data_dict:
		print(value['Numero'])
		player1 = models.Spare(mobile=value['Numero'], first_name=value['Prenom'], last_name=value['Nom'], positions=value['Positions'], rank=value['Rank'], language='fr')
		players_out.append(player1)



	# print(players_out)
	return players_out

if __name__ == '__main__':
	get_players()