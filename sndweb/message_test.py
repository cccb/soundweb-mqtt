
import pytest

from sndweb import message


def test_encode_body():

    # No substitutions
    body = b'\x23\x42\x00\xff'
    expected = b'\x23\x42\x00\xff\x9e'
    assert message.encode_body(body) == expected

    body = b'\x23\x02\x03\xff'
    expected = b'\x23\x1b\x82\x1b\x83\xff\xdd'
    assert message.encode_body(body) == expected


def test_decode_body():
    # Without substitutions
    body = b'\x23\x42\x00\xff'
    encoded = message.encode_body(body)
    assert body == message.decode_body(encoded)

    # With escaped chars
    body = b'\xfa\x02\x03\xff'
    encoded = message.encode_body(body)
    assert body == message.decode_body(encoded)

    # Trigger errors
    with pytest.raises(message.MessageError):
        message.decode_body(b'f')

    # with pytest.raises(message.ChecksumError):
    #    body = b'\xfa\x02\x03\xff'
    #    encoded = b'\xff' + message.encode_body(body)
    #    message.decode_body(encoded)



def test_encode_message():

    body = b'\x23\x02\x03\xff'
    msg = message.encode_message(body)

    assert msg[0] == 0x02
    assert msg[-1] == 0x03


def test_set_value():
    msg = message.set_value(0xf0, 0x0a, 0xfaaf)

    assert msg[0] == message.STX[0]
    assert msg[1] == 0x80
    assert msg[2] == 0xf0
    assert msg[3] == 0x0a
    assert msg[4] == 0xfa
    assert msg[5] == 0xaf
    assert msg[7] == message.ETX[0] # 6 is checksum


def test_set_string():
    msg = message.set_string(0xf0, 0x0a, "test")

    assert msg[0] == message.STX[0]
    assert msg[1] == 0x81


def test_decode_message():
    # Set value
    body = b'\x80\x05\x02\x00\xf0'
    msg = message.decode_message(body)

    assert msg["type"] == message.SET_VALUE
    assert msg["payload"]["group"] == message.SW_AMX_LEVEL
    assert msg["payload"]["id"] == 2
    assert msg["payload"]["value"] == 0xf0

    # Set string
    body = b'\x81\x07\x23\x74\x65\x73\x74\x00'
    msg = message.decode_message(body)

    assert msg["type"] == message.SET_STRING
    assert msg["payload"]["group"] == message.SW_AMX_TEXT
    assert msg["payload"]["id"] == 0x23
    assert msg["payload"]["value"] == "test"

