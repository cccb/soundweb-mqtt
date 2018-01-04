
from snmqtt import message


def test_encode_message_body():

    # No substitutions
    msg = b'\x23\x42\x00\xff'
    expected = b'\x23\x42\x00\xff\x9e'
    assert message.encode_message_body(msg) == expected

    msg = b'\x23\x02\x03\xff'
    expected = b'\x23\x1b\x82\x1b\x83\xff\xdd'
    assert message.encode_message_body(msg) == expected

