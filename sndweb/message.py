

# Message constants
STX = b'\x02'
ETX = b'\x03'
ACK = b'\x06'
NAK = b'\x15'

ESC = b'\x1b'

# Commands
SET_VALUE = b'\x80'
SET_STRING = b'\x81'
REQUEST_VALUE = b'\x82'
REQUEST_STRING = b'\x83'
RAW_MSG = b'\x84'

# Groups
SW_AMX_BUTTON = 0
SW_AMX_TOGGLE = 1
SW_AMX_LED = 2
SW_AMX_PRESET = 3
SW_AMX_SPIN = 4
SW_AMX_LEVEL = 5
SW_AMX_SOURCE = 6
SW_AMX_TEXT = 7


class MessageError(Exception):
    pass

class ChecksumError(MessageError):
    pass



def decode_message_body(buf):
    """Decode bytes received"""
    if len(buf) < 2:
        # Message must at least have a byte + checksum
        raise MessageError()

    # Remove checksum
    buf_checksum = buf[-1]
    buf = buf[:-1]

    # Decode message
    message = b''
    is_escaped = False
    for c in buf:
        if c.to_bytes(1, 'big') == ESC:
            is_escaped = True
            continue
        res = c
        if is_escaped:
            res = c - 128
            is_escaped = False

        message += res.to_bytes(1, 'big')


    # Calculate body checksum
    checksum = 0
    for c in message:
        checksum ^= c

    if checksum != buf_checksum:
        raise ChecksumError()

    return message


def decode_message(body):
    """Decode message, create object from message"""
    message_type = body[:1]
    msg = {
        "type": message_type,
        "payload": _decode_payload(message_type, body),
    }

    return msg


def _decode_payload(message_type, body):
    if message_type == SET_VALUE:
        return _decode_set_value(body)
    elif message_type == SET_STRING:
        return _decode_set_string(body)

    return None


def _decode_set_value(body):
    group = body[1:2]
    control = body[2]
    value = int.from_bytes(body[3:5], "big")

    return {
        "group": group,
        "control": control,
        "value": value,
    }


def _decode_set_string(body):
    return "Implement Me"


def _encode_body_char(char):
    """Escape chars"""
    if char.to_bytes(1, 'big') in [STX, ETX, ACK, NAK, ESC]:
        # Substitute byte with escape sequence, if reqired
        return ESC + (char + 128).to_bytes(1, 'big')

    return char.to_bytes(1, 'big')


def encode_message_body(body):
    """
    Encode message body, escape chars
    """
    body_buffer = bytes()
    checksum = 0

    # Encode message
    for c in body:
        checksum ^= c
        body_buffer += _encode_body_char(c)

    # Append checksum
    body_buffer += _encode_body_char(checksum)

    return body_buffer


def encode_message(body):
    """
    Encode a complete message
    """
    # Start message
    msg_buffer = STX
    # Add body
    msg_buffer += encode_message_body(body)
    # End message
    msg_buffer += ETX

    return msg_buffer


def set_value(control_group, control_id, value):
    """Encode set value message"""
    message = SET_VALUE + \
              control_group.to_bytes(1, 'big') + \
              control_id.to_bytes(1, 'big') + \
              value.to_bytes(2, 'big')

    return encode_message(message)


def set_string(control_group, control_id, string):
    """Encode set string message"""
    message = SET_STRING + \
              control_group.to_bytes(1, 'big') + \
              control_id.to_bytes(1, 'big') + \
              string.encode('utf-8') + \
              b'\x00'

    return encode_message(message)


def request_value(control_group, control_id):
    """Encode request value message"""
    message = REQUEST_VALUE + \
              control_group.to_bytes(1, 'big') + \
              control_id.to_bytes(1, 'big')

    return encode_message(message)


def request_string(control_group, control_id):
    """Encode request string message"""
    message = REQUEST_STRING + \
              control_group.to_bytes(1, 'big') + \
              control_id.to_bytes(1, 'big')

    return encode_message(message)

