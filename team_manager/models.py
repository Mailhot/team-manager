from datetime import datetime, timedelta
import config
from . import helpers
from .data import twilio_link
import pandas as pd
from jinja2 import Environment, FileSystemLoader

class League():
    """" a league class """
    def __init__(self,):
        self.players = []
        self.referee = []
        self.spares = []
        self.lines = {}
        self.seasons = []
        self.games = {}
        self.lines = {}
        self.default_routing = [((0, 1), (2, 3)),
                                ((0, 2), (1, 3)), 
                                ((0, 3), (1, 2)), 
                                ((2, 3), (0, 1)),
                                ((1, 3), (0, 2)),
                                ((1, 2), (0, 3)),
                                ((1, 0), (3, 2)),
                                ((2, 0), (3, 1)), 
                                ((3, 0), (2, 1)), 
                                ((3, 2), (1, 0)),
                                ((3, 1), (2, 0)),
                                ((2, 1), (3, 0)),
                                ]


    def generate_games(self, season, weekday, time, routing=None, filter_=None):
        """generate a series of game based on a season, day of week and time, line group instance"""
        # filter: list of date (2024-01-01) that needs to be filtered out from the calendar.
        print(self.default_routing)
        if routing == None:
            routing = self.default_routing
        # generate games dates from season.
        start, end = season.start_date, season.stop_date
        days = (start + timedelta(days=i) for i in range((end - start).days + 1))
        l = [d for d in days if d.weekday() in [1]]
        # print(l)

        k = 0
        i = 1
        
        for date in l:
            date_filtered_out = False
            for filtered_date_str in filter_:
                filtered_date = datetime.strptime(filtered_date_str, '%Y-%m-%d').date()
                # print(type(filtered_date), type(date))
                # print(filtered_date, date, filtered_date == date)
                if filtered_date == date:
                    date_filtered_out = True
                    break

            if date_filtered_out == True:
                continue

            this_routing = routing[k]
            team1 = Team(line1=self.lines.get(this_routing[0][0]), line2=self.lines.get(this_routing[0][1]), goaler=self.players[21], substitution=None)
            team2 = Team(line1=self.lines.get(this_routing[1][0]), line2=self.lines.get(this_routing[1][1]), goaler=self.players[20], substitution=None)

            game1 = Game(teams={'local': team1, 'visitor': team2}, date=date, time=time, location=config.default_location, referee=None, season=season)
            self.games[i] = game1
            k += 1
            i += 1
            # Restart loop if outside of routing length
            if k > (len(routing) - 1):
                k = 0
        self.seasons.append(season)

    def send_reminder(self, ):
        # TODO: find the next game, Check attendance
        pass

    def set_player(self, number_of_game):
        # TODO: 
        pass



    def replace_player(self, player, request_datetime=datetime.now(), games=1, spare=None):
        # This function will replace a player for a number of upcomming games
        # TODO: get games (number 1 = number of games )
        # TODO: get player
        # TODO: get substitute if not NOne
        # TODO: Replace player by substitute in those games
        # TODO: if Substitute = None, Get substitute from list
        # TODO: Contact Substitute in classified suitability order.
        # TODO: If substitute confirmed, replace player
        player_class = self.get_player(player)
        if spare != None:
            spare_class = self.get_spare(spare)
            print('spare found:', spare_class)
        else:
            spare_class = None
        
        next_games, _ = self.get_next_game(request_datetime=request_datetime, games=games)
        for game_ in next_games:
            game_.replacements[player_class] = spare_class

    def get_player(self, first_name, last_name=None):
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

    def get_spare(self, first_name, last_name=None):
        positive_match = []
        for spare in self.spares:
            if first_name.lower() in spare.first_name.lower():
                positive_match.append(spare)

        if len(positive_match) > 1:
            print('too many results')
            for spare in positive_match:
                print(spare)
            return None

        elif len(positive_match) == 1:
            return positive_match[0]

    def get_next_game(self, request_datetime=datetime.now(), games=1):
        games_out = []
        games_keys = []
        for game_key in self.games.keys(): #TODO: probably add a sorted
            game = self.games[game_key]
            print(request_datetime)
            if not game.date <= request_datetime.date(): #TODO: this is not robust if the key are not in order
                if games == 1:
                    return [game], game_key
                else:
                    games_out.append(game)
                    games_keys.append(game_key)
                    if len(games_out) == games:
                        return games_out, games_keys


    def find_spare(self, request_datetime=datetime.now(), games=1,):
        # find players to replace available spots
        # TODO: check for the next game or number of next games chosen, 
        # Send invitation to players (log result sending and receiving)
        """
        THis function check the database for spare on the next game, 
        It will check if a change has happened by looking at the sqlite db variable: msgIn date_ variable.
        If no change happened in the config.NO_NEWS_DELAY time, we contact a new spare.
        request_datetime: the date and time at which the find_spare is requested
        games: the number of games from the requested request_datetime to be replaced
        """

        print()
        next_game, _ = self.get_next_game(request_datetime, games)
        

        for game_ in next_game:
            # If no spare list have been created for the next game, create one
            if not isinstance(game_.spares, pd.DataFrame):
                game_.spares = helpers.get_spares(player=None)

            print(f'Finding spares for game', game_)
            # Find matching spare in the spare list for the next game.
            for key in game_.replacements:
                if game_.replacements[key] == None:
                    print(key)
                    to_contact_spare = game_.get_spares(player=key, contacted=False)
                    to_contact_row = to_contact_spare.iloc[0]
                    # TODO: Send invitation to player
                    twilio_link.send_message(to_contact_row['Numero'], 
                        f"Salut {to_contact_row['Prenom']} pourrais-tu remplacer Mardi {game_.time} au {game_.location}")
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
        next_game, _ = self.get_next_game(games=games)
        for game_ in next_game:
            if not isinstance(game_.spares, pd.DataFrame):
                print('Error: no spare list created yet, you need to run find_spare first?')
                twilio_link.send_message(number, 'Spare not yet open for next game')

            game_.spares.loc[game_.spares['Numero'].str.contains(number), 'Available'] = available

            print(game_.spares)


    def check_and_confirm(self,):
        # check spare list, mark available as confirmed if possible
        print()
        print('checking spare')
        next_game, _ = self.get_next_game(games=1)
        for game_ in next_game:
            if not isinstance(game_.spares, pd.DataFrame):
                print('Error: no spare list created yet, you need to run find_spare first?')
                print('skipped')
                return ''
            
            # print(available_spares)
            for key in game_.replacements.keys():
                print('----------------------', game_.replacements)
                if game_.replacements[key] == None:
                    # print(key)
                    to_contact_spares = game_.get_spares(player=key, contacted=True)
                    to_contact_spares_available = to_contact_spares.loc[to_contact_spares['Available'] == True, :]
                    to_contact_spares_not_confirmed = to_contact_spares_available.loc[to_contact_spares_available['Confirmed'] != True, :]
                    # print('to_contact_spares_not_confirmed', to_contact_spares_not_confirmed)
                    to_contact_row = to_contact_spares_not_confirmed.iloc[0]
                    # print('to contact row', to_contact_row)
                    twilio_link.send_message(to_contact_row['Numero'], f"Salut {to_contact_row['Prenom']} tu est confirmer pour le match de Mardi a {game_.time} a {game_.location}")
                
                    game_.replacements[key] = to_contact_row['Grouped Name'] # TODO: the get spare function does not work so we just use the name for now.
                    # set the confirmed spare as confirmed
                    game_.spares.loc[game_.spares['Numero'].str.contains(to_contact_row['Numero']), 'Confirmed'] = True
                    print('new game spare list')
                    print(game_.spares)

                    
    def print_game_sheet(self, number):
        # number: Number of games to be printed
        next_game, game_key = self.get_next_game(games=number)

        environment = Environment(loader=FileSystemLoader(config.TEMPLATE_DIR))
        template = environment.get_template("rooster_template.html")

        for i in range(len(next_game)):
            game = next_game[i]
            key = game_key[i]

            filename = f"lineup_{game.date}.html"
            content = template.render(
                game=game.__dict__,
                game_number=key
            )
            with open(filename, mode="w", encoding="iso-8859-1") as message:
                message.write(content)
                print(f"... wrote {filename}")

    def print_year_sheet(self):
        # number: Number of games to be printed
        games = self.games

        environment = Environment(loader=FileSystemLoader(config.TEMPLATE_DIR))
        template = environment.get_template("game_list_template.html")

        filename = f"Horaire_{self.seasons[-1].name}.html"
        # Split the dictionary by half using
        # the list comprehension
        half_no = len(games) // 2
        games_first_half = {k: v for i, (k, v) in enumerate(games.items()) if i <= half_no}
        games_second_half = {k: v for i, (k, v) in enumerate(games.items()) if i > half_no}

        content = template.render(
                games1=games_first_half,
                games2=games_second_half,
                season=self.seasons[-1].name,
                half_season=half_no,

            )

        with open(filename, mode="w", encoding="iso-8859-1") as message:
                message.write(content)
                print(f"... wrote {filename}")


    def line_recap(self):
        # get a recap of every line and how much they played against each other.
        # with this pretty equal, the team play equally as local, as first line.
        result = {'Ligne 1': {'Local team': 0, 'index': 0},
                    'Ligne 2': {'Local team': 0, 'index': 0},
                    'Ligne 3': {'Local team': 0, 'index': 0},
                    'Ligne 4': {'Local team': 0, 'index': 0},
                    }

        # we count games where the line is local and where the line is the first line of a team.
        for game_key in self.games.keys():
            result[self.games[game_key].teams['local'].line1.name]['Local team'] += 1
            result[self.games[game_key].teams['local'].line1.name]['index'] += 1
            result[self.games[game_key].teams['local'].line2.name]['Local team'] += 1
            result[self.games[game_key].teams['visitor'].line1.name]['index'] += 1
        print(result)


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
        print('Goaler:', self.teams['local'].goaler)
        
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
        print('Goaler:', self.teams['visitor'].goaler)
        print()


    def get_spares(self, player, contacted=False):
        # print(self.spares)

        df_data = self.spares[self.spares['Contacted'] == contacted]
        df_data = df_data.loc[df_data['Available'] != False] # Do not select spare that are set as unavailable
        # print('df_data1', df_data)

        df_data['rank_diff'] = df_data.apply(lambda x: helpers.get_rank_diff(player_rank=player.rank, spare_rank=x['Rank']), axis=1)
        df_data.loc[:, 'position_match'] = df_data.apply(lambda x: helpers.position_match(player.position, x['Positions']), axis=1)
        df_data['rank_diff'] = df_data['rank_diff'].abs()
        df_data = df_data.sort_values(['position_match', 'rank_diff', 'Favoriteness'], ascending=[False, True, True])
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
        self.grouped_name = first_name + last_name
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


        
        
        


        