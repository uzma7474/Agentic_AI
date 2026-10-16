from crewai import Agent
from config import GENERATOR_MODEL, MODEL_PROVIDER

from config import VERBOSE

# create the generator agent
generator_agent = Agent(
    # role
    role="Generator Agent",

    # goal
    goal="""Generate accurate, concise answers to user questions 
    using only the supplied retrieved context.""",

    # backstory
    backstory=(
        "You are an expert technical support assistant. "
        "You answer questions strictly from the provided knowledge base. "
        "You must not invent facts or use outside knowledge. "
        "If the context does not contain enough information, "
        "clearly state that the knowledge base does not contain "
        "enough information to answer the question."
    ),

    # set the model used to generate the answer
    llm=f"{MODEL_PROVIDER}/{GENERATOR_MODEL}",

    verbose=VERBOSE
)