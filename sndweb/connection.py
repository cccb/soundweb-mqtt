
"""
Connect to a soundweb device via serial
"""

import time
import queue

import serial

from sndweb import message

def connect(path):
    """Open a serial connection"""
    conn = serial.Serial(path, baudrate=38400, timeout=1/30)

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
        print("Giving up. Could not send message.")
        return

    ret = conn.write(buf)
    if ret != len(buf):
        print("Wrote {} to serial, expected {}.".format(ret, len(buf)))
        time.sleep(1)
        send(conn, buf, retry - 1)

    # Wait for ACK or NAK
    recv = conn.read()
    if recv == message.NAK:
        print("Received NAC from device. Trying to resend the message.")
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

        # if recv:
        #    print("0x%x " % (recv[0]), end="")

        # Begin of transmission
        if recv == message.STX:
           buf = b'' # Clear message buffer

        # End of transmission
        elif recv == message.ETX:
            # print("")
            try:
                body = message.decode_message_body(buf)
                conn.write(message.ACK)

                yield body
            except message.MessageError as e:
                # conn.write(message.NAK)
                pass

        # State / Responses
        elif recv == message.ACK:
            yield message.ACK
        elif recv == message.NAK:
            yield message.NAK
        else:
            # Just append the received byte
            buf += recv

        yield None

