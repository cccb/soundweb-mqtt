

SET_LEVEL_REQUEST = 'SET_LEVEL_REQUEST'
SET_LEVEL_SUCCESS = 'SET_LEVEL_SUCCESS'

GET_LEVEL_REQUEST = 'GET_LEVEL_REQUEST'
GET_LEVEL_SUCCESS = 'GET_LEVEL_SUCCESS'


def set_level_success(level_id, value):
    return {
        "type": SET_LEVEL_SUCCESS,
        "payload": {
            "level_id": level_id,
            "value": value,
        },
    }

def get_level_success(level_id, value):
    return {
        "type": GET_LEVEL_SUCCESS,
        "payload": {
            "level_id": level_id,
            "value": value,
        }
    }

