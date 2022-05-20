from os import path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# IF YOU MODIFY THE SCOPE DELETE THE TOKEN.TXT FILE
SCOPES = ['https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar']

# THE TOKEN.TXT FILE STORES UPDATE AND USER ACCESS TOKENS


def get_crendetials_google():
    # OPEN THE BROWSER TO AUTHORIZE
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # WE SAVE THE CREDENTIALS
    pickle.dump(creds, open("token.txt", "wb"))
    return creds

# THIS ALLOWS US TO INTERACT WITH ALL GOOGLE APIS, IN THIS CASE CALENDAR

def get_calendar_service():
    creds = None
    if path.exists("token.txt"):
        creds = pickle.load(open("token.txt", "rb"))
    # IF IT EXPIRED, WE REFRESH THE CREDENTIALS
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = get_crendetials_google()

    service = build("calendar", "v3", credentials=creds)

    return service


# METHODS

service = get_calendar_service()

# CREATE EVENT

template = {
  "summary": "Important event!",
  # "location": "Virtual event (Slack)",
  "description": "This a description",
  "start": {
    "date": "2022-4-27",
    # "dateTime": "2022-4-27T00:00:00",
    "timeZone": "Asia/Taipei"
  },
  "end": {
    "date": "2022-4-27",
    # "dateTime": "2022-4-27T00:00:00",
    "timeZone": "Asia/Taipei"
  },
  "attendees": [{ "email": "email@gmail.com" }],
  "reminders": {
    "useDefault": False,
    "overrides": [
      { "method": "email", "minutes": 30 },
      # { "method": "popup", "minutes": 10 }
    ]
  }
}

def create_event(template: dict):
    try:
        response = service.events().insert(calendarId="primary", body=template).execute()
        return response
    except Exception as e:
        return e.message

# GET EVENT BY ID


def get_event(eventId: str):
    try:
        response = service.events().get(calendarId="primary", eventId=eventId).execute()
        return response
    except Exception as e:
        return e.message

# UPDATE EVENT


def update_event(eventId: str, template: dict):
    try:
        response = service.events().update(calendarId='primary',
                                           eventId=eventId, body=template).execute()
        return response
    except Exception as e:
        return e.message

# DELETE EVENT BY ID


def delete_event(eventId: str):
    try:
        response = service.events().delete(calendarId="primary", eventId=eventId).execute()
        return response
    except Exception as e:
        return e.message


create_event(template)