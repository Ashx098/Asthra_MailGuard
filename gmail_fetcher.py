import os.path
import csv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_and_export_emails(service, max_results=500, output_file='emails.csv'):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    data = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload']['headers']
        subject = sender = date = snippet = None

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Date':
                date = header['value']

        snippet = msg_data.get('snippet')
        data.append([sender, subject, snippet, date, ""])  # Last column = label (to be filled manually)

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Sender', 'Subject', 'Snippet', 'Date', 'Label'])
        writer.writerows(data)

    print(f"✅ Exported {len(data)} emails to {output_file}")

if __name__ == '__main__':
    service = get_gmail_service()
    fetch_and_export_emails(service)
