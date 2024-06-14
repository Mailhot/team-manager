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
            player1 = models.Player(mobile=value['Numero'], first_name=value['Prenom'], 
                last_name=value['Nom'], positions=value['Positions'].split(','), 
                rank=value['Rank'], jersey_number=None, language='fr',
                )
            players_out.append(player1)
    return players_out

def get_spares_from_db():
    """get all spares list from db"""
    conn = get_db_connection()
    curs = conn.cursor()
    spares = curs.execute('SELECT * FROM Spares').fetchall()
    conn.close()
    # print('spares-', spares)
    spares_out = []
    for value in spares:
            spare1 = models.Spare(mobile=value['Numero'], first_name=value['Prenom'], 
                last_name=value['Nom'], positions=value['Positions'].split(','), 
                rank=value['Rank'], favoriteness=value['Favoriteness'], 
                jersey_number=None, language='fr',
                )
            spares_out.append(spare1)
    return spares_out

def get_db_connection():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_msg_check_datetime():
    conn = get_db_connection()
    curs = conn.cursor()
    parameter = curs.execute("SELECT date_ FROM Parameters WHERE name = 'msgIn'").fetchone()
    return parameter['date_']


if __name__ == "__main__":
    players = get_players_from_db()
    print('players')
    for player in players:
        print(player)
    print()
    print('spares')
    spares = get_spares_from_db()
    for spare in spares:
        print(spare)

    print()
    print('last check time', get_msg_check_datetime())
