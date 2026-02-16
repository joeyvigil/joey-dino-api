from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user_db_model import UserDBModel
from app.models.user_model import UserModel
from app.services.db_connection import get_db


router = APIRouter(
    prefix="/users", # http request ending in /users will be handled by this router
    tags=["users"] # this is used for documentation purposes. It helps group related endpoints together in the API docs.
)

# New User
@router.post("/", status_code=201)
async def create_user(user: UserModel, db: Session = Depends(get_db)):
    db_user = UserDBModel(
        username=user.username,
        email=user.email,
        password=user.password.get_secret_value()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user