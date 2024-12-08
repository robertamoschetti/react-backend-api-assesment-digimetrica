from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/report")
async def get_report():
    print("sono nel get")
    with open("summary2.0.json", "r") as file:
        data = json.load(file)

    return data