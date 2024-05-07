from datetime import datetime, timedelta
import config


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
		next_game = self.get_next_game()
		next_game.replacements[player_class] = spare
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


	def get_next_game(self,):
		for game_key in self.games.keys():
			game = self.games[game_key]
			if not game.date < datetime.now().date():
				return game

	def find_player(self, games=1,):
		# find players to replace available spots
		# TODO: check for the next game or number of next games chosen, 
		# Find replacement for those games, check spare, and sort by properness of class and favoriteness
		# Offer thos players to replace

		next_game = self.get_next_game()
		for key in next_game.replacements:
			if next_game.replacements[key] == None:
				pass # replace player



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
	def __init__(self, teams, date, time, location, referee=None, season=None, results=None):
		self.teams = teams
		self.date = date
		self.time = time
		self.location = location
		self.referee = referee
		self.season = season

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

	def replace_player(self, player_name, spare_name):
		# TODO: find the player in the current player list, make sure it's the only result. 
		# find the spare in the spare list
		# replace the player in it's position with the spare. 
		pass





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
	def __init__(self, mobile, first_name, last_name, position, rank, jersey_number, language):
		User.__init__(self, mobile, first_name, last_name, position, rank, jersey_number, language)
		self._type = 'player'

	def __repr__(self):
		return f'{self.first_name} {self.last_name} '

class Spare(User):
	"""docstring for Spare"""
	def __init__(self, ):
		super(Spare, self).__init__()
		self._type = 'spare'

class Referee(User):
	"""docstring for Referee"""
	def __init__(self):
		super(Referee, self).__init__()
		self._type = 'referee'
		self.position = None
		self.rank = None
		self.jersey_number = None


		
		
		


		