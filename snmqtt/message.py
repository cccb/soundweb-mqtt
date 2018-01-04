

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


def encode_message_body(body):
    """Encode message body, escap chars"""
    body_buffer = bytes()
    checksum = 0

    for c in body:
        checksum ^= c
        body_buffer += _encode_body_char(c.to_bytes(1, 'big'))

    return body_buffer




