from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import json
from typing import AsyncGenerator
load_dotenv()
from service import get_cities as get_cities_service


app = FastAPI()

# Allow front-end dev server origins (Vite default ports)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/cities")
async def get_cities():
    async def sse_stream() -> AsyncGenerator[str, None]:
        async for payload in get_cities_service():
            yield f"data: {json.dumps(payload)}\n\n"

    return StreamingResponse(sse_stream(), media_type="text/event-stream")