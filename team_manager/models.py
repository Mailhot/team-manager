


class League():
	"""" a league class """
	def __init__(self,):
		self.players = []
		self.referee = []
		self.spares = []
		self.lines = {}
		self.games = {}
		self.lines = {}

class Season():
	"""a season class"""
	def __init__(self, start_date, stop_date, name):
		super(Season, self).__init__()
		self.start_date = start_date
		self.stop_date = stop_date
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
	def __init__(self, forward_left, forward_right, center, defense_left, defence_right):
		super(Line, self).__init__()
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

		
		
		


		