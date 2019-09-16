import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the database spreadsheet.
google_sheet_id = ''
data_range = 'Sheet1!A1:B'

def google_lookup():

    """This function uses saved local credentials to access a spreadsheet
    and saves the specified range as a JSON response to be used later
    The credentials and auth portion is copied from the google sheets python tutorial
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API to get spreadsheet as JSON
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=google_sheet_id, range=data_range).execute()

    #Write Json to file to be read later
    with open('data.txt', 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False)
    return


if __name__ == "__main__":
    google_lookup()
