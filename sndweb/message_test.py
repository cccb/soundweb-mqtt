
from sndweb import message


def test_encode_message_body():

    # No substitutions
    body = b'\x23\x42\x00\xff'
    expected = b'\x23\x42\x00\xff\x9e'
    assert message._encode_message_body(body) == expected

    body = b'\x23\x02\x03\xff'
    expected = b'\x23\x1b\x82\x1b\x83\xff\xdd'
    assert message._encode_message_body(body) == expected


def test_encode_message():

    body = b'\x23\x02\x03\xff'
    msg = message._encode_message(body)

    assert msg[0] == 0x02
    assert msg[-1] == 0x03


def test_set_value():
    msg = message.set_value(0xf0, 0x0a, 0xfaaf)

    assert msg[0] == message.STX[0]
    assert msg[1] == message.SET_VALUE[0]
    assert msg[2] == 0xf0
    assert msg[3] == 0x0a
    assert msg[4] == 0xfa
    assert msg[5] == 0xaf
    assert msg[7] == message.ETX[0] # 6 is checksum
