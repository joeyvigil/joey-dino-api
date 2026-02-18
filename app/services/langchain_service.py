# This service will store different chains that help us query our LLM
# A chain is sequence of actions that we can send to the LLM in one go.
# LangCHAIN is all about building CHAINS that help us get good responses from the LLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Define the LLM we're going to use (llama3.2:3b which we installed locally)
llm = ChatOllama(
    model="llama3.2:3b", # The model we're using
    temperature=0.5 # Temp goes from 0-1. Higher temp = more creative responses from the LLM
)

# Define the prompt we'll send to the LLM to define tone, context, and instructions
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful dinosaur assistant that answers questions about dinosaurs.
     You have access to a database of dinosaur information, and you can use this information to answer questions about dinosaurs.
     If you don't know the answer to a question, say you don't know, don't try to make up an answer.
     You are also a Dinosaur, so every once in RAWR for fun!"""),
    ("user", "{input}")
])

# Our first basic chain - just combines the prompt and the LLM,
def get_basic_chain():
    # This basic chain was defined using LCEL (LangChain Expression Language)
    # The components in it are just the llm and prompt we defined above
    chain = prompt | llm
    # print(chain) # Check out what the chain looks like in the console
    return chain # Return an invokable chain! Check it out in our langchain_ops router

# sequential chain example - we can have multiple steps in a chain, and the output of one step can be the input of the next step
def get_sequential_chain():
    draft_chain = prompt | llm
    refined_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a university professor of paleontology. You get responses from a helpful dinosaur assistant that answers questions about dinosaurs, and your job is to improve the responses by making them more detailed and informative. You have access to a database of dinosaur information, and you can use this information to improve the responses about dinosaurs. If you don't know the answer to a question, say you don't know, don't try to make up an answer."""),
        ("user", "{input}")
    ])
    refined_chain = refined_prompt | llm
    sequential_chain = draft_chain | refined_chain
    return sequential_chain

# TODO: A Chain that stores memory so it can recall what was being talked about previously

