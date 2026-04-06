from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field
from typing import List
import sys
import os

# Adds the directory above (project root) to the search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import directly from the root files
from gmail_api import init_gmail_service, get_email_message_details, search_emails ,search_email_conversations

#Create Gmail API service
client_file = 'client_secret.json'
service = init_gmail_service(client_file)

# --- Define Output Schema ---
class EmailSummary(BaseModel):
    id: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    sender: str = Field(
        description="The email address of the sender."
    )
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    snippet: str = Field(
        description="A brief preview of the email content."
    )
    date: str = Field(
        description="The date the email was sent."
    )
    unread: bool = Field(
        description="Indicates if the email is unread."
    )
    has_attachment: bool = Field(
        description="Indicates if the email has attachments."
    )

class EmailSearchResponse(BaseModel):
    query_used: str =Field(
        description="The Gmail search query generated based on the user's request."
    )
    total_results: int = Field(
        description="The total number of results found."
    )
    emails: List[EmailSummary] = Field(
        description="A list of summarized emails matching the search criteria."
    )

# 1. Define the tool function
def execute_gmail_search(query: str, max_results: int = 5) -> dict:
    """
    Translates user intent into a Gmail search and returns results.
    Args:
        query (str): A valid Gmail search query (e.g., 'is:unread', 'has:attachment').
        max_results (int): Number of emails to retrieve. Defaults to 5.
    """
    # Your pasted code logic:
    messages = search_emails(service, query, max_results=max_results)
    
    summaries = []
    for msg in messages:
        details = get_email_message_details(service, msg['id'])
        summaries.append({
            "id": msg['id'],
            "sender": details['sender'],
            "subject": details['subject'],
            "snippet": details['snippet'],
            "date": details['date'],
            "unread": 'UNREAD' in details['label'],
            "has_attachment": details['has_attachments']
        })
    
    # Return as a dictionary for ADK to process
    return {
        "query_used": query,
        "total_results": len(summaries),
        "emails": summaries
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Gmail search agent',
    instruction = """
        You are a Gmail assistant. Use 'execute_gmail_search' to find emails.
        Step 1: Convert the user's natural language into a valid Gmail query.
        Step 2: Execute the tool and format the response using the output_schema.

        Available operators:

        from:email → sender
        to:email → recipient
        subject:text → subject keywords
        after:YYYY/MM/DD → emails after date
        before:YYYY/MM/DD → emails before date
        newer_than:Nd → emails newer than N days
        is:unread → unread emails
        has:attachment → emails with attachments
        label:name → specific label

        Rules:
        - Combine operators when needed
        - Return a valid Gmail query
        - Do not explain the query
    """,
    tools=[execute_gmail_search], # ADK wraps this function as a tool
    output_schema=EmailSearchResponse,
)
