
from snmqtt import message


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
    msg = message.encode_message(body)

    assert msg[0].to_bytes(1, 'big') == b'\x02'
    assert msg[-1].to_bytes(1, 'big') == b'\x03'


