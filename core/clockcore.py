from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import chr
from builtins import range
from builtins import object
from past.utils import old_div
import time
from datetime import datetime, timedelta
from . import core
import serial

__author__ = 'boselowitz'

clockdict = {
    "0": b"\x3e\x45\x49\x3e",
    "1": b"\x01\x21\x7f\x01",
    "2": b"\x23\x45\x49\x31",
    "3": b"\x22\x49\x49\x36",
    "4": b"\x0c\x14\x24\x7f",
    "5": b"\x72\x51\x51\x4e",
    "6": b"\x1e\x29\x49\x06",
    "7": b"\x40\x47\x48\x70",
    "8": b"\x36\x49\x49\x36",
    "9": b"\x30\x49\x4a\x3c",
    ":": b"\x14",
    '?': b' OH0',
    "space": b"\x00"
}

TCOLUMN_CLOCK = 35
BITMASK = [1, 2, 4, 8, 0x10, 0x20, 0x40]
DEFAULT_DELAY = 0.2
RIGHT_JUSTIFY = 1
LEFT_JUSTIFY = 2
CENTER_JUSTIFY = 3
TROW = 7
ROW_BREAK = 75
reset = b'\x81'
row1 = b'\x81'
row2 = b'\x82'


#Clock functionaility
def getbytes(m, delim=clockdict["space"], dmult=1):
    buf = b''
    for x in m:
        if not clockdict.get(x):
            buf += clockdict['?']
        else:
            buf += clockdict[x]
        buf += delim * dmult
    return buf[:len(buf) - len(delim * dmult)]


def pad(m,padsym='',justify = CENTER_JUSTIFY):
    m = clockdict['space']+m+clockdict['space']
    padsym = clockdict['space']+clockdict['space'].join([clockdict[x] for x in padsym])
    if TCOLUMN_CLOCK - len(m) < len(padsym):
        #there is not enough space to pad the full symbols.. fill it instead with spaces
        padsym = clockdict['space']
    padlen = old_div((TCOLUMN_CLOCK-len(m)),len(padsym)) #this is the number of padsym to be padded
    if padlen == 0 and justify==CENTER_JUSTIFY:
        #no space to pad them properly.. make the pad sym as space
        padsym = clockdict['space']
        padlen = old_div((TCOLUMN_CLOCK-len(m)),len(padsym))
    extrachr = (TCOLUMN_CLOCK-len(m))%len(padsym) #the remainder

    if justify == LEFT_JUSTIFY:
        return m+(padlen*padsym)+(extrachr*clockdict['space'])
    elif justify == RIGHT_JUSTIFY:
        return (extrachr*clockdict['space'])+(padlen*padsym)+m
    elif justify == CENTER_JUSTIFY:
        if extrachr%2 == 0:
            sp1 = sp2 = old_div(extrachr,2)
        else:
            sp2 = old_div(extrachr,2)
            sp1 = sp2+1
        if padlen%2 == 0:
            return (sp1*clockdict['space'])+((old_div(padlen,2))*padsym)+m+((old_div(padlen,2))*padsym)+(sp2*clockdict['space'])
        else:
            return (sp1*clockdict['space'])+(((old_div(padlen,2))+1)*padsym)+m+((old_div(padlen,2))*padsym)+(sp2*clockdict['space'])


def fill(m,fillmask=127):
    ser_secondary.write(reset+row1)
    for i in range(len(m)):
        if i == ROW_BREAK:
            ser_secondary.write(reset+row2)
        ser_secondary.write(chr(ord(m[i])&fillmask))
    return m


def clear():
    fill(b"\x00" * TCOLUMN_CLOCK)


def display_clock():
    while True:
        fill(pad(getbytes(time.strftime("%H:%M:%S")), justify=CENTER_JUSTIFY))
        time.sleep(1)


def display_binary_clock():
    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        display_str = ""
        for power in range(6):
            power = 5 - power
            col = 0
            if old_div(hour, (2 ** power)):
                hour -= 2 ** power
                col |= ord(BITMASK[6])
            if old_div(minute, (2 ** power)):
                minute -= 2 ** power
                col |= ord(BITMASK[3])
            if old_div(second, (2 ** power)):
                second -= 2 ** power
                col |= ord(BITMASK[0])
            display_str = chr(col) + display_str

        fill(display_str + clockdict["space"] * 3 + getbytes(time.strftime("%H:%M")))
        time.sleep(1)


def display_count_down(finish_message):
    previous_fill = b""
    fill_in_value = b"\x7f" * TCOLUMN_CLOCK
    for hex_value in fill_in_value:
        for position in range(TROW):
            if len(previous_fill) % 2 == 0:
                flip_with_new_dot = hex_value | BITMASK[position]
                masked_off_top_bits = bytes([flip_with_new_dot & (0x7f >> (6 - position))])
            else:
                position = 6 - position
                flip_with_new_dot = hex_value | BITMASK[position]
                masked_off_top_bits = bytes([flip_with_new_dot & (0x7f << position)])
            fill(previous_fill + masked_off_top_bits)
            time.sleep(0.12)
            fill(core.negative(previous_fill) + masked_off_top_bits)
            time.sleep(0.12)
        previous_fill += masked_off_top_bits
        fill(previous_fill)

    fill(finish_message)


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


def display_count_down2(delta=timedelta(seconds=59)):
    future_date = datetime.now() + delta
    while future_date > datetime.now():
        fill(pad(getbytes(strfdelta(future_date - datetime.now(), "{minutes}:{seconds:02d}"))))
        time.sleep(.5)
        fill(core.negative(pad(getbytes(strfdelta(future_date - datetime.now(), "{minutes}:{seconds:02d}")))))
        time.sleep(.5)


class fallbackserialsecondary(object):
    LAST_MESSAGE_WAS_CONTROL = False
    CURSOR_POSITION = 0
    SCREEN_MATRIX = []

    def write(self, message):
        for character in message:
            if character > 128:
                #Row set
                if self.LAST_MESSAGE_WAS_CONTROL:
                    self.CURSOR_POSITION += (character - 129) * ROW_BREAK
                    self.LAST_MESSAGE_WAS_CONTROL = False
                #Col set
                else:
                    self.CURSOR_POSITION = character - 129
                    self.LAST_MESSAGE_WAS_CONTROL = True
            else:
                if not self.SCREEN_MATRIX:
                    for row in range(TROW):
                        self.SCREEN_MATRIX.append([])
                        for col in range(TCOLUMN_CLOCK):
                            self.SCREEN_MATRIX[row].append(".")

                character_value = character
                for row in range(TROW):
                    row_inverse = 6 - row
                    if self.CURSOR_POSITION < len(self.SCREEN_MATRIX[row]):
                        if character_value & BITMASK[row_inverse]:
                            character_value -= BITMASK[row_inverse]
                            self.SCREEN_MATRIX[row][self.CURSOR_POSITION] = "0"
                        else:
                            self.SCREEN_MATRIX[row][self.CURSOR_POSITION] = "."

                for row in range(TROW):
                    print(" ".join(self.SCREEN_MATRIX[row]))
                print("\n")

                self.CURSOR_POSITION += 1
                self.LAST_MESSAGE_WAS_CONTROL = False

try:
    ser_secondary = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400)
except serial.SerialException:
    print("Secondary serial port not opened, fallingback to text output")
    ser_secondary = fallbackserialsecondary()
