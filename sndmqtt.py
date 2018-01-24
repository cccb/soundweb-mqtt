
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

    logging.debug("Initialized logging")


#
# Message and Action handling
#
def _handle_message(dispatch, msg):
    """Handle incoming messages from soundweb device"""
    logging.debug("Received soundweb message: {}".format(msg))

    if msg["type"] == message.SET_VALUE:
        _handle_soundweb_set_value(dispatch,
                                   msg["payload"]["group"],
                                   msg["payload"]["id"],
                                   msg["payload"]["value"])
    if msg["type"] == message.SET_TEXT:
        _handle_soundweb_set_text(dispatch,
                                  msg["payload"]["group"],
                                  msg["payload"]["id"],
                                  msg["payload"]["value"])


def _handle_soundweb_set_value(dispatch, group, control_id, value):
    """Handle incoming changes"""
    if group == messages.SW_AMX_LEVEL:
        logging.info("Publishing set level(id={}, value={}) update".format(
            control_id, value))
        dispatch(actions.set_level_success(control_id, value))


def _handle_soundweb_set_text(dispatch, group, control_id, value):
    pass


def _handle_action(dispatch, send, action):
    logging.debug("Received action: {}".format(action))

    if action["type"] == actions.SET_LEVEL_REQUEST:
        level_id = action["payload"].get("level_id")
        value = action["payload"].get("value")

        logging.info("Setting level (id={}) to {}".format(level_id, value))

        # Set value at device
        send(message.set_value(message.SW_AMX_LEVEL, level_id, value))

        # For now assume everything went fine
        dispatch(actions.set_level_success(level_id, value))


def main(args):
    """Soundweb to MQTT bridge"""
    # Show welcome message
    print("Soundweb to MQTT                                  v.0.1.0")

    # Setup logging
    _setup_logging(args.log_level)

    # Connect to soundweb
    receive, send = connection.connect(args.serial)

    # Connect to MQTT broker
    receive_action, dispatch = service.connect(args.broker,
                                               args.topic)

    logging.info("Serial and MQTT connected")

    # Main loop
    for msg in receive():
        # Check for incoming serial data
        if msg:
            # Handle message
            _handle_message(dispatch, msg)

        # Check if there are MQTT actions
        action = receive_action()
        if action:
            # Handle action
            _handle_action(dispatch, send, action)


if __name__ == "__main__":
    args = parse_args()
    main(args)

