from fastapi import FastAPI
from inflect import engine
from app.routers import dino_router
from app.services.db_connection import Base

# create db on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# register our routers.add()
app.include_router(dino_router.router)


# Generic sample endpoint
@app.get("/")
async def read_root():
    return {"Hello": "World"}