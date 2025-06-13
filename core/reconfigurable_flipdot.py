#!/usr/bin/env python3
"""
Reconfigurable Flipdot Display Controller - Protocol Compatible Version

This module provides a flexible control system for flipdot displays using
the exact same protocol as the original working core.py, but with 
configurable dimensions.
"""

import serial
import random
import time
from enum import Enum
from typing import List, Dict, Union, Optional, Tuple, ByteString
from dataclasses import dataclass

__author__ = 'boselowitz (protocol compatible version)'

# Display configuration presets
@dataclass
class DisplayConfig:
    """Configuration for a flipdot display setup."""
    name: str
    modules_wide: int
    modules_high: int
    module_width: int = 5  # pixels per module width
    module_height: int = 7  # pixels per module height
    
    @property
    def total_width(self) -> int:
        return self.modules_wide * self.module_width
    
    @property
    def total_height(self) -> int:
        return self.modules_high * self.module_height
    
    @property
    def total_pixels(self) -> int:
        return self.total_width * self.total_height
    
    @property
    def row_break(self) -> int:
        """Where display wraps to next row (for original protocol compatibility)."""
        return self.total_width


# Predefined configurations
DISPLAY_CONFIGS = {
    "current": DisplayConfig("Current 2x6", 6, 2),  # 30w × 14h
    "original": DisplayConfig("Original 21x1", 21, 1),  # 105w × 7h  
    "square": DisplayConfig("Square 4x4", 4, 4),  # 20w × 28h
    "wide": DisplayConfig("Wide 8x1", 8, 1),  # 40w × 7h
}

# Default to current configuration
DEFAULT_CONFIG = "current"

# Text height modes
class TextHeight(Enum):
    SINGLE = "single"  # Use only top row of modules
    DOUBLE = "double"  # Use both rows of modules
    AUTO = "auto"     # Choose based on text length


class Justify(Enum):
    RIGHT = 1
    LEFT = 2
    CENTER = 3


# Use the EXACT character dictionary from your original working core.py
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

# Use EXACT serial commands from your original working core.py
RESET = b'\x81'
ROW1 = b'\x82'  # This matches your working system
ROW2 = b'\x83'  # This matches your working system

# EXACT bitmask from original
BITMASK = [1, 2, 4, 8, 0x10, 0x20, 0x40]  # For 7-pixel high modules

DEFAULT_DELAY = 0.2


class FallbackSerial:
    """Simulates the flipdot display when hardware is not available."""
    
    def __init__(self, config: DisplayConfig):
        self.config = config
        self.screen_matrix = []
        self.cursor_col = 0
        self.cursor_row = 0
        self.last_message_was_control = False
        self.reset_screen()
        
    def reset_screen(self):
        """Initialize the screen matrix."""
        self.screen_matrix = [
            ['.' for _ in range(self.config.total_width)] 
            for _ in range(self.config.total_height)
        ]
        
    def write(self, message: bytes) -> None:
        """Simulate writing to the flipdot display using original protocol."""
        for byte_val in message:
            if byte_val == 0x81:  # RESET
                self.cursor_col = 0
                self.cursor_row = 0
                self.last_message_was_control = False
            elif byte_val == 0x82:  # ROW1
                self.cursor_row = 0
                self.last_message_was_control = False
            elif byte_val == 0x83:  # ROW2  
                self.cursor_row = min(7, self.config.total_height - 7)
                self.last_message_was_control = False
            elif byte_val > 128:
                # Handle original protocol positioning commands
                if self.last_message_was_control:
                    self.cursor_col += (byte_val - 129) * self.config.row_break
                    self.last_message_was_control = False
                else:
                    self.cursor_col = byte_val - 129
                    self.last_message_was_control = True
            else:
                # Character data - use original algorithm
                self._draw_byte_original_style(byte_val)
                self.cursor_col += 1
                if self.cursor_col >= self.config.total_width:
                    self.cursor_col = 0
                    
        self._print_screen()
                    
    def _draw_byte_original_style(self, byte_val: int):
        """Draw a byte using the original core.py algorithm."""
        for row in range(min(7, self.config.total_height - self.cursor_row)):
            actual_row = self.cursor_row + row
            row_inverse = 6 - row
            
            if (actual_row < self.config.total_height and 
                self.cursor_col < self.config.total_width):
                
                if byte_val & BITMASK[row_inverse]:
                    self.screen_matrix[actual_row][self.cursor_col] = 'O'
                else:
                    self.screen_matrix[actual_row][self.cursor_col] = '.'
                    
    def _print_screen(self):
        """Print the current screen state."""
        print("\n" + "="*self.config.total_width)
        for row in self.screen_matrix:
            print(''.join(row))
        print("="*self.config.total_width + "\n")


class ReconfigurableFlipdotDisplay:
    """Reconfigurable controller using original protocol."""
    
    def __init__(self, config_name: str = DEFAULT_CONFIG, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """
        Initialize the flipdot display.
        
        Args:
            config_name: Name of the display configuration to use
            port: Serial port for the display
            baud: Baud rate for serial communication
        """
        self.config = DISPLAY_CONFIGS[config_name]
        print(f"Initializing display: {self.config.name} ({self.config.total_width}×{self.config.total_height})")
        
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError):
            print("Serial port not available, using text simulation")
            self.serial = FallbackSerial(self.config)
    
    def get_text_bytes(self, message: str, delim: bytes = CHAR_DICT['space'], dmult: int = 1) -> bytes:
        """
        Convert text to display bytes using ORIGINAL algorithm.
        This matches your working core.getbytes() exactly.
        
        Args:
            message: Text to convert
            delim: Delimiter between characters  
            dmult: Delimiter multiplier
            
        Returns:
            Byte representation of the text
        """
        buf = b''
        for x in message:
            char_key = x.upper()  # Convert to uppercase for lookup
            if char_key not in CHAR_DICT:
                buf += CHAR_DICT.get('?', b'\x00')
            else:
                buf += CHAR_DICT[char_key]
            buf += delim * dmult
        
        # Remove the last delimiter (original behavior)
        return buf[:-len(delim * dmult)] if dmult > 0 and delim else buf
    
    def clear(self) -> None:
        """Clear the display using original protocol."""
        self.serial.write(RESET + ROW1)
        self.serial.write(b'\x00' * self.config.total_width)
        
        if self.config.modules_high > 1:
            self.serial.write(ROW2)
            self.serial.write(b'\x00' * self.config.total_width)
    
    def fill(self, message: bytes, fillmask: int = 127) -> bytes:
        """
        Fill display using ORIGINAL algorithm adapted for configurable size.
        
        Args:
            message: Bytes to display
            fillmask: Bitmask for filtering display content
            
        Returns:
            The displayed message
        """
        self.serial.write(RESET + ROW1)

        # Adapt original fill algorithm for configurable width
        total_pixels = self.config.total_width * self.config.modules_high
        
        for i in range(total_pixels):
            # Switch to ROW2 when we reach the second row of modules
            if i == self.config.total_width and self.config.modules_high > 1:
                self.serial.write(ROW2)

            # Original algorithm adapted
            if (i // self.config.total_width) % 2 == 0:
                # Top row or single row
                if i < len(message):
                    self.serial.write(bytes([message[i] & fillmask]))
                else:
                    self.serial.write(b"\x00")
            else:
                # Bottom row - use original backward logic
                col_in_row = i % self.config.total_width
                adjusted_index = col_in_row + (self.config.total_width - 1 - (2 * (col_in_row % 5)))
                
                if adjusted_index < len(message):
                    self.serial.write(bytes([message[adjusted_index] & fillmask]))
                else:
                    self.serial.write(b"\x00")

        return message
    
    def display_text(self, message: str, height_mode: TextHeight = TextHeight.AUTO, 
                    justify: Justify = Justify.CENTER, scroll: bool = True, 
                    scroll_speed: float = 0.2) -> None:
        """
        Display text using original protocol with smart sizing.
        
        Args:
            message: Text to display
            height_mode: How to handle text height
            justify: Text justification  
            scroll: Whether to scroll long text
            scroll_speed: Speed of scrolling
        """
        text_bytes = self.get_text_bytes(message)
        
        # Determine if we should scroll
        if len(text_bytes) <= self.config.total_width and not scroll:
            # Text fits, display statically
            padded = self._pad_text(text_bytes, justify)
            self.fill(padded)
        else:
            # Scroll the text using original-style algorithm
            self._scroll_text_original(text_bytes, scroll_speed)
    
    def _pad_text(self, text_bytes: bytes, justify: Justify) -> bytes:
        """Pad text using original algorithm."""
        if len(text_bytes) >= self.config.total_width:
            return text_bytes[:self.config.total_width]
        
        padding_needed = self.config.total_width - len(text_bytes)
        
        if justify == Justify.LEFT:
            return text_bytes + b'\x00' * padding_needed
        elif justify == Justify.RIGHT:
            return b'\x00' * padding_needed + text_bytes
        else:  # CENTER
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            return b'\x00' * left_pad + text_bytes + b'\x00' * right_pad
    
    def _scroll_text_original(self, text_bytes: bytes, speed: float) -> None:
        """Scroll text using algorithm similar to original scrollleft."""
        # Add padding for smooth scrolling (original style)
        padded_text = self.config.total_width * CHAR_DICT['space'] + text_bytes + self.config.total_width * CHAR_DICT['space']
        
        message_len = len(padded_text) - self.config.total_width
        d = 1  # Distance per step
        
        for k in range((message_len // d) + 1):
            chunk = padded_text[k*d:(k*d) + self.config.total_width]
            self.fill(chunk)
            time.sleep(speed)
    
    def display_frame(self, frame_data: bytes) -> None:
        """
        Display a video frame using original protocol.
        
        Args:
            frame_data: Raw frame data
        """
        if len(frame_data) > self.config.total_width:
            frame_data = frame_data[:self.config.total_width]
        elif len(frame_data) < self.config.total_width:
            frame_data += b'\x00' * (self.config.total_width - len(frame_data))
            
        self.fill(frame_data)
    
    def get_config_info(self) -> str:
        """Get information about the current display configuration."""
        return (f"Display: {self.config.name}\n"
                f"Modules: {self.config.modules_wide}×{self.config.modules_high}\n" 
                f"Pixels: {self.config.total_width}×{self.config.total_height}\n"
                f"Module size: {self.config.module_width}×{self.config.module_height}")

    # Original compatibility methods
    def negative(self, message: bytes) -> bytes:
        """Return the negative image of the buffer (original algorithm)."""
        return bytes([x ^ 127 for x in message])
    
    def raw_send(self, b: bytes, col: Optional[int] = None, row: Optional[int] = None) -> None:
        """Send raw bytes using original protocol."""
        if col is not None and (col < 129 or col > 204):
            print(f"Warning: Column index {col} may be out of range for this display")
        if row is not None and (row < 129 or row > 130):
            print(f"Warning: Row index {row} may be out of range for this display")
            
        if col:
            self.serial.write(bytes([col]))
        if row:
            self.serial.write(bytes([row]))
        self.serial.write(b)


# Convenience function
def create_display(config_name: str = DEFAULT_CONFIG, **kwargs) -> ReconfigurableFlipdotDisplay:
    """Create a display with the specified configuration."""
    return ReconfigurableFlipdotDisplay(config_name, **kwargs)


# Demo function
def demo():
    """Demonstrate the protocol-compatible reconfigurable display."""
    display = create_display("current")
    print(display.get_config_info())
    
    # Test messages that should work with original protocol
    test_messages = [
        "HELLO",
        "HI THERE", 
        "TESTING 123",
        "THIS IS A LONGER MESSAGE"
    ]
    
    for msg in test_messages:
        print(f"\nDisplaying: '{msg}'")
        display.display_text(msg, scroll=True, scroll_speed=0.15)
        time.sleep(1)
        
        display.clear()
        time.sleep(0.5)


if __name__ == "__main__":
    demo()
