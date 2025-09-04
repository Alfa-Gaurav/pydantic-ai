from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import json
from typing import AsyncGenerator
load_dotenv()
from service import get_cities as get_cities_service
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/cities")
async def get_cities():
    async def sse_stream() -> AsyncGenerator[str, None]:
        async for payload in get_cities_service():
            yield f"data: {json.dumps(payload)}\n\n"

    return StreamingResponse(sse_stream(), media_type="text/event-stream")