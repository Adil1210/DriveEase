from fastapi import FastAPI

from app.api.endpoints import example, auth


app = FastAPI()

app.include_router(example.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
