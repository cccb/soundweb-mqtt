
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
            action_payload = json.loads(str(msg.payload, 'utf-8'))
        except:
            action_payload = None

        action = {
            "type": action_type,
            "payload": action_payload,
        }

        actions.put(action)

    return _on_message


def _make_action_generator(actions):
    """Convenient generator for handling actions"""
    while True:
        try:
            action = actions.get(timeout=1)
        except queue.Empty:
            action = None

        if not action:
            print(">> Foo")
        else:
            yield action


def _make_dispatch(client, base_topic):
    """Create dispatch function"""
    def dispatch(action):
        payload = json.dumps(action.get("payload")).encode("utf-8")
        topic = base_topic + "/" + action["type"]

        ticket = client.publish(topic, payload)
        ticket.wait_for_publish()


    return dispatch


def connect(address, base_topic):
    """Open connection, subscribe and create dispatch"""
    try:
        host, port = address.split(":", 1)
    except ValueError:
        host = address
        port = 1883

    actions_queue = queue.Queue()

    client = mqtt.Client()
    client.on_message = _make_message_handler(actions_queue)
    client.connect(host, int(port), 60)
    client.subscribe("{}/#".format(base_topic))

    # Start client in dedicated thread. Do not
    # block our main application.
    client.loop_start()

    # Create actions generator
    actions = _make_action_generator(actions_queue)

    # Create dispatch function
    dispatch = _make_dispatch(client, base_topic)

    return actions, dispatch


if __name__ == "__main__":
    actions, dispatch = connect("localhost", "fnord")
    dispatch({"type": "FOO"})

    for action in actions:
        print("Incoming:")
        print(action)

