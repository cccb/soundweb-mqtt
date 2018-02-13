
from meta import actions

def handle(dispatch, action):

    if action["type"] == actions.PING:
        dispatch(_handle_ping(action["payload"]))

    elif action["type"] == actions.WHOIS:
        dispatch(_handle_whois(action["payload"]))


def _handle_ping(payload):
    if payload != actions.MANIFEST["handle"] and payload != "*":
        return None

    return actions.pong()

def _handle_whois(payload):
    if payload != actions.MANIFEST["handle"] and payload != "*":
        return None

    return actions.iama()

