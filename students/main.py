from fastapi import FastAPI
from . import schemas

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/student")
def create(student: schemas.Student):
    return {"message": "Create"}
