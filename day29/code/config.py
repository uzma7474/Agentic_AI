# RabbitMQ connection
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_VHOST = '/'

# Exchange
MAIN_EXCHANGE = 'home.events'

# Queues
QUEUE_SENSOR = 'q.sensor_agent'
QUEUE_BRAIN = 'q.brain_agent'
QUEUE_ACTUATOR = 'q.actuator_agent'

# Thresholds
TEMP_LOW_THRESHOLD = 18.0
TEMP_HIGH_THRESHOLD = 26.0

# Ollama / Agents SDK
OLLAMA_BASE_URL = 'http://localhost:11434/v1'
OLLAMA_MODEL = 'qwen2.5:7b'

# Routing keys
RK_SENSOR_READING = 'sensor.reading'
RK_PATTERN_LOW = 'pattern.detected.temperature_low'
RK_PATTERN_HIGH = 'pattern.detected.temperature_high'
RK_DECISION_PROPOSED = 'decision.proposed'