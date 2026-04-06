from google_apis import create_service
CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
service = create_service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)