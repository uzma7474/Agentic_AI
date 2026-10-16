from crewai import Task
from app_agents.generator import generator_agent

# create a task for generating the contents using context
generator_task = Task(
    description="""
        Answer the user's question using ONLY the retrieved context.

        User Question:
        {question}

        Retrieved Context:
        --------------------
        {context}
        --------------------

        Rules:
        1. Use only information contained in the retrieved context.
        2. Do not use your general knowledge to fill gaps.
        3. Do not invent facts.
        4. If the context does not contain enough information, explicitly state: 
           "I don't have enough information in the knowledge base to answer this question."
        5. Keep the answer clear and concise.
        6. When making factual claims, mention the source document when possible.
        7. Do not claim that information is present in the context if it is not actually present.
    """,

    # set the expectation 
    expected_output="""
        A concise answer to the user's question based strictly on the retrieved context.
    """,

    # use the agent to perform the task
    agent=generator_agent
)
