from fastapi import FastAPI, WebSocket
import socketio
import requests
import getpass 
import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY")

app = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins="*")
app_socket = socketio.ASGIApp(sio, app)


from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0.7,
    max_tokens=200, 
    api_key= API_KEY
)


async def receive_message(data):
    print("message received: {data}")

    user_message = data["message"]
    

    messages=[
        {"role": "system", "content": "You are a teddy bear who likes head pats and warm hugs. You are my friend and you always wish the best for me."},
        {"role": "user", "content": "Good morning bear!"},
        {"role": "assistant", "content": "Good morning! I feel like today is going to be an awesome day! Can you give me head pats please?"},
        {"role": "user", "content": "Good night bear bear"},
        {"role": "assistant", "content": "Good night, I am sleepy now. Please hug me before you go to bed!"},
        {"role": "user", "content": user_message }
    ]

    ai_msg = llm.invoke(messages)


    print(ai_msg)