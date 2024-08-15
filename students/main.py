import uvicorn
from fastapi import FastAPI
import schemas, models
from Database.database import engine  # Make sure you have adjusted connection setup in "database.py"

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/student")
def create(student: schemas.Student):
    return {"message": "Create"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
