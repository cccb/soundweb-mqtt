
"""
MQTT service
"""

import time
import queue
import json

import paho.mqtt.client as mqtt


def _make_message_handler(actions):
    """Create message handler"""

    def _on_message(_client, _obj, msg):
        tokens = msg.topic.split("/")

        # Receive and decode, publish in queue
        action_type = tokens[-1]
        try:
            action_payload = json.loads(msg.payload)
        except:
            action_payload = {}
        action = {
            "type": action_type,
            "payload": action_payload,
        }

        actions.put(action)

    return _on_message


def connect(address, base_topic):
    """Open connection, subscribe and create dispatch"""
    try:
        host, port = address.split(":", 1)
    except ValueError:
        host = address
        port = 1883

    actions = queue.Queue()

    client = mqtt.Client()
    client.on_message = _make_message_handler(actions)
    client.connect(host, int(port), 60)
    client.subscribe("{}/#".format(base_topic))

    # Start client in dedicated thread. Do not
    # block our main application.
    client.loop_start()

    # Create dispatch function


    return actions


if __name__ == "__main__":
    actions = connect("localhost", "fnord")


    while True:
        try:
            action = actions.get(block=False)
        except queue.Empty:
            action = None

        if not action:
            print(">> Foo")
        else:
            print(">> Incoming:")
            print(action)

        time.sleep(1)

