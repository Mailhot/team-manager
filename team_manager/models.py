from datetime import datetime, timedelta
import config
from . import helpers
from .data import twilio_link
import pandas as pd

class League():
	"""" a league class """
	def __init__(self,):
		self.players = []
		self.referee = []
		self.spares = []
		self.lines = {}
		self.games = {}
		self.lines = {}
		self.default_routing = [((0, 1), (2, 3)),
								((0, 2), (1, 3)), 
								((0, 3), (1, 2)), 
								((2, 3), (0, 1)),
								((1, 3), (0, 2)),
								((1, 2), (0, 3)),
								]


	def generate_games(self, season, weekday, time, routing=None):
		"""generate a series of game based on a season, day of week and time, line group instance"""
		print(self.default_routing)
		if routing == None:
			routing = self.default_routing
		# generate games dates from season.
		start, end = season.start_date, season.stop_date
		days = (start + timedelta(days=i) for i in range((end - start).days + 1))
		l = [d for d in days if d.weekday() in [1]]
		# print(l)

		k = 0
		i = 0
		for date in l:
			this_routing = routing[k]
			team1 = Team(line1=self.lines.get(this_routing[0][0]), line2=self.lines.get(this_routing[0][1]), goaler=None, substitution=None)
			team2 = Team(line1=self.lines.get(this_routing[1][0]), line2=self.lines.get(this_routing[1][1]), goaler=None, substitution=None)

			game1 = Game(teams={'local': team1, 'visitor': team2}, date=date, time=time, location=config.default_location, referee=None, season=season)
			self.games[i] = game1
			k += 1
			i += 1
			# Restart loop if outside of routing length
			if k > (len(routing) - 1):
				k = 0

	def send_reminder(self, ):
		# TODO: find the next game, Check attendance
		pass

	def set_player(self, number_of_game):
		# TODO: 
		pass



	def replace_player(self, player, games=1, spare=None):
		# This function will replace a player for a number of upcomming games
		# TODO: get games (number 1 = number of games )
		# TODO: get player
		# TODO: get substitute if not NOne
		# TODO: Replace player by substitute in those games
		# TODO: if Substitute = None, Get substitute from list
		# TODO: Contact Substitute in classified suitability order.
		# TODO: If substitute confirmed, replace player
		player_class = self.get_player(player)
		next_games = self.get_next_game(games)
		for game_ in next_games:
			game_.replacements[player_class] = spare
		# for key in next_game.teams.keys():
		# 	# next_game.teams[key]
		# 	for player_key in next_game.teams[key].line1.players.keys():
		# 		if player_class == next_game.teams[key].line1.players[player_key]:
		# 			next_game.teams[key].line1.players[player_key] = spare
		# 			print('player changed:', next_game.date, player, spare)
		# 	for player_key in next_game.teams[key].line2.players.keys():
		# 		if player_class == next_game.teams[key].line2.players[player_key]:
		# 			next_game.teams[key].line2.players[player_key] = spare
		# 			print('player changed:', next_game.date, player, spare)
	
	def get_player(self, first_name):
		positive_match = []
		for player in self.players:
			if first_name.lower() in player.first_name.lower():
				positive_match.append(player)

		if len(positive_match) > 1:
			print('too many results')
			for player in positive_match:
				print(player)
			return None

		if len(positive_match) == 1:
			return positive_match[0]

	def get_spare(self, first_name, last_name):
		positive_match = []
		for spare in self.spares:
			if first_name.lower() in player.first_name.lower():
				positive_match.append(player)

		if len(positive_match) > 1:
			print('too many results')
			for player in positive_match:
				print(player)
			return None

		if len(positive_match) == 1:
			return positive_match[0]

	def get_next_game(self, games=1):
		games_out = []
		for game_key in self.games.keys(): #TODO: probably add a sorted
			game = self.games[game_key]
			if not game.date < datetime.now().date(): #TODO: this is not robust if the key are not in order
				if games == 1:
					return [game]
				else:
					games_out.append(game)
					if len(games_out) == games:
						return games_out


	def find_spare(self, games=1,):
		# find players to replace available spots
		# TODO: check for the next game or number of next games chosen, 
		# Send invitation to players (log result sending and receiving)
		"""
		THis function check the database for spare on the next game, 
		It will check if a change has happened by looking at the sqlite db variable: msgIn date_ variable.
		If no change happened in the config.NO_NEWS_DELAY time, we contact a new spare.
		"""

		print()
		next_game = self.get_next_game(games)
		

		for game_ in next_game:
			# If no spare list have been created for the next game, create one
			if not isinstance(game_.spares, pd.DataFrame):
				game_.spares = helpers.get_spares(player=None)

			print(f'Finding spares for game', game_)
			# Find matching spare in the spare list for the next game.
			for key in game_.replacements:
				if game_.replacements[key] == None:
					print(key)
					to_contact_spare = game_.get_spares(player=key)
					to_contact_row = to_contact_spare.iloc[0]
					# twilio_link.pushover(numbers=[to_contact_spare.at[0, 'Numero']], 'Peut-tu remplacer au hockey ce mardi 20:00 au centre civic?')
					# TODO: Send invitation to player
					twilio_link.send_message(to_contact_row['Numero'], f"Hey {to_contact_row['Prenom']} can you replace next Tuesday at 19:00")
					game_.spares.loc[game_.spares['Grouped Name'] == to_contact_row['Grouped Name'], 'Contacted'] = True

					print(game_.spares)


	def set_player_present(self, player, games=1):
		print()
		next_game = self.get_next_game(games)

		for game_ in next_game:
			print(f'setting player')
			game_.spares.loc['']


	def set_spare_availability(self, number, available=False, games=1):
		print()
		print('setting spare available', number)
		next_game = self.get_next_game(games)
		for game_ in next_game:
			if not isinstance(game_.spares, pd.DataFrame):
				print('Error: no spare list created yet, you need to run find_spare first?')
				twilio_link.send_message(number, 'Spare not yet open for next game')

			game_.spares.loc[game_.spares['Numero'].str.contains(number), 'Available'] = available

			print(game_.spares)


	def check_and_confirm(self,):
		print()
		print('checking spare')
		next_game = self.get_next_game(1)
		for game_ in next_game:
			if not isinstance(game_.spares, pd.DataFrame):
				print('Error: no spare list created yet, you need to run find_spare first?')
				print('skipped')
				return ''
			
			# print(available_spares)
			for key in game_.replacements:
				if game_.replacements[key] == None:
					print(key)
					to_contact_spares = game_.get_spares(player=key)
					to_contact_spares_available = to_contact_spares.loc[to_contact_spares['Available'] == True, :]
					print('to_contact_spares', to_contact_spares)
					to_contact_row = to_contact_spares.iloc[0]
class Season():
	"""a season class"""
	def __init__(self, start_date, stop_date, name):
		super(Season, self).__init__()
		self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
		self.stop_date = datetime.strptime(stop_date, '%Y-%m-%d').date()
		self.name = name

		self.games = {}

	def __repr__(self):
		return f'{self.name} start: {self.start_date}, end: {self.stop_date}'

		

class Game():
	"""a game class"""
	def __init__(self, teams, date, time, location, referee=None, season=None, results=None, spares=None):
		self.teams = teams
		self.date = date
		self.time = time
		self.location = location
		self.referee = referee
		self.season = season
		self.spares = spares #dataframe of spare players

		self.replacements = {} # a dict with players: substitute values for replacement


	def print(self):

		print(self.season)
		print(self.date, self.time, self.location)
		
		print('Local team:')
		print(self.teams['local'].line1.name)
		for player_key in self.teams['local'].line1.players.keys():
			default_player = self.teams['local'].line1.players[player_key]
			if default_player in self.replacements.keys():
				player=self.replacements[default_player]
				print(player_key, default_player, '>', player)
			else:
				player=default_player

				print(player_key, player)

		print(self.teams['local'].line2.name)
		for player_key in self.teams['local'].line2.players.keys():
			default_player = self.teams['local'].line2.players[player_key]
			if default_player in self.replacements.keys():
				player=self.replacements[default_player]
				print(player_key, default_player, '>', player)
			else:
				player=default_player

				print(player_key, player)
		
		print()
		print('Visitor team:')
		print(self.teams['visitor'].line1.name)
		for player_key in self.teams['visitor'].line1.players.keys():
			default_player = self.teams['visitor'].line1.players[player_key]
			if default_player in self.replacements.keys():
				player=self.replacements[default_player]
				print(player_key, default_player, '>', player)
			else:
				player=default_player
				print(player_key, player) 
				
		print(self.teams['visitor'].line2.name)
		for player_key in self.teams['visitor'].line2.players.keys():
			default_player = self.teams['visitor'].line2.players[player_key]
			if default_player in self.replacements.keys():
				player=self.replacements[default_player]
				print(player_key, default_player, '>', player)
			else:
				player=default_player

				print(player_key, player)
		print()


	def get_spares(self, player):
		# print(self.spares)

		df_data = self.spares[self.spares['Contacted'] == False]

		df_data['rank_diff'] = df_data.apply(lambda x: helpers.get_rank_diff(player_rank=player.rank, spare_rank=x['Rank']), axis=1)
		df_data.loc[:, 'position_match'] = df_data.apply(lambda x: helpers.position_match(player.position, x['Positions']), axis=1)
		df_data = df_data.sort_values(['position_match', 'rank_diff'], ascending=False)
		print()
		print('replacement for ', player)
		print(df_data)
		return df_data

			

		







class Team():
	"""a team class"""
	def __init__(self,  line1, line2, goaler, substitution=None):

		self.line1 = line1
		self.line2 = line2
		self.goaler = goaler
		self.substitution = substitution



class Line():
	"""a line class (3 offence and 2 defence)"""
	def __init__(self, name, forward_left, forward_right, center, defense_left, defence_right):
		self.name = name
		self.players = {}
		self.players['forward_left'] = forward_left
		self.players['forward_right'] = forward_right
		self.players['center'] = center
		self.players['defense_left'] = defense_left
		self.players['defence_right'] = defence_right

		

class User():
	"""a member class for the league"""
	def __init__(self, mobile, first_name, last_name, position, rank, jersey_number, language='fr'):
		self.mobile = mobile
		self.first_name = first_name
		self.last_name = last_name
		self.position = position
		self.rank = rank
		self.jersey_number = jersey_number
		self.language = language

class Player(User):
	"""A player class from a member"""
	def __init__(self, mobile, first_name, last_name, positions, rank, jersey_number, language):
		super().__init__(mobile, first_name, last_name, positions, rank, jersey_number, language)
		self._type = 'player'
		self.grouped_name = first_name + last_name

	def __repr__(self):
		return f'{self.first_name} {self.last_name} '

class Spare(User):
	"""docstring for Spare"""
	def __init__(self, mobile, first_name, last_name, positions, rank, favoriteness=3, jersey_number=None, language='fr'):
		super().__init__(mobile, first_name, last_name, positions, rank, jersey_number, language)
		self._type = 'spare'
		self.favoriteness = favoriteness

	def __repr__(self):
		return f'{self.first_name} {self.last_name} '

class Referee(User):
	"""docstring for Referee"""
	def __init__(self):
		super(Referee, self).__init__()
		self._type = 'referee'
		self.position = None
		self.rank = None
		self.jersey_number = None


		
		
		


		