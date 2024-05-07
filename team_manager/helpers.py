from .data import gsheet_link as gs_link
from . import helpers
from . import models

def get_players():
	"""get all player list from gsheet"""
	df_data = gs_link.get_data(value='PLAYERS')
	data_dict = df_data.to_dict('records')
	print('df_data', df_data)
	players_out = []
	for value in data_dict:
		print(value['Numero'])
		player1 = models.Player(mobile=value['Numero'], first_name=value['Prenom'], last_name=value['Nom'], position=None, rank=None, jersey_number=None, language='fr')
		players_out.append(player1)

	# print(players_out)
	return players_out

def get_spares():
	''' get spares list from gsheet '''
	df_data = gs_link.get_data(value='SPARE')
	data_dict = df_data.to_dict('records')
	print('df_data', df_data)
	players_out = []
	for value in data_dict:
		print(value['Numero'])
		player1 = models.Spare(mobile=value['Numero'], first_name=value['Prenom'], last_name=value['Nom'], position=None, rank=None, jersey_number=None, language='fr')
		players_out.append(player1)

	# print(players_out)
	return players_out