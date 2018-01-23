
"""
MQTT service
"""

import paho.mqtt.client as mqtt


def _on_message(client, obj, msg):
    print("RECV obj and msg:")
    print(obj)
    print(msg)


def connect(address, base_topic):
    """Open connection, subscribe and create dispatch"""
    try:
        host, port = address.split(":", 1)
    except ValueError:
        host = address
        port = 1883

    client = mqtt.Client()
    client.on_message = _on_message
    client.connect(host, int(port), 60)
    client.subscribe("{}/#".format(base_topic))

    client.loop_start()

    return client


if __name__ == "__main__":
    
    conn = connect("localhost", "fnord")

