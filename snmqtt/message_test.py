
from snmqtt import message


def test_encode_message_body():

    # No substitutions
    msg = b'\x23\x42\x00\xff'
    assert message.encode_message_body(msg) == msg

    msg = b'\x23\x02\x03\xff'
    expected = b'\x23\x1b\x82\x1b\x83\xff'
    assert message.encode_message_body(msg) == expected

