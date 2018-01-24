
"""
Connect to a soundweb device via serial
"""

import sys
import time
import queue
import logging

import serial

from sndweb import message

def connect(path):
    """Open a serial connection"""
    try:
        conn = serial.Serial(path, baudrate=38400, timeout=1/30)
    except serial.serialutil.SerialException as e:
        logging.error(str(e))
        sys.exit(-1)


    # Create tx queue
    tx = queue.Queue()

    # Make send function
    def send(data):
        tx.put(data)

    # Make receive function
    def receive():
        return _receive(conn, tx)

    return receive, send


def _send(conn, buf, retry=3):
    """Send encoded messge"""
    if retry == 0:
        logging.warning("Giving up. Could not send message.")
        return

    ret = conn.write(buf)
    if ret != len(buf):
        logging.debug("Wrote {} to serial, expected {}.".format(ret, len(buf)))
        time.sleep(1)
        send(conn, buf, retry - 1)

    # Wait for ACK or NAK
    recv = conn.read()
    if recv == message.NAK:
        logging.warning("Received NAC from device. "
                        "Trying to resend the message.")
        time.sleep(1)
        send(conn, buf, retry - 1)


def _receive(conn, tx):
    """Receive and decode a message"""
    buf = b''

    while True:
        recv = conn.read() # Read bytewise
        if not recv:
            try:
                msg = tx.get(block=False)
                _send(conn, msg)
            except queue.Empty:
                pass

        # Begin of transmission
        if recv == message.STX:
           buf = b'' # Clear message buffer

        # End of transmission
        elif recv == message.ETX:
            try:
                body = message.decode_body(buf)
                conn.write(message.ACK)

                yield message.decode_message(body)

            except message.MessageError as e:
                time.sleep(0.5) # Ratelimiting
                conn.write(message.NAK)

        # State / Responses
        elif recv == message.ACK:
            yield message.ACK
        elif recv == message.NAK:
            yield message.NAK
        else:
            # Just append the received byte
            buf += recv

        yield None # Nothing happend, keep the main loop alive.

