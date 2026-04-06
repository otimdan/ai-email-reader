import json
import os
from dotenv import load_dotenv

# 1. Load the environment variables immediately  
load_dotenv()

# 2. DEBUG: Verify the key is actually there
print(f"DEBUG: GOOGLE_API_KEY is {'SET' if os.getenv('GOOGLE_API_KEY') else 'MISSING'}")

import uuid
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import agent
from ai_email_reader.agent import root_agent


app = FastAPI()

# Frontend folders
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# -----------------------------
# ADK SETUP
# -----------------------------

session_service = InMemorySessionService()

APP_NAME = "Otim's Email Reader"
USER_ID = "dan_otim"
SESSION_ID = str(uuid.uuid4())

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


# -----------------------------
# CREATE SESSION ON STARTUP
# -----------------------------

@app.on_event("startup")
async def startup():

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    print("SESSION CREATED:", SESSION_ID)


# -----------------------------
# ROUTES
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):

    data = await request.json()
    user_message = data["message"]

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    final_response = ""

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    try:
        # 1. Parse the string back into a Python Dictionary
        clean_json = json.loads(final_response)
        
        # 2. Return it as a direct JSON object
        return clean_json
    except json.JSONDecodeError:
        # Fallback if the AI returns a regular sentence instead of JSON
        return {"response": final_response}
