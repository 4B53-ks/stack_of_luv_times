from fastapi import FastAPI
from api.v1.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="News + Discord API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:5173", "http://localhost:5173", "http://127.0.0.1:5173", "http://solt.soorry.in", "https://backend.solt.soorry.in"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",       # file_name:app_instance
        host="0.0.0.0",
        port=8000,
        reload=True       # auto reload on changes
    )