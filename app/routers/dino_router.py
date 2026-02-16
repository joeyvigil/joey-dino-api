# Routers are how we expose http endpoints in FastAPI. This file will contain all of the endpoints related to dinosaurs. 
# take in http requests, process them, and return responses. We will use the APIRouter class from FastAPI to create a router for our dinosaur endpoints.
from os import path
from fastapi import APIRouter, HTTPException
from app.models.dino_model import DinoModel


router = APIRouter(
    prefix="/dinos", # http request ending in /dinos will be handled by this router
    tags=["dinos"] # this is used for documentation purposes. It helps group related endpoints together in the API docs.
)

# Dinky python map database ( check out the user_router for and endpoint that hits a real database )
dino_database = {
    1: DinoModel(id=1, species="Tyrannosaurus Rex", period="Late Cretaceous"),
    2: DinoModel(id=2, species="Triceratops", period="Late Cretaceous"),
    3: DinoModel(id=3, species="Velociraptor", period="Late Cretaceous"),
}



# CRUD Endpoints

# GET all dinos
@router.get("/")
async def get_all_dinos():
    return list(dino_database.values())

# GET a single dino by id
@router.get("/get1/{dino_id}")
async def get_dino_by_id(dino_id: int):
    if dino_id in dino_database:
        return dino_database[dino_id]
    else:
        raise HTTPException(status_code=404, detail="Dino not found")

# POST a new dino
@router.post("/", status_code=201)
async def create_dino(dino: DinoModel):
    new_id = max(dino_database.keys()) + 1
    dino_database[new_id] = DinoModel(id=new_id, species=dino.species, period=dino.period)
    return dino_database[new_id]

# GET a certain number of dinos using query parameter. For example, /dinos?limit=2 will return the first 2 dinos in the database.
@router.get("/some_dinos")
async def get_some_dinos(limit: int=2):
    return list(dino_database.values())[:limit]

# PUT (update) a dino by id

# DELETE a dino by id