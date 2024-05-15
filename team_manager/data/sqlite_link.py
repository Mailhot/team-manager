import sqlite3
import config
from .. import models




def get_players_from_db():
    """get all player list from db"""
    conn = get_db_connection()
    curs = conn.cursor()
    players = curs.execute('SELECT * FROM Players').fetchall()
    conn.close()
    print('players', players)
    players_out = []
    for value in players:
            player1 = models.Player(mobile=value['Numero'], first_name=value['Prenom'], last_name=value['Nom'], positions=value['Positions'].split(','), rank=value['Rank'], jersey_number=None, language='fr')
            players_out.append(player1)
    return players_out


def get_db_connection():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    players = get_players_from_db()
    for player in players:
        print(player)
