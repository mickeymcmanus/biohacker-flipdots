#!/usr/bin/env python3
"""
Fixed Protocol-Compatible Flipdot Core

This matches your original protocol EXACTLY but sends the right amount of data
for your 30×14 display.
"""

import serial
import time
from typing import Optional

# Use EXACT constants from your diagnostic output
TROW = 7  # Keep original for compatibility
TCOLUMN = 30  # Your actual display width
ROW_BREAK = 30  # Your actual display width

# EXACT commands from your working system
RESET = b'\x81'
ROW1 = b'\x81'  # Your system uses \x81 twice
ROW2 = b'\x82'  # Your system uses \x82 for row 2

# EXACT character dictionary from your original
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

class FixedFlipdotDisplay:
    """Fixed flipdot display that matches your original protocol exactly."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize with your exact serial port."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
    
    def get_text_bytes(self, message: str, delim: bytes = CHAR_DICT['space'], dmult: int = 1) -> bytes:
        """Convert text to bytes using EXACT original algorithm."""
        buf = b''
        for x in message.upper():
            if x not in CHAR_DICT:
                buf += CHAR_DICT.get('?', b'\x00')
            else:
                buf += CHAR_DICT[x]
            buf += delim * dmult
        
        # Remove the last delimiter (original behavior)
        return buf[:-len(delim * dmult)] if dmult > 0 and delim else buf
    
    def clear(self) -> None:
        """Clear display using EXACT original protocol."""
        # Send exactly what your original sends but with correct length
        self.serial.write(b'\x81\x81')  # RESET + ROW1 (your pattern)
        self.serial.write(b'\x00' * TCOLUMN)  # Clear top row (30 bytes)
        
        self.serial.write(b'\x81\x82')  # RESET + ROW2 (your pattern)  
        self.serial.write(b'\x00' * TCOLUMN)  # Clear bottom row (30 bytes)
    
    def flip(self, message: str, d: int = 1) -> None:
        """Display text using EXACT original flip algorithm."""
        i = 0
        self.serial.write(b'\x81\x81')  # RESET + ROW1 (your exact pattern)
        
        for k in message.upper():
            i += 1
            try:
                c = CHAR_DICT[k]
            except KeyError:
                c = CHAR_DICT.get('?', b'\x00')
                
            if i > 5:  # Adjust for your display width (rough estimate)
                if i == 6:
                    self.serial.write(b'\x81\x82')  # RESET + ROW2
                # For second row, we might need to reverse or adjust
                # Let's try sending normally first
            
            self.serial.write(c)
    
    def fill(self, message: bytes, fillmask: int = 127) -> bytes:
        """Fill display using corrected original algorithm."""
        self.serial.write(b'\x81\x81')  # RESET + ROW1 (your pattern)

        # Send top row data
        for i in range(TCOLUMN):
            if i < len(message):
                self.serial.write(bytes([message[i] & fillmask]))
            else:
                self.serial.write(b"\x00")

        # Send bottom row data
        self.serial.write(b'\x81\x82')  # RESET + ROW2 (your pattern)
        
        # For bottom row, start from where top row ended
        start_idx = TCOLUMN
        for i in range(TCOLUMN):
            if start_idx + i < len(message):
                self.serial.write(bytes([message[start_idx + i] & fillmask]))
            else:
                self.serial.write(b"\x00")

        return message
    
    def scroll_left(self, message: bytes, t: float = 0.2, d: int = 1) -> None:
        """Scroll text using original algorithm."""
        # Add padding for smooth scrolling
        padded_message = TCOLUMN * CHAR_DICT['space'] + message + TCOLUMN * CHAR_DICT['space']
        
        message_len = len(padded_message) - TCOLUMN
        
        for k in range((message_len // d) + 1):
            chunk = padded_message[k*d:(k*d) + TCOLUMN]
            self.fill(chunk)
            time.sleep(t)

def test_fixed_display():
    """Test the fixed display."""
    print("=== Testing Fixed Display ===")
    
    display = FixedFlipdotDisplay()
    
    try:
        print("1. Testing clear...")
        display.clear()
        time.sleep(2)
        
        print("2. Testing simple text 'HI'...")
        display.flip("HI")
        time.sleep(3)
        
        print("3. Testing fill with pattern...")
        test_pattern = b'\x7F\x00' * 15  # 30 bytes alternating
        display.fill(test_pattern)
        time.sleep(3)
        
        print("4. Testing text bytes...")
        text_bytes = display.get_text_bytes("HELLO")
        print(f"   'HELLO' = {len(text_bytes)} bytes: {text_bytes.hex()}")
        display.fill(text_bytes)
        time.sleep(3)
        
        print("5. Testing scroll...")
        scroll_text = display.get_text_bytes("SCROLL TEST")
        display.scroll_left(scroll_text, t=0.15)
        
        print("6. Final clear...")
        display.clear()
        
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_display()
