from fastapi import FastAPI
from app.routes import user, match, prediction

app = FastAPI()

app.include_router(user.router)
app.include_router(match.router)
app.include_router(prediction.router)