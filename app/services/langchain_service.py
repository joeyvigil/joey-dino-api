# This service will store different chains that help us query our LLM
# A chain is sequence of actions that we can send to the LLM in one go.
# LangCHAIN is all about building CHAINS that help us get good responses from the LLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory

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
        ("system", """You are a university professor of paleontology. You get responses from a helpful dinosaur assistant that answers questions about dinosaurs, and your job is to improve the responses by making them more detailed and informative."""),
        ("user", "{input}")
    ])
    refined_chain = refined_prompt | llm
    sequential_chain = draft_chain | refined_chain
    return sequential_chain

def get_memory_chain():

    # Create a memory object, an instance of ConversationBufferWindowMemory
    # This Memory instance remembers the last "k" interactions
    memory = ConversationBufferWindowMemory(k=3)

    # Make a Prompt and Chain the old fashioned way...

    # Prompt - We're using an older Memory object, so notice:
        # {input} to store the user input like we've been doing
        # {history} which stores the conversation history
    # Unfortunately, we will have to rewrite the prompt
    memory_prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are a helpful dinosaur assistant that answers questions about dinosaurs.
        You have access to a database of dinosaur information, and you can use this information to answer questions about dinosaurs.
        If you don't know the answer to a question, say you don't know, don't try to make up an answer.
        You are also a Dinosaur, so every once in RAWR for fun!"""),
        ("user", "Current input: {input},"
                 "Conversation history: {history}")
    ])

    # Chain - we have to use an older clunkier syntax to use memory here
    # (Remember the Chain and Memory stuff in week 2 is kind of outdated...)
    memory_chain = ConversationChain(
        llm = llm,
        memory = memory,
        prompt = memory_prompt
    )

    # Return the chain with memory, invoked in the router endpoint
    return memory_chain
    



