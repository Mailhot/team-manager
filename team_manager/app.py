
from .data import gsheet_link as gs_link


def check_replacement():
	df_data = gs_link.get_data()

	for index, row in df_data['Replacement'].iterrows():
		if row['Remplacant'] == None:
			print('YES', row['Remplacant'])
	return df_data

def replace_player(player):
	pass

if __name__ == "__main__":
	df_data = check_replacement()
	# print(df_data)