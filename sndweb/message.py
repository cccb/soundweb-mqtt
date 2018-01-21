

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


def _encode_body_char(char):
    char = char.to_bytes(1, 'big')

    # Substitute special chars
    special = {
        STX: ESC + b'\x82',
        ETX: ESC + b'\x83',
        ACK: ESC + b'\x86',
        NAK: ESC + b'\x95',
        ESC: ESC + b'\x9b',
    }

    # Substitute byte with escape sequence, if reqired
    subst = special.get(char)
    if subst:
        return subst

    return char


def _encode_message_body(body):
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


def _encode_message(body):
    """
    Encode a complete message
    """
    # Start message
    msg_buffer = STX
    # Add body
    msg_buffer += _encode_message_body(body)
    # End message
    msg_buffer += ETX

    return msg_buffer


def set_value(control_group, control_id, value):
    """Encode set value message"""
    message = SET_VALUE + \
              control_group.to_bytes(1, 'big') + \
              control_id.to_bytes(1, 'big') + \
              value.to_bytes(2, 'big')

    return _encode_message(message)

