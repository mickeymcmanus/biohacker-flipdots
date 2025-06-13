#!/usr/bin/env python3
"""
Flipdot Display Controller

This module provides control for a flipdot display via serial connection.
It supports text display, animations, and patterns.

Reference: http://www.flipdots.com/EN/applications/page-15/big_electromagnetic_displays.html
"""

import serial
import random
import time
from enum import Enum
from typing import List, Dict, Union, Optional, Tuple, ByteString

__author__ = 'boselowitz (modernized version)'

# Display Constants
TROW = 7  # Number of rows in the display
TCOLUMN = 105  # Number of columns in the display
ROW_BREAK = 85  # Column index where the display wraps to the next row
BITMASK = [1, 2, 4, 8, 0x10, 0x20, 0x40]  # Bitmask for each row
DEFAULT_DELAY = 0.2  # Default animation delay


# Justification options
class Justify(Enum):
    RIGHT = 1
    LEFT = 2
    CENTER = 3


# Serial control commands
RESET = b'\x81'
ROW1 = b'\x81'
ROW2 = b'\x82'


# Character dictionary for display
CHAR_DICT = {
    ' ': b'\x00\x00\x00',
    '$': b'2I\x7fI&',
    '(': b'>A',
    ',': b'\x01\x06',
    '0': b'>AAA>',
    '4': b'\x1c$D\x7f\x04',
    '8': b'6III6',
    '<': b'\x08\x14"',
    '@': b'\x1f\x10\x17\x15\x1f',
    'D': b'\x7fAAA>',
    'H': b'\x7f\x08\x08\x08\x7f',
    'L': b'\x7f\x01\x01\x01',
    'P': b'\x7fHHH0',
    'T': b'@@\x7f@@',
    'X': b'A"\x1c"A',
    '\\': b'`\x1c\x03',
    '`': b'@ ',
    'd': b'\x0e\x11\x11\x7f',
    'h': b'\x7f\x10\x10\x10\x0f',
    'l': b'~\x01',
    'p': b'?$$\x18',
    't': b'\x10>\x11',
    'x': b'\x1b\x04\x04\x1b',
    '|': b'w',
    '#': b'\x14\x7f\x14\x7f\x14',
    "'": b'`',
    'space': b'\x00',
    '+': b'\x08\x08>\x08\x08',
    '/': b'\x03\x1c`',
    '3': b'"AII6',
    '7': b'`@GX`',
    ';': b'\x016',
    '?': b' OH0',
    'C': b'>AAA"',
    'G': b'>AAI/',
    'K': b'\x7f\x08\x14"A',
    'O': b'>AAA>',
    'S': b'2III&',
    'W': b'~\x01\x01~\x01\x01~',
    '[': b'\x7fA',
    '_': b'\x01\x01\x01',
    'c': b'\x0e\x11\x11\x11',
    'g': b'\x81\x15\x15\x15\x0e',
    'k': b'\x7f\x06\n\x11',
    'o': b'\x0e\x11\x11\x0e',
    's': b'\t\x15\x15\x12',
    'w': b'\x1e\x01\x01\x1e\x01\x01\x1e',
    '{': b'\x086A',
    '"': b'``',
    '&': b'7IE+\x07',
    '*': b'(\x10|\x10(',
    '.': b'\x01',
    '2': b'!CEI1',
    '6': b'\x1e)II\x06',
    ':': b'6',
    '>': b'"\x14\x08',
    'B': b'\x7fIII6',
    'F': b'\x7fHH@',
    'J': b'\x02\x01A~',
    'N': b'\x7f \x10\x08\x04\x7f',
    'R': b'\x7fHHH7',
    'V': b'x\x06\x01\x06x',
    'Z': b'CEIQa',
    '^': b' @ ',
    'b': b'\x7f\x11\x11\x0e',
    'f': b'\x10?P',
    'j': b'\x11^',
    'n': b'\x1f\x10\x10\x0f',
    'r': b'\x1f\x08\x10',
    'v': b'\x1e\x01\x01\x1e',
    'z': b'\x13\x14\x14\x19',
    '~': b'\x08\x10\x08\x04\x08',
    '!': b'}',
    '%': b'1JL>\x19)F',
    ')': b'A>',
    '-': b'\x08\x08\x08\x08\x08',
    '1': b' \x7f',
    '5': b'rQQQN',
    '9': b'0IIJ<',
    '=': b'\x14\x14\x14\x14',
    'A': b'?HHH?',
    'E': b'\x7fIIA',
    'I': b'\x7f',
    'M': b'\x7f \x10\x08\x10 \x7f',
    'Q': b'<BFB=',
    'U': b'~\x01\x01\x01~',
    'Y': b'`\x10\x0f\x10`',
    ']': b'A\x7f',
    'a': b'\x0e\x11\x11\x1f',
    'e': b'\x0e\x15\x15\r',
    'i': b'\x10_',
    'm': b'\x1f\x10\x10\x0f\x10\x10\x0f',
    'q': b'\x18$$?',
    'u': b'\x1e\x01\x01\x1f',
    'y': b'8\x05\x05>',
    '}': b'A6\x08'
}


class FallbackSerial:
    """Simulates the flipdot display when hardware is not available."""
    
    def __init__(self):
        self.last_message_was_control = False
        self.cursor_position = 0
        self.screen_matrix = []
        
    def write(self, message: bytes) -> None:
        """
        Simulates writing to the flipdot display.
        
        Args:
            message: Bytes to send to the display
        """
        for char_byte in message:
            # Python 3 returns int for bytes iteration
            character = char_byte  
            
            if character > 128:
                # Row set
                if self.last_message_was_control:
                    self.cursor_position += (character - 129) * ROW_BREAK
                    self.last_message_was_control = False
                # Col set
                else:
                    self.cursor_position = character - 129
                    self.last_message_was_control = True
            else:
                # Initialize screen matrix if needed
                if not self.screen_matrix:
                    self.screen_matrix = [["." for _ in range(TCOLUMN)] for _ in range(TROW)]
                
                character_value = character
                for row in range(TROW):
                    row_inverse = 6 - row
                    if self.cursor_position < len(self.screen_matrix[row]):
                        if character_value & BITMASK[row_inverse]:
                            character_value -= BITMASK[row_inverse]
                            self.screen_matrix[row][self.cursor_position] = "0"
                        else:
                            self.screen_matrix[row][self.cursor_position] = "."
                
                # Print the screen matrix
                for row in range(TROW):
                    print(" ".join(self.screen_matrix[row]))
                print("\n")
                
                self.cursor_position += 1
                self.last_message_was_control = False


class FlipdotDisplay:
    """Controller for the flipdot display."""
    
    def __init__(self, port='/dev/tty.usbserial-A3000lDq', baud=38400):
        """
        Initialize the flipdot display.
        
        Args:
            port: Serial port for the display
            baud: Baud rate for serial communication
        """
        try:
            self.serial = serial.Serial(port, baud)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError):
            print("Main serial port not opened, falling back to text output")
            self.serial = FallbackSerial()
    
    def display_image(self, frame):
        """For future implementation."""
        pass
    
    def raw_send(self, b: bytes, col: Optional[int] = None, row: Optional[int] = None) -> None:
        """
        Send raw bytes to the flipdot display at specified position.
        
        Args:
            b: Bytes to send
            col: Column position (129-204)
            row: Row position (129-130)
        """
        if col is not None and (col < 129 or col > 204):
            raise ValueError(f"Column index {col} out of range (129-204)")
        if row is not None and (row < 129 or row > 130):
            raise ValueError(f"Row index {row} out of range (129-130)")
            
        print((col, row, [x for x in b]))
        if col:
            self.serial.write(bytes([col]))
        if row:
            self.serial.write(bytes([row]))
        self.serial.write(b)
    
    def clear(self) -> None:
        """Clear the display."""
        self.fill(b'\x00' * TCOLUMN)
    
    def flip(self, message: str, d: int = 1) -> None:
        """
        Display text on the flipdot.
        
        Args:
            message: Text to display
            d: Delay between characters
        """
        i = 0
        self.serial.write(RESET + ROW1)
        for k in message:
            i += 1
            try:
                c = CHAR_DICT[k]
            except KeyError:
                # Use '?' for unknown characters
                c = CHAR_DICT.get('?', b'\x00')
                
            if i > 15:
                if i == 16:
                    self.serial.write(RESET + ROW2)
                # Reverse the string for the second row
                c = c[::-1]
            self.serial.write(c)

    def get_bytes(self, message: str, delim: bytes = CHAR_DICT['space'], dmult: int = 1) -> bytes:
        """
        Convert text to display bytes with delimiter between characters.
        
        Args:
            message: Text to convert
            delim: Delimiter to use between characters
            dmult: Number of times to repeat the delimiter
            
        Returns:
            Byte representation of the text
        """
        buf = b''
        for x in message:
            if x not in CHAR_DICT:
                buf += CHAR_DICT.get('?', b'\x00')
            else:
                buf += CHAR_DICT[x]
            buf += delim * dmult
        
        # Remove the last delimiter
        return buf[:-len(delim * dmult)] if dmult > 0 and delim else buf
    
    def fill(self, message: bytes, fillmask: int = 127) -> bytes:
        """
        Fill the display with the given byte pattern.
        
        Args:
            message: Bytes to display
            fillmask: Bitmask for filtering display content
            
        Returns:
            The displayed message
        """
        self.serial.write(RESET + ROW1)

        for i in range(150):
            if i == ROW_BREAK:
                self.serial.write(RESET + ROW2)

            if (i // 30) % 2 == 0:
                if i < len(message):
                    self.serial.write(bytes([message[i] & fillmask]))
                else:
                    self.serial.write(b"\x00")
            else:
                # Backward row, need to manipulate
                index = ((i % 30) + (25 - (10 * ((i % 30) // 5)))) + (30 * (i // 30))
                if index < len(message):
                    self.serial.write(bytes([message[index] & fillmask]))
                else:
                    self.serial.write(b"\x00")

        return message
    
    def pad(self, message: bytes, padsym: str = '', justify: Justify = Justify.CENTER) -> bytes:
        """
        Pad a message to fill the display width with the given symbol.
        
        Args:
            message: Bytes to pad
            padsym: Symbol to use for padding
            justify: Justification (LEFT, RIGHT, or CENTER)
            
        Returns:
            Padded message
        """
        message = CHAR_DICT['space'] + message + CHAR_DICT['space']
        
        if padsym:
            padsym_bytes = CHAR_DICT['space'] + CHAR_DICT['space'].join(
                [CHAR_DICT[x] for x in padsym if x in CHAR_DICT]
            )
        else:
            padsym_bytes = CHAR_DICT['space']
            
        if TCOLUMN - len(message) < len(padsym_bytes):
            # Not enough space for padding, use spaces
            padsym_bytes = CHAR_DICT['space']
            
        padlen = (TCOLUMN - len(message)) // len(padsym_bytes)
        extrachr = (TCOLUMN - len(message)) % len(padsym_bytes)
        
        if justify == Justify.LEFT:
            return message + (padlen * padsym_bytes) + (extrachr * CHAR_DICT['space'])
        elif justify == Justify.RIGHT:
            return (extrachr * CHAR_DICT['space']) + (padlen * padsym_bytes) + message
        elif justify == Justify.CENTER:
            if extrachr % 2 == 0:
                sp1 = sp2 = extrachr // 2
            else:
                sp2 = extrachr // 2
                sp1 = sp2 + 1
                
            if padlen % 2 == 0:
                pad_left = pad_right = padlen // 2
            else:
                pad_right = padlen // 2
                pad_left = pad_right + 1
                
            return (sp1 * CHAR_DICT['space']) + (pad_left * padsym_bytes) + message + \
                   (pad_right * padsym_bytes) + (sp2 * CHAR_DICT['space'])
        else:
            raise ValueError(f"Unknown justification: {justify}")
    
    def negative(self, message: bytes) -> bytes:
        """
        Return the negative image of the buffer.
        
        Args:
            message: Original message bytes
            
        Returns:
            Negated message bytes
        """
        return bytes([x ^ 127 for x in message])
    
    # Animation methods
    def scroll_left(self, message: bytes, t: float = DEFAULT_DELAY, d: int = 1,
                   pause_delay: Optional[float] = None, only_pad_left: bool = False) -> bytes:
        """
        Scroll text from right to left across the display.
        
        Args:
            message: Message to scroll
            t: Time delay between scroll steps
            d: Distance to scroll per step
            pause_delay: Optional delay in the middle of scrolling
            only_pad_left: If True, only pad left side with spaces
            
        Returns:
            Updated buffer after scrolling
        """
        if not only_pad_left:
            padded_message = TCOLUMN * CHAR_DICT['space'] + message + TCOLUMN * CHAR_DICT['space']
        else:
            padded_message = TCOLUMN * CHAR_DICT['space'] + message
            
        message_len = len(padded_message) - TCOLUMN
        
        for k in range((message_len // d) + 1):
            self.fill(padded_message[k*d:(k*d) + TCOLUMN])
            
            if pause_delay and k == ((message_len // d) + 1) // 2:
                time.sleep(pause_delay - t)
                
            time.sleep(t)
            
        return padded_message
    
    def rotate_left(self, message: bytes, t: float = DEFAULT_DELAY, d: int = 1) -> bytes:
        """
        Rotate the display content to the left.
        
        Args:
            message: Message to rotate
            t: Time delay between rotation steps
            d: Distance to rotate per step
            
        Returns:
            Updated buffer after rotation
        """
        for k in range(TCOLUMN // d):
            self.fill(message)
            message = message[d:] + message[:d]
            time.sleep(t)
        return message
    
    def rotate_right(self, message: bytes, t: float = DEFAULT_DELAY, d: int = 1) -> bytes:
        """
        Rotate the display content to the right.
        
        Args:
            message: Message to rotate
            t: Time delay between rotation steps
            d: Distance to rotate per step
            
        Returns:
            Updated buffer after rotation
        """
        for k in range(TCOLUMN // d):
            self.fill(message)
            message = message[-d:] + message[:-d]
            time.sleep(t)
        return message
    
    def scroll_up(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Scroll the display content upward.
        
        Args:
            message: Message to scroll
            t: Time delay between scroll steps
            
        Returns:
            Updated buffer after scrolling
        """
        for _ in range(TROW):
            message = bytes([(x << 1) & 127 for x in message])
            self.fill(message)
            time.sleep(t)
        return message
    
    def scroll_down(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Scroll the display content downward.
        
        Args:
            message: Message to scroll
            t: Time delay between scroll steps
            
        Returns:
            Updated buffer after scrolling
        """
        for _ in range(TROW):
            message = bytes([x >> 1 for x in message])
            self.fill(message)
            time.sleep(t)
        return message
    
    def fill_from_bottom_up(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Animate filling the display from bottom to top.
        
        Args:
            message: Message to display
            t: Time delay between animation steps
            
        Returns:
            The displayed message
        """
        btm = 0
        for k in range(len(BITMASK)):
            btm += BITMASK[k]
            self.fill(message, btm)
            time.sleep(t)
        return message
    
    def fill_from_top_down(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Animate filling the display from top to bottom.
        
        Args:
            message: Message to display
            t: Time delay between animation steps
            
        Returns:
            The displayed message
        """
        btm = 0
        for k in range(len(BITMASK) - 1, -1, -1):
            btm += BITMASK[k]
            self.fill(message, btm)
            time.sleep(t)
        return message
    
    def erase_from_top_down(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Animate erasing the display from top to bottom.
        
        Args:
            message: Message to erase
            t: Time delay between animation steps
            
        Returns:
            The erased message
        """
        btm = 127
        for k in range(len(BITMASK) - 1, -1, -1):
            btm -= BITMASK[k]
            self.fill(message, btm)
            time.sleep(t)
        return message
    
    def erase_from_bottom_up(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Animate erasing the display from bottom to top.
        
        Args:
            message: Message to erase
            t: Time delay between animation steps
            
        Returns:
            The erased message
        """
        btm = 127
        for k in range(len(BITMASK)):
            btm -= BITMASK[k]
            self.fill(message, btm)
            time.sleep(t)
        return message
    
    def fill_random_order(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Animate filling the display in random order.
        
        Args:
            message: Message to display
            t: Time delay between animation steps
            
        Returns:
            The displayed message
        """
        btm = 0
        for k in range(8):
            if k < 6:
                btm = min(random.getrandbits(TROW), 127)
            else:
                btm = min(btm + random.getrandbits(TROW), 127)
            self.fill(message, btm)
            time.sleep(t)
            
        if btm < 127:
            self.fill(message)  # Fill it all up in case any are left out
            
        return message
    
    def erase_random_order(self, message: bytes, t: float = DEFAULT_DELAY) -> bytes:
        """
        Animate erasing the display in random order.
        
        Args:
            message: Message to erase
            t: Time delay between animation steps
            
        Returns:
            The erased message
        """
        btm = 127
        for k in range(8):
            if k < 6:
                btm = max(127 - random.getrandbits(TROW), 0)
            else:
                btm = max(btm - random.getrandbits(TROW), 0)
            self.fill(message, btm)
            time.sleep(t)
            
        if btm > 0:
            self.clear()  # Clear it all in case any are left
            
        return message
    
    def fill_typewriter(self, message: bytes) -> None:
        """
        Animate filling the display like a typewriter.
        
        Args:
            message: Message to display
        """
        col = 129
        row = 129
        for hex_value in message:
            for position in range(TROW):
                flip_with_new_dot = hex_value | BITMASK[position]
                masked_off_top_bits = flip_with_new_dot & (0x7f >> (6 - position))
                self.raw_send(bytes([masked_off_top_bits]), col=col, row=row)
                time.sleep(.06)
            self.raw_send(bytes([hex_value]), col=col, row=row)
            col += 1
            if col == 204:
                row += 1
                col = 129
    
    def fill_makerbot(self, message: bytes) -> None:
        """
        Animate filling the display with makerbot pattern.
        
        Args:
            message: Message to display
        """
        col = 129
        row = 129
        for hex_value in message:
            for position in range(TROW):
                if col % 2 == 0:
                    # For even columns
                    safe_position = min(position, 6)
                    flip_with_new_dot = hex_value | BITMASK[safe_position]
                    masked_off_top_bits = flip_with_new_dot & (0x7f >> (6 - safe_position))
                else:
                    # For odd columns
                    safe_position = min(position, 6)
                    adjusted_position = 6 - safe_position
                    flip_with_new_dot = hex_value | BITMASK[safe_position]
                    masked_off_top_bits = flip_with_new_dot & (0x7f << adjusted_position)
                
                self.raw_send(bytes([masked_off_top_bits]), col=col, row=row)
                time.sleep(.06)
            
            self.raw_send(bytes([hex_value]), col=col, row=row)
            col += 1

            if col == 204:
                row += 1
                col = 129
    
    # Pattern animation methods
    def draw_pattern_left_to_right(self, p: bytes = b'', trail_pattern: bytes = b'',
                                  dist: int = 1, picklist: List[bytes] = None,
                                  picklen: int = 1, t: float = DEFAULT_DELAY) -> None:
        """
        Draw a pattern from left to right across the display.
        
        Args:
            p: Pattern to display
            trail_pattern: Pattern to show in the trail
            dist: Distance to move per step
            picklist: List of patterns to cycle through
            picklen: Number of patterns to pick from picklist per step
            t: Time delay between animation steps
        """
        if picklist:
            p = picklist[0:picklen]
        p += trail_pattern
        pr = p[::-1]
        plen = len(pr)
        
        if plen > ROW_BREAK or plen < 1:
            return  # Pattern is too long to be repeated properly
            
        colst = 129
        rowst = 129
        
        for cyc in range(TCOLUMN // dist):
            if picklist:
                # Get the pattern value for this iteration
                st = cyc % len(picklist)
                if picklen == 1:
                    p = picklist[st] + trail_pattern
                    pr = p[::-1]
                else:
                    if st + picklen <= len(picklist):
                        pr = trail_pattern + b''.join(picklist[st:st + picklen])
                    else:
                        pr = (trail_pattern + 
                              b''.join(picklist[-(len(picklist) - st):]) + 
                              b''.join(picklist[:picklen - (len(picklist) - st)]))
                plen = len(pr)
                
            if (dist * cyc) == 0:
                for i in range(plen):
                    if picklist and picklen == 1:
                        st = i % len(picklist)
                        p = picklist[st] + trail_pattern
                        pr = p[::-1]
                    nx = -i - 1
                    self.raw_send(pr[nx:], colst, rowst)
                    if i < plen - 1:
                        time.sleep(t)
            elif (dist * cyc) + plen < ROW_BREAK:
                self.raw_send(pr, colst + (dist * cyc), rowst)
            elif (dist * cyc) < ROW_BREAK:
                nx = ROW_BREAK - (dist * cyc)
                self.raw_send(pr[:nx], colst + (dist * cyc), rowst)
                self.raw_send(pr[nx:], colst + (dist * cyc) - ROW_BREAK + nx, rowst + 1)
            else:
                self.raw_send(pr, colst + (dist * cyc) - ROW_BREAK, rowst + 1)
                
            print("endline")
            time.sleep(t)


# Predefined patterns
class Patterns:
    """Predefined patterns for animations."""
    
    ARROW = b'\x08\x1c\x3e\x08\x08\x7f'  # arrow pattern
    PACMAN = b'\x22\x36\x2a\x22\x1c'
    BUGS = b'\x1e\x34\x22\x34\x1e'
    PICKLIST = [b'\x01', b'\x02', b'\x04', b'\x08', b'\x10', b' b', b'@', b'@', 
                b' b', b'\x10', b'\x08', b'\x04', b'\x02', b'\x01']
    OPICKLIST = [b'@', b' b', b'\x10', b'\x08', b'\x04', b'\x02', b'\x01', b'\x01', 
                 b'\x02', b'\x04', b'\x08', b'\x10', b' b', b'@']
    
    # Pre-computed patterns for animations
    PACMANLIST = [
        b'\x00\x41\x63\x77\x7f\x3e\x1c',
        b'\x22\x77\x7f\x7f\x7f\x3e\x1c',
        b'\x1c\x3e\x7f\x7f\x7f\x3e\x1c',
        b'\x22\x77\x7f\x7f\x7f\x3e\x1c',
        b'\x00\x41\x63\x77\x7f\x3e\x1c'
    ]
    
    PACMONSTERLIST = [
        b'\x3f\x42\x51\x42\x51\x42\x3f',
        b'\x3f\x42\x41\x42\x41\x42\x3f'
    ]


class FlipdotAnimations:
    """Animation sequences for the flipdot display."""
    
    def __init__(self, display: FlipdotDisplay):
        """
        Initialize animations with the specified display.
        
        Args:
            display: Flipdot display to use for animations
        """
        self.display = display
    
    def draw_pacman(self, trail: int = 0, d: int = 1, t: float = DEFAULT_DELAY) -> None:
        """
        Draw the PacMan animation.
        
        Args:
            trail: If non-zero, show a trail
            d: Distance to move per step
            t: Time delay between animation steps
        """
        if trail == 0:
            trail_pattern = b'\x00'
        else:
            trail_pattern = b''
            
        self.display.draw_pattern_left_to_right(
            p=b'',
            trailpattern=trail_pattern,
            dist=d,
            picklist=Patterns.PACMANLIST,
            picklen=1,
            t=t
        )
    
    def draw_pacman_chased(self, monsters_num: int = 2, d: int = 10, t: float = DEFAULT_DELAY) -> None:
        """
        Draw the PacMan being chased by ghosts.
        
        Args:
            monsters_num: Number of monster ghosts
            d: Distance between elements
            t: Time delay between animation steps
        """
        pacman_chased = []
        for i in range(len(Patterns.PACMANLIST)):
            pacman_chased.append(
                Patterns.PACMANLIST[i] + 
                b'\x00' * d + 
                Patterns.PACMONSTERLIST[i % 2] + 
                b'\x00' * d + 
                Patterns.PACMONSTERLIST[(i + 1) % 2]
            )
            
        self.display.draw_pattern_left_to_right(
            trailpattern=b'\x00',
            t=t,
            picklist=pacman_chased
        )


def main():
    """Main function to demonstrate the flipdot display."""
    display = FlipdotDisplay()
    animations = FlipdotAnimations(display)
    
    # Clear the display
    display.clear()
    
    # Display a welcome message
    message = "Hello Flipdot!"
    message_bytes = display.get_bytes(message)
    
    # Demonstrate different animations
    display.fill(message_bytes)
    time.sleep(1)
    
    display.scroll_left(message_bytes)
    time.sleep(0.5)
    
    display.rotate_left(message_bytes)
    time.sleep(0.5)
    
    display.fill_from_bottom_up(message_bytes)
    time.sleep(0.5)
    
    display.erase_from_top_down(message_bytes)
    time.sleep(0.5)
    
    # Run the PacMan animation
    animations.draw_pacman()
    time.sleep(0.5)
    
    animations.draw_pacman_chased()
    
    # Final message
    display.fill_typewriter(display.get_bytes("GOODBYE!"))
    time.sleep(2)
    display.clear()


#############################################
# COMPATIBILITY LAYER FOR EXISTING SCRIPTS  #
#############################################

# Create global instances for backward compatibility
_display = FlipdotDisplay()
_animations = FlipdotAnimations(_display)

# Re-export constants to maintain compatibility with old code
RIGHT_JUSTIFY = Justify.RIGHT.value
LEFT_JUSTIFY = Justify.LEFT.value
CENTER_JUSTIFY = Justify.CENTER.value
dict = CHAR_DICT  # Note: This shadows the built-in dict but matches original code
reset = RESET
row1 = ROW1
row2 = ROW2

# Create backwards-compatible module-level functions
def display_image(frame):
    return _display.display_image(frame)

def flip(m, d=1):
    return _display.flip(m, d)

def rotate_left(s, d=1):
    """Original rotate_left function (string operation)"""
    return s[d:] + s[:d]

def rotate_right(s, d=1):
    """Original rotate_right function (string operation)"""
    return s[-d:] + s[:-d]

def addspacers(m, spacelen=1):
    """Add spacers between characters"""
    return (CHAR_DICT['space'] * spacelen).join(m)

def pad(m, padsym='', justify=CENTER_JUSTIFY):
    return _display.pad(m, padsym, Justify(justify))

def fill(m, fillmask=127):
    return _display.fill(m, fillmask)

def filltypewriter(message):
    return _display.fill_typewriter(message)

def fillmakerbot(message):
    return _display.fill_makerbot(message)

def fillfrombottomup(m, t=DEFAULT_DELAY):
    return _display.fill_from_bottom_up(m, t)

def fillfromtopdown(m, t=DEFAULT_DELAY):
    return _display.fill_from_top_down(m, t)

def scrolldown(m, t=DEFAULT_DELAY, wraparound=False):
    return _display.scroll_down(m, t)

def scrollup(m, t=DEFAULT_DELAY, wraparound=False):
    return _display.scroll_up(m, t)

def erasefromtopdown(m, t=DEFAULT_DELAY):
    return _display.erase_from_top_down(m, t)

def erasefrombottomup(m, t=DEFAULT_DELAY):
    return _display.erase_from_bottom_up(m, t)

def fillrandomorder(m, t=DEFAULT_DELAY):
    return _display.fill_random_order(m, t)

def eraserandomorder(m, t=DEFAULT_DELAY):
    return _display.erase_random_order(m, t)

def getbytes(m, delim=dict['space'], dmult=1):
    return _display.get_bytes(m, delim, dmult)

def clear():
    return _display.clear()

def rotateleft(m, t=DEFAULT_DELAY, d=1):
    return _display.rotate_left(m, t, d)

def rotateright(m, t=DEFAULT_DELAY, d=1):
    return _display.rotate_right(m, t, d)

def scrollleft(m, t=DEFAULT_DELAY, d=1, pausedelay=None, o=False):
    return _display.scroll_left(m, t, d, pausedelay, o)

def negative(m):
    return _display.negative(m)

def raw_send(b, col=None, row=None):
    return _display.raw_send(b, col, row)

def drawpacman(trail=0, d=1, t=DEFAULT_DELAY):
    return _animations.draw_pacman(trail, d, t)

def drawpacmanchased(monstersnum=2, d=10, t=DEFAULT_DELAY):
    return _animations.draw_pacman_chased(monstersnum, d, t)

def drawpatternlefttoright(p=b'', trailpattern=b'', dist=1, picklist=None, picklen=1, t=DEFAULT_DELAY):
    return _display.draw_pattern_left_to_right(p, trailpattern, dist, picklist, picklen, t)

def drawpatternrighttoleft(p=b'', trailpattern=b'', dist=1, picklist=None, picklen=1, t=DEFAULT_DELAY):
    return _display.draw_pattern_right_to_left(p, trailpattern, dist, picklist, picklen, t)

# Also expose the original global variables for pattern definitions
p = Patterns.ARROW
pqman = Patterns.PACMAN
pcbugs = Patterns.BUGS
picklist = Patterns.PICKLIST
opicklist = Patterns.OPICKLIST
mpicklist = bytes([x[0][0] | x[1][0] for x in zip(picklist, opicklist)])
pacmanlist = Patterns.PACMANLIST
pacmonsterlist = Patterns.PACMONSTERLIST

# Make the original serial object available (for scripts that might access it directly)
try:
    ser_main = _display.serial
except AttributeError:
    # Fallback if the serial attribute isn't exactly as expected
    ser_main = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400) if not isinstance(_display.serial, FallbackSerial) else _display.serial


if __name__ == "__main__":
    main()
    
    def draw_pattern_right_to_left(self, p: bytes = b'', trail_pattern: bytes = b'',
                                  dist: int = 1, picklist: List[bytes] = None,
                                  picklen: int = 1, t: float = DEFAULT_DELAY) -> None:
        """
        Draw a pattern from right to left across the display.
        
        Args:
            p: Pattern to display
            trail_pattern: Pattern to show in the trail
            dist: Distance to move per step
            picklist: List of patterns to cycle through
            picklen: Number of patterns to pick from picklist per step
            t: Time delay between animation steps
        """
        if picklist:
            p = picklist[0:picklen]
        p += trail_pattern
        plen = len(p)
        
        if plen > ROW_BREAK or plen < 1:
            return  # Pattern is too long to be repeated properly
            
        pr = p[::-1]
        colst = 199
        rowst = 130
        
        for cyc in range(TCOLUMN // dist):
            if picklist:
                # Get the pattern value for this iteration
                st = cyc % len(picklist)
                if st + picklen <= len(picklist):
                    p = b''.join(picklist[st:st + picklen]) + trail_pattern
                else:
                    p = (b''.join(picklist[-(len(picklist) - st):]) + 
                         b''.join(picklist[:picklen - (len(picklist) - st)]) + 
                         trail_pattern)
                pr = p
                
            if (dist * cyc) == 0:
                for i in range(plen):
                    nx = -i - 1
                    self.raw_send(pr[nx:], colst - i, rowst)
            elif (dist * cyc) + plen < ROW_BREAK:
                self.raw_send(pr, colst + (dist * cyc), rowst)
            elif (dist * cyc) < ROW_BREAK:
                nx = ROW_BREAK - (dist * cyc)
                self.raw_send(pr[:nx], colst + (dist * cyc), rowst)
                self.raw_send(pr[nx:], colst + (dist * cyc) - ROW_BREAK + nx, rowst + 1)
            else:
                self.raw_send(pr, colst + (dist * cyc) - ROW_BREAK, rowst + 1)
                
            print("endline")
            time.sleep(t)
