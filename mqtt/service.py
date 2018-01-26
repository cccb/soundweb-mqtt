
"""
MQTT service
"""

import time
import queue
import json
import logging
import functools

import paho.mqtt.client as paho_mqtt

import mqtt.decoders as decoders
import mqtt.actions as mqtt_actions


def _on_message(actions, _client, _obj, msg):
    """Handle incoming messages from MQTT"""
    try:
        action = decoders.decode_action(msg.topic, msg.payload)
    except decoders.DecodeMessageError as e:
        logging.warning("Could not decode incoming message: {}".format(e))
        action = mqtt_actions.message_decode_error_result(msg.topic, msg.payload, e)

    actions.put(action)


def _dispatch(client, base_topic, action):
    """General action dispatch function"""
    try:
        payload = json.dumps(action.get("payload")).encode("utf-8")
    except Exception as e:
        logging.error("Could not encode payload: {}".format(e))
        return

    topic = base_topic + "/" + action["type"]

    ticket = client.publish(topic, payload)
    ticket.wait_for_publish()


def _receive(actions):
    """General receive function"""
    try:
        return actions.get(block=False)
    except queue.Empty:
        return None


def connect(address, base_topic):
    """Open connection, subscribe and create dispatch"""
    try:
        host, port = address.split(":", 1)
    except ValueError:
        host = address
        port = 1883

    actions_queue = queue.Queue()

    client = paho_mqtt.Client()
    client.on_message = functools.partial(_on_message, actions_queue)
    client.connect(host, int(port), 60)
    client.subscribe("{}/#".format(base_topic))

    logging.info("Receiving actions on topic {}/#".format(base_topic))

    # Start client in dedicated thread. Do not
    # block our main application.
    client.loop_start()

    # Make receive function
    receive = functools.partial(_receive, actions_queue)

    # Create dispatch function
    dispatch = functools.partial(_dispatch, client, base_topic)

    return receive, dispatch

