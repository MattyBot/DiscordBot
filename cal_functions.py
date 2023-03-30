
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = Credentials.from_authorized_user_file('cal_token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)


class GoogleCalendarEvents():

    def AddToCalendar(event_name, location, description, start_date, start_time, end_date, end_time):
        event_name = event_name
        location = location
        description = description
        start_date =start_date
        start_time = start_time
        end_date = end_date
        end_time = end_time
        
        event = {
            'summary': f'{event_name}',
            'location': f'{location}',
            'description': f'{description}',
            'start': {
                'dateTime': f'{start_date}T{start_time}:00-07:00', #YYYY-MM-DDTHH:mm:ss.000Z
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': f'{end_date}T{end_time}:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        event_link = (event.get('htmlLink'))
        event_id = event['id']
        
        print('Event created: %s' % (event.get('htmlLink')))
        print('Event ID: %s' % (event_id))

        return (event_link, event_id)

