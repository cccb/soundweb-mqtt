
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
    logging.debug("Incoming MQTT message: {}".format(msg))
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


def _log(_client, userdata, level, buf):
    logging.debug("MQTT: {}".format(buf))


def _on_connect(base_topic, client, userdata, flags, rc):
    # Subscribe to queue
    client.subscribe("{}/#".format(base_topic))
    logging.info("Receiving actions on topic {}/#".format(base_topic))


def _on_disconnect(client, userdata, rc):
    logging.warning("MQTT client disconnected.")


def connect(address, base_topic):
    """Open connection, subscribe and create dispatch"""
    try:
        host, port = address.split(":", 1)
    except ValueError:
        host = address
        port = 1883

    logging.info("Connecting to mqtt://{}:{}".format(host, port))

    actions_queue = queue.Queue()

    client = paho_mqtt.Client()

    # Configure Client
    client.reconnect_delay_set(min_delay=1, max_delay=15)

    # Client Callbacks
    client.on_log = _log
    client.on_message = functools.partial(_on_message, actions_queue)
    client.on_connect = functools.partial(_on_connect, base_topic)
    client.on_disconnect = _on_disconnect

    # Open connection
    client.connect(host, int(port), 60)
    logging.info("Connected.")

    # Start client in dedicated thread. Do not
    # block our main application.
    client.loop_start()

    # Make receive function
    receive = functools.partial(_receive, actions_queue)

    # Create dispatch function
    dispatch = functools.partial(_dispatch, client, base_topic)

    return receive, dispatch

