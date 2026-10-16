from agents import Agent, Runner, set_default_openai_client
from openai import AsyncOpenAI
import config
from base_agent import BaseAgent
import asyncio
import json

# create the client
client = AsyncOpenAI(
    base_url=config.OLLAMA_BASE_URL,
    api_key="ollama"
)

# set the default client
set_default_openai_client(client)

# The agent definition
brain = Agent(
    name="BrainAgent",
    instructions="""
        You are a smart home AI.
        You receive a temperature reading. 
        Decide a thermostat action.
        Respond ONLY with valid JSON:
        {"action": "set_thermostat", "value": 21.5, "reason": "brief explanation"}

        Rules:
        - If temperature is below 18, set value higher.
        - If temperature is above 26, set value lower.
        - Keep value between 16 and 28.
    """,
    model=config.OLLAMA_MODEL,
)

class BrainAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name='brain-agent',
            queue_name=config.QUEUE_BRAIN,
            routing_keys=[config.RK_SENSOR_READING],
        )

    # process the received message
    def handle_event(self, event):
        temp = event['payload']['temperature']
        self.logger.info(f"Got temperature: {temp}°C")

        decision = asyncio.run(self._decide(temp))
        self.logger.info(f"Decision: {decision}")

        self.publish(
            routing_key=config.RK_DECISION_PROPOSED,
            payload=decision,
        )

    async def _decide(self, temp):
        prompt = f"Temperature is {temp}°C. Decide a thermostat action."
        result = await Runner.run(starting_agent=brain, input=prompt)

        try:
            return json.loads(result.final_output)
        except json.JSONDecodeError:
            self.logger.warning("Bad JSON from LLM. Using default.")
            return {"action": "set_thermostat", "value": 22.0, "reason": "default"}

if __name__ == '__main__':
    BrainAgent().run()