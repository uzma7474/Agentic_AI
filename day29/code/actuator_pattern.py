from base_agent import BaseAgent
import config


class ActuatorPattern(BaseAgent):
    def __init__(self):
        super().__init__(
            name='actuator-agent',
            queue_name=config.QUEUE_ACTUATOR,
            routing_keys=[config.RK_DECISION_PROPOSED],
        )

    def handle_event(self, event):
        decision = event['payload']
        self.logger.info(
            f"ACTION: {decision['action']} = {decision['value']} "
            f"({decision.get('reason', '')})"
        )

if __name__ == '__main__':
    ActuatorPattern().run()