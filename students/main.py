from fastapi import FastAPI
from . import schemas, models
from Database.database import engine


models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/student")
def create(student: schemas.Student):
    return {"message": "Create"}
