import uvicorn
from fastapi import FastAPI

from Database.database import engine
from router import account, student
from . import models

# Migration
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(account.router)
app.include_router(student.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
