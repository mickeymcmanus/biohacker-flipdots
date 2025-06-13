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
#    {"function": transition.pop, "parameter": "MAKE AMERICA"},
#    {"function": transition.adventurelook, "parameter": "MAKE AMERICA"},
#    {"function": transition.plain, "parameter": "MAKE AMERICA"},
#    {"function": transition.upnext, "parameter": "MAKE AMERICA"},
#    {"function": video.display_video, "parameter": "barber-pole-10s.mov"},
#    {"function": transition.righttoleft, "parameter": "NAMII"},
    {"function": transition.amdissolve, "parameter": "FIRESIDE CHAT"},# seems broken because it calls core.fillmakerbot
#    {"function": transition.dissolve, "parameter": "THE FUTURE"}, # seems broken because it calls core.fillmakerbot
    {"function": transition.righttoleft, "parameter": "WELCOME TO RAPID"},
    {"function": transition.magichat, "parameter": "COME HELP US"},
 #   {"function": video.display_video, "parameter": "printer-welcome"},
 #   {"function": video.display_video, "parameter": "block-game"},
 #   {"function": twitter.display_direct_messages, "parameter": None},
 #   {"function": video.display_video, "parameter": "printer-namii"},
 #   {"function": transition.righttoleft, "parameter": "WIN A IPAD MINI -- NAMII SCAVENGER HUNT -- WINNERS CMU MECHANICAL ENGINEERING DEPARTMENT"},
 #   {"function": transition.magichat, "parameter": "FOR EVERY $1.00 SPENT IN MANUFACTURING, ANOTHER $1.48 IS ADDED TO THE ECONOMY"},
 #   {"function": twitter.display_direct_messages, "parameter": None},
]

QUIET_PLAYLIST = [
    {"function": transition.righttoleft, "parameter": "77 MEMBERS AND COUNTING"},
    {"function": transition.amdissolve, "parameter": "FIRESIDE CHAT"},
    {"function": transition.dissolve, "parameter": "SHAPE THE FUTURE"},
]

DEFAULT_PLAYIST = MAIN_PLAYIST

while True:
    for sequence in DEFAULT_PLAYIST:
        if sequence["parameter"] is not None:
            sequence["function"](sequence["parameter"])
        else:
            sequence["function"]()
