from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user_db_model import UserDBModel, CreateUserModel
from app.models.user_model import UserModel
from app.services.db_connection import get_db
from app.services.langchain_service import get_basic_chain

# Same old Router Setup
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# All of these functions use DEPENDENCY INJECTION to get access to a DB connection

# Insert User
@router.post("/")
async def create_user(new_user:CreateUserModel, db: Session = Depends(get_db)):

    # Extract the incoming user data into a format that the DB can accept
    # **? this unpacks the data into a dict which we convert to a UserDBModel
    user = UserDBModel(**new_user.model_dump())

    # Add and commit the new user to the DB
    db.add(user)
    db.commit()

    # Refresh the user variable, which overwrites it with what went into the DB
    db.refresh(user)

    return user # Send the new User back to the client (SwaggerUI in this case)


# Get all users
@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserDBModel).all()

# Get one user by ID (path param)
@router.get("/by_id/{user_id}")
async def get_user_by_id(user_id:int, db: Session = Depends(get_db)):
    # Filter the ResultSet to only include the user with the given id.
    # first() returns the first result of the query... there should only be one
    user = db.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    # Some basic error handling for user not found
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found!")

    # If the user is found, return it
    return user

# update user by ID (path param)
@router.put("/by_id/{user_id}")
async def update_user_by_id(user_id:int, updated_user:CreateUserModel, db: Session = Depends(get_db)):
    # Find the user we want to update
    user = db.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    # Error handling for user not found
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found!")

    # Update the user's data with the incoming data
    user.username = updated_user.username
    user.password = updated_user.password

    # Commit the changes to the DB
    db.commit()
    db.refresh(user) # Refresh the user variable to get the updated data from the DB

    return user # Return the updated user to the client

# delete user by ID (path param)
@router.delete("/by_id/{user_id}")
async def delete_user_by_id(user_id:int, db: Session = Depends(get_db)):
    # Find the user we want to delete
    user = db.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    # Error handling for user not found
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found!")

    # Delete the user and commit the change to the DB
    db.delete(user)
    db.commit()

    return {"message":f"User with ID {user_id} has been deleted!"}

# RAG (Retrieval Augmented Generation) with our llm and user data
# Augmenting the Generated response based on some data we're retrieving
@router.post("/rag")
async def user_rag(user_input:str, db: Session = Depends(get_db)):
    # get all users as a string
    users = db.query(UserDBModel).all()
    user_string = "\n".join([f"User ID: {user.id}, Username: {user.username}, password: {user.password}" for user in users])
    # ask the LLM a question based on that user info, and return the response
    # Get the basic chain from the langchain service
    chain = get_basic_chain()

    # Ask the LLM a question based on that user info
    response = chain.invoke(
        {"input": f"""Here is some information about users in our database: {user_string}
            Based on this information, answer the user's query: {user_input} """}
    )
    return {"response": response}

