
"""
Connect to a soundweb device via serial
"""

import serial

import message

def connect(path):
    """Open a serial connection"""
    conn = serial.Serial(path, baudrate=38400)

    return conn


def send(conn, buf):
    """Send encoded messge"""
    return conn.write(buf)


def receive(conn):
    """Receive and decode a message"""
    buf = b''

    while True:
        recv = conn.read() # Read bytewise
        # Begin of transmission
        if recv == message.STX:
            buf = b'' # Clear message buffer

        # End of transmission
        elif recv == message.ETX
            try:
                body = message.decode_message_body(buf)
                send(conn, message.ACK)

                return body
            except message.ChecksumError:
                send(conn, message.NAK)

        # State / Responses
        elif recv == message.ACK:
            return message.ACK
        elif recv == message.NAK:
            return message.NAK
        else:
            # Just append the received byte
            buf += recv

