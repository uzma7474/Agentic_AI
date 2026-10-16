import json
import queue
import threading
import time
import uuid
from collections import deque
from datetime import datetime

import pika
import streamlit as st

import config

st.set_page_config(page_title="Smart Home Demo", layout="wide")

@st.cache_resource
def get_event_queue():
    return queue.Queue()

@st.cache_resource
def start_consumer(_event_queue):
    """Starts the RabbitMQ consumer thread once per process."""
    queue_name = f'q.ui_dashboard_{uuid.uuid4().hex[:8]}'
    print(f"[UI] Starting consumer on {queue_name}")

    def consume():
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(config.RABBITMQ_HOST)
            )
            channel = connection.channel()
            channel.queue_declare(
                queue=queue_name,
                durable=False,
                exclusive=True,
                auto_delete=True,
            )
            channel.queue_bind(
                exchange=config.MAIN_EXCHANGE,
                queue=queue_name,
                routing_key='#',
            )

            def callback(ch, method, properties, body):
                try:
                    _event_queue.put(json.loads(body))
                except Exception:
                    pass
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=False,
            )
            print(f"[UI] Consuming on {queue_name}")
            channel.start_consuming()
        except Exception as e:
            print(f"[UI] Consumer crashed: {e}")

    thread = threading.Thread(target=consume, daemon=True)
    thread.start()
    return thread


# Call once. Streamlit caches the results across reruns.
event_queue = get_event_queue()
_consumer_thread = start_consumer(event_queue)

if 'readings' not in st.session_state:
    st.session_state.readings = deque(maxlen=30)
if 'decisions' not in st.session_state:
    st.session_state.decisions = deque(maxlen=30)
if 'events' not in st.session_state:
    st.session_state.events = deque(maxlen=50)


drained = 0
while not event_queue.empty():
    try:
        event = event_queue.get_nowait()
    except queue.Empty:
        break
    drained += 1
    etype = event.get('event_type', '')
    payload = event.get('payload', {})
    now = datetime.now().strftime('%H:%M:%S')

    if etype == config.RK_SENSOR_READING:
        temp = payload.get('temperature')
        st.session_state.readings.append({'time': now, 'temp': temp})
        st.session_state.events.append(
            {'time': now, 'type': 'reading', 'detail': f"{temp}°C"}
        )
    elif etype == config.RK_DECISION_PROPOSED:
        value = payload.get('value')
        reason = payload.get('reason', '')
        st.session_state.decisions.append(
            {'time': now, 'value': value, 'reason': reason}
        )
        st.session_state.events.append(
            {'time': now, 'type': 'decision', 'detail': f"→ {value}°C — {reason}"}
        )

st.title("IoT Smart Home Orchestrator")
st.caption(f"Drained {drained} events this cycle")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Temperature readings")
    temps = [r['temp'] for r in st.session_state.readings if r['temp'] is not None]
    if temps:
        st.line_chart(temps)
        st.caption(f"Latest: {temps[-1]}°C — {len(temps)} readings")
    else:
        st.info("Waiting for sensor readings...")

with col2:
    st.subheader("Latest decision")
    if st.session_state.decisions:
        d = st.session_state.decisions[-1]
        st.metric("Target temp", f"{d['value']}°C")
        st.caption(f"Reason: {d['reason']}")
    else:
        st.info("No decisions yet.")

st.subheader("Recent events")
if st.session_state.events:
    for row in list(st.session_state.events)[-15:]:
        if row['type'] == 'decision':
            st.success(f"{row['time']}  {row['detail']}")
        else:
            st.text(f"{row['time']}  {row['detail']}")
else:
    st.info("No events yet.")

time.sleep(2)
st.rerun()