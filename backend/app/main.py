from fastapi import FastAPI
from app.database import engine, Base
from app import auth, messages
from app.websocket import websocket_endpoint, send_message


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth.router)
app.include_router(messages.router)

app.add_api_websocket_route("/ws/{username}", websocket_endpoint)

app.post("/send-message/")(send_message)


@app.on_event("startup")
async def startup_event():
    print("Starting application...")