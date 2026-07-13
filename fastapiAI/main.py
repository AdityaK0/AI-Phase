from fastapi import FastAPI,Request
from ai_.api import ai_router
from users.api import user_router
from exceptions import AppException
from fastapi.responses import JSONResponse

app = FastAPI(prefix="/api", title="AI Integration with FastAPI", description="This is a FastAPI application that integrates AI functionality.", version="1.0.0")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "_error": exc.message
        }
    )

@app.get("/")
def root():
    return {"message":"learning AI integration with FastAPI"}



app.include_router(ai_router)
app.include_router(user_router)
