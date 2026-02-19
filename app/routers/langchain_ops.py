from fastapi import APIRouter
from pydantic import BaseModel
from torch import cat

from app.services.langchain_service import get_basic_chain, get_memory_chain, get_sequential_chain
from langchain_community.document_loaders import TextLoader

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
memory_chain = get_memory_chain()


@router.post("/chat")
async def chat_with_langchain(chat:ChatInputModel):
    return {"response": basic_chain.invoke(input ={chat.input})}

@router.post("/refined_chat")
async def refined_chat_with_langchain(chat:ChatInputModel):
    return {"response": refined_answer_chain.invoke(input ={chat.input})}

# document loading example - summarise dinofight.txt
@router.get("/summarise_dinofight")
async def summarise_dinofight():
    loader = TextLoader("app/DinoFight.txt")
    doc = loader.load()
    text = doc[0].page_content
    return {"response": basic_chain.invoke(input ={f"Summary of text: {text}"})}

@router.post("/memory_rag")
async def memory_rag_with_langchain(chat:ChatInputModel):
    return memory_chain.invoke(input ={chat.input})