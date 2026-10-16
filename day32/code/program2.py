import asyncio

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types


# create an agent
agent = Agent(
    name="my_agent",
    model=LiteLlm(
        model="ollama_chat/qwen2.5:7b",
        api_base="http://localhost:11434"
    ),
    instruction="You are a helpful assistance answering the user query."
)

async def main():
    # create a session service
    session_service = InMemorySessionService()

    # create a runner
    runner = Runner(
        agent=agent,
        app_name="my app",
        session_service=session_service
    )

    # create a session
    session = await session_service.create_session(
        app_name="my app",
        user_id="user1"
    )

    while True:
        # get user input
        user_input = input("[user]> ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # preprocess the input
        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        # send the input to the runner to generate the answer
        async for event in runner.run_async(
            user_id="user1",
            session_id=session.id,
            new_message=content
        ):
            # extract the text from the content events
            if event.content and event.content.parts:

                # check if this is the final content
                if event.is_final_response():

                    # print content parts
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)

        print()
        
if __name__ == '__main__':
    asyncio.run(main=main())
