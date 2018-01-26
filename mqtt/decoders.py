
import logging
import json

from mqtt import actions


class DecodeMessageError(Exception):
    pass

class UnknownActionError(DecodeMessageError):
    pass


#
# Action Decoders
#
def decode_action(topic, payload):
    """Decode an incoming MQTT message into an action"""
    tokens = topic.split("/")

    if len(tokens) < 2:
        raise DecodeMessageError("ActionType missing in topic")

    # Extract type and decode payload
    action_type = tokens[-1]
    action_payload = _decode_action_payload(action_type, payload)

    action = {
        "type": action_type,
        "payload": action_payload,
    }

    return action


def _decode_action_payload(action_type, payload):
    """Decode action payload for specific action types"""
    try:
        payload = json.loads(str(payload, "utf-8"))
    except Exception as e:
        logging.warning("Could not decode JSON payload: {}".format(e))
        payload = {}


    if action_type in [actions.GET_LEVELS_REQUEST,
                       actions.GET_TOGGLES_REQUEST,
                       actions.GET_SOURCES_REQUEST]:
        return None


    if action_type in [actions.GET_LEVEL_REQUEST,
                       actions.GET_TOGGLE_REQUEST,
                       actions.GET_SOURCE_REQUEST]:
        return _decode_get_id_payload(payload)


    if action_type in [actions.SET_LEVEL_REQUEST,
                       actions.SET_SOURCE_REQUEST]:
        return _decode_set_value_payload(payload)


    if action_type in [actions.SET_TOGGLE_REQUEST]:
        return _decode_set_state_payload(payload)


def _decode_get_id_payload(payload):
    """Retrieve id from payload"""
    try:
        payload_id = payload["id"]
    except KeyError:
        raise DecodeMessageError("Missing payload: id")

    return {
        "id": payload_id
    }


def _decode_set_value_payload(payload):
    try:
        payload_id = payload["id"]
    except KeyError:
        raise DecodeMessageError("Missing payload: id")

    try:
        payload_value = payload["value"]
    except KeyError:
        raise DecodeMessageError("Missing payload: value")

    return {
        "id": payload_id,
        "value": payload_value
    }


def _decode_set_state_payload(payload):
    try:
        payload_id = payload["id"]
    except KeyError:
        raise DecodeMessageError("Missing payload: id")

    try:
        payload_value = payload["state"]
    except KeyError:
        raise DecodeMessageError("Missing payload: value")


    payload_state = 1 if payload_value == True else 0

    return {
        "id": payload_id,
        "state": payload_state,
    }

