from fastapi import FastAPI
from basic_data import basic_data
from retrive import retrive


app = FastAPI()

app.include_router(retrive.router)
app.include_router(basic_data.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

