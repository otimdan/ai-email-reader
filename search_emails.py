from gmail_api import init_gmail_service, get_email_message_details, search_emails ,search_email_conversations

#Create Gmail API service
client_file = 'client_secret.json'
service = init_gmail_service(client_file)

#Search for emails with specific query
query = 'is:important'
email_messages = search_emails(service, query, max_results=3)

for message in email_messages:
    email_detail = get_email_message_details(service, message['id'])
    print(message['id'])
    print(f"Subject: {email_detail['subject']}")
    print(f"Date: {email_detail['date']}")
    print(f"Labels: {email_detail['label']}")
    print(f"Snippet: {email_detail['snippet']}")
    print(f"Body: {email_detail['body']}")
    print("--"*20)