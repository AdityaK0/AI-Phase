from fastapi import FastAPI
from ai_.api import ai_router


app = FastAPI()

@app.get("/")
def root():
    return {"message":"learning AI integration with FastAPI"}



app.include_router(ai_router)