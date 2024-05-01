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
		if routing == None:
			routing == self.default_routing
		# generate games dates from season.
		start, end = season.start_date, season.stop_date
		days = (start + timedelta(days=i) for i in range((end - start).days + 1))
		l = [d for d in days if d.weekday() in [1] ]

		k = 0
		for date in l:
			this_routing = routing[k]
			team1 = Team(line1=this_routing[0][0], line2=this_routing[0][1], goaler=players[19], substitution=None)
			team2 = Team(line1=this_routing[1][0], line2=this_routing[1][1], goaler=players[18], substitution=None)

			game1 = Game(local_team=team1, visitor_team=team2, date=date, location=config.default_location, referee=None, season=season)
			self.games[k] = game1
			k += 1
			# Restart loop if outside of routing length
			if k > (len(routing) - 1):
				k = 0



class Season():
	"""a season class"""
	def __init__(self, start_date, stop_date, name):
		super(Season, self).__init__()
		self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
		self.stop_date = datetime.strptime(stop_date, '%Y-%m-%d').date()
		self.name = name

		self.games = {}

		

class Game():
	"""a game class"""
	def __init__(self, local_team, visitor_team, date, location, referee=None, season=None):
		super(Game, self).__init__()
		self.local_team = local_team
		self.visitor_team = visitor_team
		self.date = date
		self.location = location
		self.referee = referee
		self.season = season

class Team():
	"""a team class"""
	def __init__(self,  line1, line2, goaler, substitution=None):
		super(Team, self).__init__()
		self.line1 = line1
		self.line2 = line2
		self.goaler = goaler
		self.substitution = substitution

class Line():
	"""a line class (3 offence and 2 defence)"""
	def __init__(self, name, forward_left, forward_right, center, defense_left, defence_right):
		self.name = name
		self.forward_left = forward_left
		self.forward_right = forward_right
		self.center = center
		self.defense_left = defense_left
		self.defence_right = defence_right
		

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

class Substitute(User):
	"""docstring for Substitute"""
	def __init__(self, ):
		super(Substitute, self).__init__()
		self._type = 'substitute'

class Referee(User):
	"""docstring for Referee"""
	def __init__(self):
		super(Referee, self).__init__()
		self._type = 'referee'
		self.position = None
		self.rank = None
		self.jersey_number = None

		
		
		


		