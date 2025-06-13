from builtins import range
import time
from random import randint
from core import core
from video import video

####################
# BASE TRANSITIONS #
####################
def upnext(message):
    for j in range(3):
        for i in range(5):
            core.fill(core.negative(core.pad(core.getbytes("UP NEXT"), justify=core.CENTER_JUSTIFY)))
            time.sleep(0.25)
            core.fill(core.pad(core.getbytes("UP NEXT"), justify=core.CENTER_JUSTIFY))
            time.sleep(0.2)
            core.fill(core.negative(core.pad(core.getbytes("UP NEXT"), justify=core.CENTER_JUSTIFY)))
            time.sleep(0.1)
            core.fill(core.pad(core.getbytes("UP NEXT"), justify=core.CENTER_JUSTIFY))
            time.sleep(0.2)
        m = core.getbytes(message)
        if j == 2:
            core.scrollleft(core.pad(m, justify=core.CENTER_JUSTIFY), o=True, t=0.15, d=3)
        else:
            core.scrollleft(m, t=0.15, d=3)
    core.drawpacmanchased()

def righttoleft(message):
    core.scrollleft(core.pad(core.getbytes(message),justify=core.CENTER_JUSTIFY))

def pop(message):
    core.clear()
    for i in range(7):
        core.fill(core.pad(core.getbytes(message),justify=core.CENTER_JUSTIFY))
        time.sleep(0.25)
        core.fill(core.negative(core.pad(core.getbytes(message),justify=core.CENTER_JUSTIFY)))
        time.sleep(0.25)
    core.clear()
    time.sleep(1)

def amdissolve(message):
    core.fillmakerbot(core.pad(core.getbytes(message),justify=core.CENTER_JUSTIFY))
    time.sleep(2)
    core.filltypewriter(core.pad(b"",justify=core.CENTER_JUSTIFY))

def dissolve(message):
    core.fillmakerbot(core.pad(core.getbytes(message),justify=core.CENTER_JUSTIFY))
    time.sleep(2)
    core.eraserandomorder(core.pad(core.getbytes(message),justify=core.CENTER_JUSTIFY))

def magichat(message):
    long_string=message
    screens = []
    more = True
    while more:
        if len(long_string) <= 21:
            screens.append(long_string)
            more = False
            break
        for i in range(21, 0, -1):
            if long_string[i] == " " and len(core.getbytes(long_string[:i]))<104:
                screens.append(long_string[:i])
                long_string = long_string[i+1:]
                break
    for screen in range(len(screens)):
        core.fillfrombottomup(core.pad(core.getbytes(screens[screen]),justify=core.CENTER_JUSTIFY))
        time.sleep(1)
        core.scrollup(core.pad(core.getbytes(screens[screen]),justify=core.CENTER_JUSTIFY))
        #core.erasefrombottomup(core.pad(core.getbytes(screens[k]),justify=core.CENTER_JUSTIFY))

def adventurelook(message):
    long_string=message
    screens = []
    more = True
    while more:
        if len(long_string) <= 21:
            screens.append(long_string)
            more = False
            break
        for i in range(21, 0, -1):
            if long_string[i] == " " and len(core.getbytes(long_string[:i]))<105:
                screens.append(long_string[:i])
                long_string = long_string[i+1:]
                break
    for screen in range(len(screens)):
        if screen == len(screens)-1:
            core.fillfrombottomup(core.pad(core.getbytes(screens[screen]),justify=core.CENTER_JUSTIFY))
            time.sleep(5)
        else:
            core.fillfrombottomup(core.pad(core.getbytes(screens[screen]),justify=core.CENTER_JUSTIFY))
            time.sleep(1)
            core.erasefrombottomup(core.pad(core.getbytes(screens[screen]),justify=core.CENTER_JUSTIFY))


def plain(message):
    core.scrollleft(core.getbytes(message))

#################################
# RANDOMLY PICK BASE TRANSITION #
#################################
TRANSITION_LIST = [plain, upnext, magichat, adventurelook]
GENERAL_TRANSITION_LIST = [plain, magichat, adventurelook]
ANNOUNCEMENT_TRANSITION_LIST = [upnext]


def random_pick(pick_list):
    return pick_list[randint(0, len(pick_list) - 1)]


def random(message):
    random_pick(TRANSITION_LIST)(message)


def randomgeneral(message):
    random_pick(GENERAL_TRANSITION_LIST)(message)


def randomannouncement(message):
    random_pick(ANNOUNCEMENT_TRANSITION_LIST)(message)
