
import argparse
import logging

from sndweb import connection, message
from mqtt import service, actions



def parse_args():
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--broker",
                        required=True,
                        help="The MQTT broker host and port")
    parser.add_argument("-t", "--topic",
                        default="soundweb")
    parser.add_argument("-s", "--serial",
                        required=True,
                        help="The serialdevice the soundweb is connected to")
    parser.add_argument("-l", "--log-level",
                        default="info",
                        help="Set log level")

    return parser.parse_args()


def _setup_logging(level):
    """Setup logger based on cli args"""
    fmt = '%(asctime)s [%(name)s::%(levelname)s] %(message)s'
    logging.basicConfig(format=fmt)

    try:
        log_level = getattr(logging, level.upper())
    except:
        logging.warning("Unknown log level ({}), falling back to INFO".format(
            level))
        log_level = logging.INFO

    root = logging.getLogger()
    root.setLevel(log_level)

    logging.debug("initialized logging")


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
    # Setup logging
    _setup_logging(args.log_level)

    return

    # Connect to soundweb
    receive, send = connection.connect("/dev/tty.usbserial")

    # Connect to MQTT broker
    receive_action, dispatch = service.connect("localhost", "fnord")

    # Show welcome message
    print("Soundweb to MQTT                  v.0.1.0")


    # Main loop
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
    args = parse_args()
    main(args)

