import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
# import pickle
import config


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']   #['https://www.googleapis.com/auth/spreadsheets', ]#'https://www.googleapis.com/auth/documents']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = config.SAMPLE_SPREADSHEET_ID_input


sheet_data_dict = {'SPARES': config.SPARES,
                'PLAYERS': config.PLAYERS,
                }
                # 'REPLACEMENT': config.REPLACEMENT, 
                # 'ALIGNMENT': config.ALIGNMENT, 
                # 'SCHEDULE': config.SCHEDULE,
                # }

SPARES = config.SPARES
PLAYERS = config.PLAYERS
REPLACEMENT = config.REPLACEMENT
ALIGNMENT = config.ALIGNMENT
SCHEDULE = config.SCHEDULE

def get_creds_or_create():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(config.token_location):
        creds = Credentials.from_authorized_user_file(config.token_location, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(config.token_location, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_data(value=None):
    """ Get data from a google sheet based on a 'value':
    value: a string that is a key to sheet_data to determine what value you want, currently SPARES or PLAYERS
    output: return a dataframe with the google sheet data, empty values are replaced with None.
    """

    global values_input, service

    if value == None: 
        sheet_data = [SPARES, PLAYERS] #, REPLACEMENT, ALIGNMENT, SCHEDULE]
    
    elif type(value) == list:
        sheet_data = []
        for element in value:
            sheet_data.append(sheet_data_dict[element])
    elif type(value) == str:
        sheet_data = [sheet_data_dict[value]]


    creds = get_creds_or_create()
    service1 = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API
    sheet = service1.spreadsheets()
    sheet_data_output = {}
    for element in sheet_data:
        result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                    range=element).execute()

        values_input = result_input.get('values', [])
        # remplce incomplete lines with None values
        for key, value_ in enumerate(values_input):

            if len(value_) < len(values_input[0]):
                none_list = [None] * (len(values_input[0]) - len(value_))
                value_ += none_list

        # print('values:', values_input)
        if not values_input:
            print('No data found.')

        df=pd.DataFrame(values_input[1:], columns=values_input[0])
        # print('sheet_data_output', sheet_data_output, df)
        # print('result_input', result_input)
        sheet_data_output[result_input['range'].split('!')[0]] = df
        # sheet_data_output[]
        # print(sheet_data_output)

        if len(sheet_data_output.keys()) == 1:
            if 'Players' in sheet_data_output.keys():
                sheet_data_output = sheet_data_output['Players']
            elif 'Spares' in sheet_data_output.keys():
                sheet_data_output = sheet_data_output['Spares']

    return sheet_data_output


def create(title):
  """
  Creates the Sheet the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = get_creds_or_create()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    spreadsheet = {"properties": {"title": title}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
    print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
    return spreadsheet.get("spreadsheetId")
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error



  
if __name__ == '__main__':
    #create("mysheet1")
    df_list = get_data('SPARES')
    print(df_list)

    # for key in df_list.keys():
    #     print()
    #     print(key)
    #     print(df_list[key])
