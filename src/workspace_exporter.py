import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def export_audit_to_sheets(spreadsheet_id: str, row_data: list, token_path: str = "token.json"):
    if not os.path.exists(token_path):
        print(" [Workspace API] Notice: token.json not found. Local audit logged (Sheets export skipped).")
        return False

    try:
        creds = Credentials.from_authorized_user_file(token_path)
        service = build('sheets', 'v4', credentials=creds)

        body = {'values': [row_data]}
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="AuditLogs!A1",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(" [Workspace API] Successfully appended audit log entry to Google Sheets!")
        return True
    except Exception as e:
        print(f" [Workspace API] Export notice: {e}")
        return False
