# coding: utf-8
from __future__ import absolute_import
from video import video
from twitter import twitter
from transition import transition
from games.scavengerhunt import scavengerhunt
import time

__author__ = 'boselowitz'

DEFAULT_DELAY = .75
MAIN_PLAYIST = [
    {"function": transition.righttoleft, "parameter": "Welcome to the Biohacker Floor"},
    {"function": transition.upnext, "parameter": "DNA Beware!"},
    {"function": transition.dissolve, "parameter": "Bio"},
    {"function": transition.magichat, "parameter": "biohacker"},
    {"function": video.display_video, "parameter": "barber-pole-10s.mov"},
 #   {"function": video.display_video, "parameter": "block-game"},
]


DEFAULT_PLAYIST = MAIN_PLAYIST

while True:
    for sequence in DEFAULT_PLAYIST:
        if sequence["parameter"] is not None:
            sequence["function"](sequence["parameter"])
        else:
            sequence["function"]()
