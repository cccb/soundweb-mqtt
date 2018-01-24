
from sndweb import connection, message
from mqtt import service, actions


def _handle_message(dispatch, message):
    pass

def _handle_action(dispatch, send, action):
    if action["type"] == actions.SET_LEVEL_REQUEST:
        level_id = action["payload"].get("level_id")
        value = action["payload"].get("value")

        send(message.set_value(message.SW_AMX_LEVEL, level_id, value))

        # Todo error handling


def main(args):
    """Soundweb to MQTT bridge"""
    # Connect to soundweb
    receive, send = connection.connect("/dev/tty.usbserial")

    # Connect to MQTT broker
    receive_action, dispatch = service.connect("localhost", "fnord")

    print("Soundweb to MQTT ready")


    for msg in receive():
        # Check for incoming serial data
        if msg:
            print("Received soundweb:")
            print(msg)

            # Handle message
            _handle_message(dispatch, msg)

        # Check if there are MQTT actions
        action = receive_action()
        if action:
            print("Received action:")
            print(action)

            # Handle action
            _handle_action(dispatch, send, action)


if __name__ == "__main__":
    main({})


