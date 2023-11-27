from fastapi import FastAPI

from app.api.endpoints import example

app = FastAPI()

app.include_router(example.router)
