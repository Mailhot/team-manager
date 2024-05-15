import sqlite3
from . import gsheet_link as gs_link


connection = sqlite3.connect('database.db')


with open('./team_manager/data/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

"""get all player list from db"""
df_data = gs_link.get_data(value='PLAYERS')
print('df_data', df_data)
data_dict = df_data.to_dict('records')
df_phones = df_data[['Grouped Name', 'Numero']]
print(df_phones.to_json(orient="records"))


for value in data_dict:
    # print(value['Numero'])
    cur.execute("INSERT INTO Players ('Grouped Name', Prenom, Nom, Rank, Positions, Numero, Jersey) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (value['Grouped Name'], value['Prenom'], value['Nom'], value['Rank'], value['Positions'], value['Numero'], value['Jersey'])
            )
connection.commit()

df_data = gs_link.get_data(value='SPARES')
data_dict = df_data.to_dict('records')

for value in data_dict:
    # print(value['Numero'])
    cur.execute("INSERT INTO Players ('Grouped Name', Prenom, Nom, Rank, Positions, Numero) VALUES (?, ?, ?, ?, ?, ?)",
            (value['Grouped Name'], value['Prenom'], value['Nom'], value['Rank'], value['Positions'], value['Numero'])
            )

connection.commit()
connection.close()