from fastapi import FastAPI
from api.v1.router import api_router

app = FastAPI(
    title="News + Discord API",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",       # file_name:app_instance
        host="127.0.0.1",
        port=8000,
        reload=True       # auto reload on changes
    )