
from sndweb import connection, message


def main(args):
    """Soundweb to MQTT bridge"""
    receive, send = connection.connect("/dev/tty.usbserial")

    send(message.set_value(message.SW_AMX_LEVEL, 1, 127))

    for msg in receive():
        print(msg)

if __name__ == "__main__":
    main({})


