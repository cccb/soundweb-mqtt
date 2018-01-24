

SET_LEVEL_REQUEST = 'SET_LEVEL_REQUEST'
SET_LEVEL_SUCCESS = 'SET_LEVEL_SUCCESS'

def set_level_success(level_id, value):
    return {
        "type": SET_LEVEL_SUCCESS,
        "payload": {
            "level_id": level_id,
            "value": value,
        },
    }

