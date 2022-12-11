# Copyright (c) 2022 Johnathan P. Irvin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json

from fastapi import FastAPI, Request, Response, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from revChatGPT.revChatGPT import Chatbot
from uvicorn import run
from credentials import CredentialManager

app = FastAPI()
creds = CredentialManager()

# Create a Jinja2 environment
templates = Jinja2Templates(directory="templates")

# Store the connected clients in a dictionary, with the username as the key
clients = []

# Stored messages
messages = []

with open("config.json") as f:
    config = json.load(f)
chatbot = Chatbot(config)

for user in config.get("users", []):
    creds.register(user.get("username"), user.get("password"))


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request, response: Response):
    return templates.TemplateResponse("index.html", {"request": request, "response": response})

async def broadcast(message: str):
    for client in clients:
        try:
            await client.send_text(message)
        except Exception:
            clients.remove(client)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    await websocket.send_text("Username?")
    username = await websocket.receive_text()
    await websocket.send_text("Password?")
    password = await websocket.receive_text()

    try:
        creds.login(username, password)
    except ValueError as e:
        await websocket.send_text(str(e))
        await websocket.close()
        return

    clients.append(websocket)
    await websocket.send_text("Welcome to the adventure!")

    # Send the user all the messages that have occurred so far
    for message in messages:
        await websocket.send_text(f"{message}")

    while True:
        message = await websocket.receive_text()
        messages.append(message)
        await broadcast(f"{message}")
        response = chatbot.get_chat_response(message)['message']
        messages.append(response)
        await broadcast(f"{response}")

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
