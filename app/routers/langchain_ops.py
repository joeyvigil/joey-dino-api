from fastapi import APIRouter
from pydantic import BaseModel

from app.services.langchain_service import get_basic_chain, get_sequential_chain

# same setup

router = APIRouter(
    prefix="/langchain",
    tags=["langchain"]
)

# making a quick pydantic model that will represent the user's input
class ChatInputModel(BaseModel):
    input: str
    
basic_chain = get_basic_chain()
refined_answer_chain = get_sequential_chain()


@router.post("/chat")
async def chat_with_langchain(chat:ChatInputModel):
    return {"response": basic_chain.invoke(chat.input)}

@router.post("/refined_chat")
async def refined_chat_with_langchain(chat:ChatInputModel):
    return {"response": refined_answer_chain.invoke(chat.input)}