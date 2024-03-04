from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAIError
from requests import codes

from sales_chat.helpers.chat import chat
from sales_chat.helpers.constants import RETRIEVE_MESSAGE_FAILURE
from sales_chat.helpers.schemas import UserInput

app = FastAPI()

templates = Jinja2Templates(directory="sales_chat/templates")

MESSAGES = [
    ("bot", "Olá, como posso ajudá-lo?")
]


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "messages": MESSAGES},
    )

@app.post("/chat", status_code=codes.OK)
def sales_chat(user_input: UserInput):
    MESSAGES.append(
        ("usuário", user_input.message)
    )
    
    try:
        result = chat.predict(input=user_input.message)
        MESSAGES.append(("bot", result))
    except OpenAIError:
        MESSAGES.append(("bot", RETRIEVE_MESSAGE_FAILURE))

    return {"success": True}