# coding: utf-8
from __future__ import absolute_import
from video import video
from twitter import twitter
from core import core
from transition import transition
import time

__author__ = 'boselowitz'

DEFAULT_DELAY = .75
MAIN_PLAYIST = [
    {"function": transition.dissolve, "parameter": "WELCOME TO RAPID"},
    {"function": video.display_video, "parameter": "block-game"},
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "barber-pole-10s.mov"},
    {"function": transition.magichat, "parameter": "FOR EVERY $1.00 SPENT IN MANUFACTURING, ANOTHER $1.48 IS ADDED TO THE ECONOMY"},    
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "big-namii"},
    {"function": transition.magichat, "parameter": "IT'S TIME FOR AMERICA'S NEXT MOON SHOT."},
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "rocket-takeoff"},
    {"function": transition.magichat, "parameter": "IN AMERICA, YOU'VE GOT TO BE A LITTLE RECKLESS. YOU CAN'T BE AFRAID TO FAIL. THAT'S WHAT INNOVATION AND PROGRESS IS ALL ABOUT."},    
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "printer-namii"},
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "rocket-takeoff"},
    {"function": transition.righttoleft, "parameter": "IT'S TIME FOR AMERICA'S NEXT MOON SHOT. "},    
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "rocket-takeoff"},
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": transition.righttoleft, "parameter": "MANUFACTURERS ARE THE BACKBONE OF OUR ECONOMY."},    
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "big-namii"},
    {"function": transition.pop, "parameter": "WELCOME TO RAPID"},
    {"function": video.display_video, "parameter": "printer-welcome"},
    {"function": transition.righttoleft, "parameter": "COME HELP US SHAPE THE FUTURE OF NAMII"},
    {"function": twitter.display_direct_messages, "parameter": None},
    {"function": video.display_video, "parameter": "trampoline-man"},
    {"function": transition.righttoleft, "parameter": "77 MEMBERS AND COUNTING"},
]

QUIET_PLAYLIST = [
    {"function": transition.amdissolve, "parameter": "77 MEMBERS ++"},
    {"function": transition.amdissolve, "parameter": "FIRESIDE CHAT"},
    {"function": transition.dissolve, "parameter": "SHAPE THE FUTURE"},
]

DEFAULT_PLAYIST = QUIET_PLAYLIST

while True:
    for sequence in DEFAULT_PLAYIST:
        if sequence["parameter"] is not None:
            sequence["function"](sequence["parameter"])
        else:
            sequence["function"]()
