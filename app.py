import os

from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

ID="1TntCc3pojmkvl3sjU79Ar4rnOeidoUT1iGZrsc5xdFo"

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json",SCOPE)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPE)
            credentials = flow.run_local_server(port=0)
        with open("token.json","w") as token:
            token.write(credentials.to_json())
    try:
        service = build("sheets","v4",credentials=credentials)
        sheets = service.spreadsheets()

        for row in range(2,10):
            num1 = sheets.values().get(spreadsheetId=ID,range=f"Sheet1!A{row}").execute().get("values")[0][0]
            num2 = sheets.values().get(spreadsheetId=ID,range=f"Sheet1!B{row}").execute().get("values")[0][0]
            calc_result=num1+num2
            print(f"Processing {type(calc_result)}")
            sheets.values().update(spreadsheetId=ID,range=f"Sheet1!C{row}",valueInputOption="USER_ENTERED", body={"values":[[f"{calc_result}"]]}).execute()
        # result = sheets.values().get(spreadsheetId=ID,range="Sheet1!A1:B3").execute()

        # values = result.get("values",[])
        # print("Here\n",values,"\n here")

    
    except HttpError as error:
        print(error)

if __name__ == "__main__":
    main()
