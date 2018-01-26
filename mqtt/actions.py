
SET_LEVEL_REQUEST = 'SET_LEVEL_REQUEST'
SET_LEVEL_SUCCESS = 'SET_LEVEL_SUCCESS'

GET_LEVEL_REQUEST = 'GET_LEVEL_REQUEST'
GET_LEVEL_SUCCESS = 'GET_LEVEL_SUCCESS'

GET_LEVELS_REQUEST = 'GET_LEVELS_REQUEST'
GET_LEVELS_SUCCESS = 'GET_LEVELS_SUCCESS'

SET_TOGGLE_REQUEST = 'SET_TOGGLE_REQUEST'
SET_TOGGLE_SUCCESS = 'SET_TOGGLE_SUCCESS'

GET_TOGGLE_REQUEST = 'GET_TOGGLE_REQUEST'
GET_TOGGLE_SUCCESS = 'GET_TOGGLE_SUCCESS'

GET_TOGGLES_REQUEST = 'GET_TOGGLES_REQUEST'
GET_TOGGLES_SUCCESS = 'GET_TOGGLES_SUCCESS'

SET_SOURCE_REQUEST = 'SET_SOURCE_REQUEST'
SET_SOURCE_SUCCESS = 'SET_SOURCE_SUCCESS'

GET_SOURCE_REQUEST = 'GET_SOURCE_REQUEST'
GET_SOURCE_SUCCESS = 'GET_SOURCE_SUCCESS'

GET_SOURCES_REQUEST = 'GET_SOURCES_REQUEST'
GET_SOURCES_SUCCESS = 'GET_SOURCES_SUCCESS'


def set_level_success(level_id, value):
    return {
        "type": SET_LEVEL_SUCCESS,
        "payload": {
            "id": level_id,
            "value": value,
        },
    }

def get_level_success(level_id, value):
    return {
        "type": GET_LEVEL_SUCCESS,
        "payload": {
            "id": level_id,
            "value": value,
        }
    }


def get_levels_success(levels):
    # Transform dict
    level_values = [{"id": k, "value": v} for k, v in levels.items()]

    return {
        "type": GET_LEVELS_SUCCESS,
        "payload": level_values,
    }


def set_toggle_success(toggle_id, state):
    return {
        "type": SET_TOGGLE_SUCCESS,
        "payload": {
            "id": toggle_id,
            "state": state == 1,
        }
    }


def get_toggle_success(toggle_id, state):
    return {
        "type": GET_TOGGLE_SUCCESS,
        "payload": {
            "state": state == 1,
            "id": toggle_id,
        }
    }


def get_toggles_success(toggles):
    level_values = [{"id": k, "value": v} for k, v in toggles.items()]

    return {
        "type": GET_TOGGLE_SUCCESS,
        "payload": level_values,
    }


def set_source_success(source_id, value):
    return {
        "type": SET_SOURCE_SUCCESS,
        "payload": {
            "id": source_id,
            "value": value,
        }
    }


def get_source_success(source_id, value):
    return {
        "type": GET_SOURCE_SUCCESS,
        "payload": {
            "id": source_id,
            "value": value,
        }
    }


def get_sources_success(sources):
    sources_values = [{"id": k, "value": v} for k, v in sources.items()]

    return {
        "type": GET_SOURCES_SUCCESS,
        "payload": sources_values,
    }


