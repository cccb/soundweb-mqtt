
from datetime import datetime


PING = "@meta/PING"
PONG = "@meta/PONG"

WHOIS = "@meta/WHOIS"
IAMA = "@meta/IAMA"

# TODO: Make this configurable
MANIFEST = {
    "handle": "soundweb@mainhall",
    "name": "sndmqtt",
    "description": "Soundweb Audiomatrix to MQTT bridge",
    "version": "1.2.5",
    "started_at": int(datetime.utcnow().timestamp() * 1000),
}


def pong():
    return {
        "type": PONG,
        "payload": {
            "handle": "soundweb@mainhall",
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
        }
    }


def iama():
    return {
        "type": IAMA,
        "payload": MANIFEST,
    }

