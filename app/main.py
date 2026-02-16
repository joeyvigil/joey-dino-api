from fastapi import FastAPI
from app.routers import dino_router

app = FastAPI()

# register our routers.add()
app.include_router(dino_router.router)


# Generic sample endpoint
@app.get("/")
async def read_root():
    return {"Hello": "World"}