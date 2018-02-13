
import argparse
import logging
import copy

from llama import mqtt

from sndweb import connection, message
from mqtt import actions


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
    root.name = "sndmqtt"

    logging.debug("Initialized logging")


#
# Message and Action handling
#
def _handle_message(dispatch, state, msg):
    """Handle incoming messages from soundweb device"""
    logging.debug("Received soundweb message: {}".format(msg))
    state = copy.deepcopy(state)

    if msg["type"] == message.SET_VALUE:
        state = _handle_soundweb_set_value(dispatch,
                                           state,
                                           msg["payload"]["group"],
                                           msg["payload"]["id"],
                                           msg["payload"]["value"])

    elif msg["type"] == message.SET_TEXT:
        state = _handle_soundweb_set_text(dispatch,
                                          state,
                                          msg["payload"]["group"],
                                          msg["payload"]["id"],
                                          msg["payload"]["value"])

    return state


def _handle_soundweb_set_value(dispatch, state, group, control_id, value):
    """Handle incoming changes"""
    if group == message.SW_AMX_LEVEL:
        logging.info("Publishing set level(id={}, value={}) update".format(
            control_id, value))
        dispatch(actions.set_level_success(control_id, value))
        state["levels"][control_id] = value

    elif group == message.SW_AMX_TOGGLE:
        logging.info("Publishing set toggle(id={}, state={}) update".format(
            control_id, value))

        dispatch(actions.set_toggle_success(control_id, value))
        state["toggles"][control_id] = (value == 1)

    elif group == message.SW_AMX_SOURCE:
        logging.info("Publishing set source(id={}, value={}) update".format(
            control_id, value))

        dispatch(actions.set_source_success(control_id, value))
        state["sources"][control_id] = value


    return state


def _handle_soundweb_set_text(dispatch, state, group, control_id, value):
    pass


def _handle_action(dispatch, send, state, action):
    logging.debug("Received action: {}".format(action))
    state = copy.deepcopy(state)

    if action["type"] == actions.SET_LEVEL_REQUEST:
        level_id = action["payload"]["id"]
        value = action["payload"]["value"]

        logging.info("Setting level (id={}) to {}".format(level_id, value))

        # Set value at device
        send(message.set_value(message.SW_AMX_LEVEL, level_id, value))

        # For now assume everything went fine
        dispatch(actions.set_level_success(level_id, value))

        state["levels"][level_id] = value

    elif action["type"] == actions.GET_LEVEL_REQUEST:
        level_id = action["payload"]["id"]
        try:
            value = state["levels"][level_id]
            dispatch(actions.get_level_success(level_id, value))
        except KeyError:
            dispatch(actions.get_level_error(level_id, "404 unknown id"))


    elif action["type"] == actions.GET_LEVELS_REQUEST:
        dispatch(actions.get_levels_success(state["levels"]))


    elif action["type"] == actions.SET_TOGGLE_REQUEST:
        toggle_id = action["payload"]["id"]
        value = action["payload"]["state"]

        logging.info("Setting toggle (id={}) to {}".format(toggle_id, value))

        # Set at device
        send(message.set_value(message.SW_AMX_TOGGLE, toggle_id, value))

        # Inform other devices
        dispatch(actions.set_toggle_success(toggle_id, value))

        # Update state
        state["toggles"][toggle_id] = value


    elif action["type"] == actions.GET_TOGGLE_REQUEST:
        toggle_id = action["payload"]["id"]

        try:
            dispatch(actions.get_toggle_success(toggle_id,
                                                state["toggles"][toggle_id]))
        except KeyError:
            dispatch(actions.get_toggle_error(toggle_id, "404 unknown id"))


    elif action["type"] == actions.GET_TOGGLES_REQUEST:
        dispatch(actions.get_toggles_success(state["toggles"]))


    elif action["type"] == actions.SET_SOURCE_REQUEST:
        source_id = action["payload"].get("id")
        value = action["payload"].get("value")

        logging.info("Setting source (id={}) to {}".format(source_id, value))

        send(message.set_value(message.SW_AMX_SOURCE, source_id, value))
        dispatch(actions.set_source_success(source_id, value))

        state["sources"][source_id] = value


    elif action["type"] == actions.GET_SOURCE_REQUEST:
        source_id = action["payload"].get("id")

        try:
            dispatch(actions.get_source_success(source_id,
                                                state["sources"][source_id]))
        except KeyError:
            dispatch(actions.get_source_error(source_id, "404 unknown id"))


    elif action["type"] == actions.GET_SOURCES_REQUEST:
        dispatch(actions.get_sources_success(state["sources"]))


    elif action["type"] == actions.MESSAGE_DECODE_ERROR_RESULT:
        error_result = action["payload"]
        dispatch(actions.message_decode_error(error_result["topic"],
                                              error_result["payload"],
                                              error_result["error"]))


    return state


def main(args):
    """Soundweb to MQTT bridge"""
    # Show welcome message
    print("Soundweb to MQTT                                  v.0.1.0")
    print()

    # Setup logging
    _setup_logging(args.log_level)

    # Connect to soundweb
    receive, send = connection.connect(args.serial)

    # Connect to MQTT broker
    dispatch, receive_action = mqtt.connect(args.broker, {
        "soundweb": args.topic,
        "meta": "v1/_meta",
    })

    logging.info("Serial and MQTT connected")

    # Make initial states
    state = {
        "levels": {},
        "toggles": {},
        "sources": {},
    }

    # Main loop
    for msg in receive():
        # Check for incoming serial data
        if msg:
            # Handle incoming soundweb message
            state = _handle_message(dispatch, state, msg)

        # Check if there are MQTT actions
        action = receive_action(once=True, timeout=0)
        if action:
            # Handle MQTT action
            state = _handle_action(dispatch, send, state, action)


if __name__ == "__main__":
    args = parse_args()
    main(args)

