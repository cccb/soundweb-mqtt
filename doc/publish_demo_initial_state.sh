#!/bin/bash


MPUB=mosquitto_pub
BASE_TOPIC="soundweb"

function pub {
    $MPUB -t "$BASE_TOPIC/$1" -m "$2"
}

function set_level {
    pub "SET_LEVEL_REQUEST" "{\"id\": $1, \"value\": $2}"
}

function set_source {
    pub "SET_SOURCE_REQUEST" "{\"id\": $1, \"value\": $2}"
}

function set_toggle {
    pub "SET_TOGGLE_REQUEST" "{\"id\": $1, \"state\": $2}"
}


# == Levels
# Master Volume
set_level 1 42

# Delay (CenterLevel)
set_level 3 192
set_level 4 192

# Bar (CenterLevel)
set_level 5 192

# Source (linked)
set_source 2 1
set_source 7 1

# == Toggles
# Mute Mater
set_toggle 1 "false"

# Mute Delay
set_toggle 13 "false"

# Mute Bar
set_toggle 12 "true"


