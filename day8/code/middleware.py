from langchain.agents.middleware import AgentMiddleware
import logging
from config import MESSAGE_COUNT, MESSAGE_DURATION
from collections import deque
import time

# get the logger
logger = logging.getLogger(__name__)

class RateLimitMiddleware(AgentMiddleware):

    def __init__(self):
        super().__init__()

        # middleware wont allow user to send more than this count
        self.max_requests = MESSAGE_COUNT

        # middleware wont allow user to send more than this count within this duration
        self.duration = MESSAGE_DURATION

        # collect all the timestamps
        self.timestamps: deque[float] = deque()

    def before_agent(self, state, runtime):
        """before hitting the message to the model, check the no of requests"""

        # get the current timestamp
        now = time.time()

        # remove the older timestamp which are already occurred
        while self.timestamps and self.timestamps[0] < now - self.duration:
            # popleft will remove the items from beginning
            self.timestamps.popleft()

        # check the number of requests
        if len(self.timestamps) >= self.max_requests:
            logger.warning(f"max limit of messages hit")

            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": f"rate limit of {self.max_requests} is hit. Do not answer any question."
                    }
                ],
                "jump_to": "end"
            }

        # add the current timestamp
        self.timestamps.append(now)

        logger.info(f"no of requests = {len(self.timestamps)}")

        return None
