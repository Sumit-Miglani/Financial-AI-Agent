import os
from google_auth_oauthlib.flow import Flow

# Permit http for local OAuth testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

scopes = ['https://www.googleapis.com/auth/spreadsheets']
flow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=scopes,
    redirect_uri='http://localhost'
)

auth_url, _ = flow.authorization_url(prompt='consent')
print(f"\n1. Open this URL in your browser:\n\n{auth_url}\n")
print("2. Sign in with your Google account.")
print("3. If warned, click 'Advanced' -> 'Go to Finalyst (unsafe)' -> 'Allow'.")
print("4. When redirected to the blank/unreachable page, copy the ENTIRE URL from your browser address bar.")

redirect_response = input("\n5. Paste the full redirected URL here: ").strip()

flow.fetch_token(authorization_response=redirect_response)
creds = flow.credentials

with open('token.json', 'w') as f:
    f.write(creds.to_json())

print("\nSuccessfully generated token.json!")
