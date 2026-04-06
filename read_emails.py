from gmail_api import init_gmail_service, get_email_messages, get_email_message_details

client_file = 'client_secret.json'
service = init_gmail_service(client_file)

messages = get_email_messages(service, max_results=5)

print(f"Retrieved {len(messages)} messages: ")
for msg in messages:
    msg_details = get_email_message_details(service, msg['id'])
    print(f"Subject: {msg_details['subject']}")
    print(f"Sender: {msg_details['sender']}")
    print(f"Recepients: {msg_details['recipients']}")
    print(f"Snippet: {msg_details['snippet']}")
    print(f"Has Attachments: {'Yes' if msg_details['has_attachments'] else 'No'}")
    print(f"Date: {msg_details['date']}")
    print(f"Starred: {'Yes' if msg_details['star'] else 'No'}")
    print(f"Labels: {msg_details['label']}")
    print("---"*20)