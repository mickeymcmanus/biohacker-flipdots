#!/usr/bin/env python3
"""
Double Height Text Implementation for Flipdot Display

This module adds double-height text capability to your existing flipdot system.
Double-height characters are 14 pixels tall (spanning both rows) instead of 7.
"""

import time
import sys
import os
from typing import Dict, List, Tuple

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Double-height character dictionary (14 pixels tall)
# Each character is represented as a list of column bytes
# Top 7 bits go to top row, bottom 7 bits go to bottom row
double_height_dict = {
    'A': [
        0b0001111, 0b0010000, 0b0100000, 0b0100000, 0b0010000, 0b0001111, 0b0000000,  # Top row
        0b1111000, 0b0000100, 0b0000010, 0b0000010, 0b0000100, 0b1111000, 0b0000000   # Bottom row
    ],
    'B': [
        0b0111111, 0b0100001, 0b0100001, 0b0111110, 0b0000000,  # Top row
        0b1111110, 0b1000001, 0b1000001, 0b0111110, 0b0000000   # Bottom row
    ],
    'C': [
        0b0011110, 0b0100001, 0b0100000, 0b0100000, 0b0100001, 0b0010010, 0b0000000,  # Top row
        0b0111100, 0b1000010, 0b0000001, 0b0000001, 0b1000010, 0b0100100, 0b0000000   # Bottom row
    ],
    'D': [
        0b0111111, 0b0100001, 0b0100001, 0b0100001, 0b0011110, 0b0000000,  # Top row
        0b1111110, 0b1000001, 0b1000001, 0b1000001, 0b0111100, 0b0000000   # Bottom row
    ],
    'E': [
        0b0111111, 0b0100001, 0b0100001, 0b0100001, 0b0100000, 0b0000000,  # Top row
        0b1111111, 0b1000001, 0b1000001, 0b1000001, 0b0000001, 0b0000000   # Bottom row
    ],
    'F': [
        0b0111111, 0b0100000, 0b0100000, 0b0100000, 0b0100000, 0b0000000,  # Top row
        0b1111111, 0b1000000, 0b1000000, 0b0000000, 0b0000000, 0b0000000   # Bottom row
    ],
    'G': [
        0b0011110, 0b0100001, 0b0100000, 0b0100000, 0b0100001, 0b0010010, 0b0000000,  # Top row
        0b0111100, 0b1000010, 0b0000001, 0b0001111, 0b1000010, 0b0111100, 0b0000000   # Bottom row
    ],
    'H': [
        0b0111111, 0b0001000, 0b0001000, 0b0001000, 0b0111111, 0b0000000,  # Top row
        0b1111111, 0b0010000, 0b0010000, 0b0010000, 0b1111111, 0b0000000   # Bottom row
    ],
    'I': [
        0b0100001, 0b0111111, 0b0100001, 0b0000000,  # Top row
        0b1000001, 0b1111111, 0b1000001, 0b0000000   # Bottom row
    ],
    'J': [
        0b0000010, 0b0000001, 0b0000001, 0b0111110, 0b0000000,  # Top row
        0b0100000, 0b1000000, 0b1000000, 0b0111111, 0b0000000   # Bottom row
    ],
    'K': [
        0b0111111, 0b0001000, 0b0010100, 0b0100010, 0b0000001, 0b0000000,  # Top row
        0b1111111, 0b0010000, 0b0101000, 0b1000100, 0b0000010, 0b0000000   # Bottom row
    ],
    'L': [
        0b0111111, 0b0000001, 0b0000001, 0b0000001, 0b0000000,  # Top row
        0b1111111, 0b1000000, 0b1000000, 0b1000000, 0b0000000   # Bottom row
    ],
    'M': [
        0b0111111, 0b0100000, 0b0010000, 0b0001000, 0b0010000, 0b0100000, 0b0111111, 0b0000000,  # Top row
        0b1111111, 0b0000010, 0b0000100, 0b0001000, 0b0000100, 0b0000010, 0b1111111, 0b0000000   # Bottom row
    ],
    'N': [
        0b0111111, 0b0100000, 0b0010000, 0b0001000, 0b0000100, 0b0111111, 0b0000000,  # Top row
        0b1111111, 0b0000010, 0b0000100, 0b0001000, 0b0010000, 0b1111111, 0b0000000   # Bottom row
    ],
    'O': [
        0b0011110, 0b0100001, 0b0100001, 0b0100001, 0b0100001, 0b0011110, 0b0000000,  # Top row
        0b0111100, 0b1000010, 0b1000010, 0b1000010, 0b1000010, 0b0111100, 0b0000000   # Bottom row
    ],
    'P': [
        0b0111111, 0b0100000, 0b0100000, 0b0111111, 0b0000000,  # Top row
        0b1111111, 0b1001000, 0b1001000, 0b0110000, 0b0000000   # Bottom row
    ],
    'Q': [
        0b0011110, 0b0100001, 0b0100001, 0b0100001, 0b0100001, 0b0011110, 0b0000000,  # Top row
        0b0111100, 0b1000010, 0b1000110, 0b1001010, 0b1010010, 0b1111101, 0b0000000   # Bottom row
    ],
    'R': [
        0b0111111, 0b0100000, 0b0100000, 0b0111110, 0b0000001, 0b0000000,  # Top row
        0b1111111, 0b1001000, 0b1001000, 0b0110100, 0b0000011, 0b0000000   # Bottom row
    ],
    'S': [
        0b0110010, 0b0100001, 0b0100001, 0b0100001, 0b0100110, 0b0000000,  # Top row
        0b0100110, 0b1000001, 0b1000001, 0b1000001, 0b0100110, 0b0000000   # Bottom row
    ],
    'T': [
        0b0100000, 0b0100000, 0b0111111, 0b0100000, 0b0100000, 0b0000000,  # Top row
        0b0000000, 0b0000000, 0b1111111, 0b0000000, 0b0000000, 0b0000000   # Bottom row
    ],
    'U': [
        0b0111110, 0b0000001, 0b0000001, 0b0000001, 0b0111110, 0b0000000,  # Top row
        0b0111111, 0b1000000, 0b1000000, 0b1000000, 0b0111111, 0b0000000   # Bottom row
    ],
    'V': [
        0b0111000, 0b0000110, 0b0000001, 0b0000110, 0b0111000, 0b0000000,  # Top row
        0b0001111, 0b0110000, 0b1000000, 0b0110000, 0b0001111, 0b0000000   # Bottom row
    ],
    'W': [
        0b0111111, 0b0000010, 0b0001100, 0b0000010, 0b0111111, 0b0000000,  # Top row
        0b1111111, 0b0100000, 0b0011000, 0b0100000, 0b1111111, 0b0000000   # Bottom row
    ],
    'X': [
        0b0100001, 0b0010010, 0b0001100, 0b0010010, 0b0100001, 0b0000000,  # Top row
        0b1000001, 0b0100010, 0b0011000, 0b0100010, 0b1000001, 0b0000000   # Bottom row
    ],
    'Y': [
        0b0100000, 0b0010000, 0b0001111, 0b0010000, 0b0100000, 0b0000000,  # Top row
        0b0000000, 0b0000000, 0b1111111, 0b0000000, 0b0000000, 0b0000000   # Bottom row
    ],
    'Z': [
        0b0100001, 0b0100011, 0b0100101, 0b0101001, 0b0110001, 0b0000000,  # Top row
        0b1000001, 0b1100001, 0b1010001, 0b1001001, 0b1000110, 0b0000000   # Bottom row
    ],
    ' ': [
        0b0000000, 0b0000000, 0b0000000,  # Top row
        0b0000000, 0b0000000, 0b0000000   # Bottom row
    ],
    '0': [
        0b0011110, 0b0100001, 0b0100101, 0b0101001, 0b0110001, 0b0011110, 0b0000000,  # Top row
        0b0111100, 0b1000110, 0b1001010, 0b1010010, 0b1000010, 0b0111100, 0b0000000   # Bottom row
    ],
    '1': [
        0b0100010, 0b0111111, 0b0000010, 0b0000000,  # Top row
        0b1000000, 0b1111111, 0b1000000, 0b0000000   # Bottom row
    ],
    '2': [
        0b0100010, 0b0100011, 0b0100101, 0b0101001, 0b0110001, 0b0000000,  # Top row
        0b1100000, 0b1010000, 0b1001000, 0b1000100, 0b1000011, 0b0000000   # Bottom row
    ],
    '3': [
        0b0100010, 0b0100001, 0b0101001, 0b0101001, 0b0011110, 0b0000000,  # Top row
        0b0100000, 0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000   # Bottom row
    ],
    '4': [
        0b0001000, 0b0011000, 0b0101000, 0b0111111, 0b0001000, 0b0000000,  # Top row
        0b0001000, 0b0001000, 0b0001000, 0b1111111, 0b0001000, 0b0000000   # Bottom row
    ],
    '5': [
        0b0111001, 0b0101001, 0b0101001, 0b0101001, 0b0100110, 0b0000000,  # Top row
        0b0100000, 0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000   # Bottom row
    ],
    '6': [
        0b0011110, 0b0101001, 0b0101001, 0b0101001, 0b0100110, 0b0000000,  # Top row
        0b0111110, 0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000   # Bottom row
    ],
    '7': [
        0b0100000, 0b0100000, 0b0100111, 0b0101000, 0b0110000, 0b0000000,  # Top row
        0b0000000, 0b0000000, 0b1111111, 0b0000000, 0b0000000, 0b0000000   # Bottom row
    ],
    '8': [
        0b0011110, 0b0101001, 0b0101001, 0b0101001, 0b0011110, 0b0000000,  # Top row
        0b0111110, 0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000   # Bottom row
    ],
    '9': [
        0b0110010, 0b0101001, 0b0101001, 0b0101001, 0b0011110, 0b0000000,  # Top row
        0b0111110, 0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000   # Bottom row
    ],
    '!': [
        0b0111101, 0b0000000,  # Top row
        0b1111011, 0b0000000   # Bottom row
    ],
    '?': [
        0b0100000, 0b0100000, 0b0100101, 0b0101000, 0b0110000, 0b0000000,  # Top row
        0b0000000, 0b0000000, 0b1111011, 0b0000000, 0b0000000, 0b0000000   # Bottom row
    ],
}

def get_double_height_bytes(message: str, delim_cols: int = 1) -> Tuple[bytes, bytes]:
    """
    Convert a message string to double-height display bytes.
    
    Args:
        message: Text to convert
        delim_cols: Number of blank columns between characters
        
    Returns:
        Tuple of (top_row_bytes, bottom_row_bytes)
    """
    top_bytes = []
    bottom_bytes = []
    
    for char in message.upper():
        if char in double_height_dict:
            char_data = double_height_dict[char]
            char_width = len(char_data) // 2  # Split between top and bottom
            
            # Add character columns
            for i in range(char_width):
                top_bytes.append(char_data[i])
                bottom_bytes.append(char_data[i + char_width])
            
            # Add delimiter columns
            for _ in range(delim_cols):
                top_bytes.append(0)
                bottom_bytes.append(0)
        else:
            # Unknown character - use space
            for _ in range(3 + delim_cols):
                top_bytes.append(0)
                bottom_bytes.append(0)
    
    return bytes(top_bytes), bytes(bottom_bytes)

def display_double_height_text(core_instance, message: str, justify: str = 'left'):
    """
    Display double-height text on the flipdot display using the correct buffer mapping.
    
    Args:
        core_instance: Instance of WorkingFlipdotCore
        message: Text to display
        justify: Text justification ('left', 'center', 'right')
    """
    top_bytes, bottom_bytes = get_double_height_bytes(message)
    
    # Calculate positioning for 30-column display
    text_width = len(top_bytes)
    
    if justify == 'center':
        padding = max(0, (30 - text_width) // 2)
    elif justify == 'right':
        padding = max(0, 30 - text_width)
    else:  # left
        padding = 0
    
    # Create the 105-byte buffer using your display's actual mapping
    display_buffer = [0] * 105
    
    # Fill the top row (first 30 columns)
    for i in range(min(30, len(top_bytes))):
        col_pos = padding + i
        if col_pos < 30:
            display_buffer[col_pos] = top_bytes[i]
    
    # Fill the bottom row (starts at position 75, not 30!)
    for i in range(min(30, len(bottom_bytes))):
        col_pos = padding + i
        if col_pos < 30:
            display_buffer[75 + col_pos] = bottom_bytes[i]  # Use 75 offset, not 30
    
    core_instance.fill(bytes(display_buffer))

def scroll_double_height_left(core_instance, message: str, t: float = 0.2, d: int = 1):
    """
    Scroll double-height text from right to left using correct buffer mapping.
    
    Args:
        core_instance: Instance of WorkingFlipdotCore
        message: Text to scroll
        t: Time delay between frames
        d: Number of columns to advance per frame
    """
    top_bytes, bottom_bytes = get_double_height_bytes(message)
    
    # Add padding for smooth scrolling
    padding = 30
    padded_top = bytes([0] * padding) + top_bytes + bytes([0] * padding)
    padded_bottom = bytes([0] * padding) + bottom_bytes + bytes([0] * padding)
    
    total_width = len(padded_top)
    
    for offset in range(0, total_width - 30 + 1, d):
        # Extract 30-column window
        display_top = padded_top[offset:offset + 30]
        display_bottom = padded_bottom[offset:offset + 30]
        
        # Pad to ensure 30 columns
        if len(display_top) < 30:
            display_top += bytes([0] * (30 - len(display_top)))
        if len(display_bottom) < 30:
            display_bottom += bytes([0] * (30 - len(display_bottom)))
        
        # Create 105-byte buffer with correct mapping
        display_buffer = [0] * 105
        
        # Top row (positions 0-29)
        for i in range(30):
            display_buffer[i] = display_top[i]
        
        # Bottom row (positions 75-104)
        for i in range(30):
            display_buffer[75 + i] = display_bottom[i]
        
        core_instance.fill(bytes(display_buffer))
        time.sleep(t)

def typewriter_double_height(core_instance, message: str, char_delay: float = 0.2):
    """
    Display double-height text with typewriter effect using correct buffer mapping.
    
    Args:
        core_instance: Instance of WorkingFlipdotCore
        message: Text to display
        char_delay: Delay between characters
    """
    for i in range(1, len(message) + 1):
        partial_message = message[:i]
        display_double_height_text(core_instance, partial_message, justify='left')
        time.sleep(char_delay)

def display_text_from_bytes_double_height(core_instance, top_bytes, bottom_bytes):
    """
    Display double-height text from pre-generated bytes using correct buffer mapping.
    """
    # Center the text
    text_width = len(top_bytes)
    padding = max(0, (30 - text_width) // 2)
    
    # Create the 105-byte buffer 
    display_buffer = [0] * 105
    
    # Fill top row (positions 0-29)
    for i in range(min(30, len(top_bytes))):
        col_pos = padding + i
        if col_pos < 30:
            display_buffer[col_pos] = top_bytes[i]
    
    # Fill bottom row (positions 75-104)  
    for i in range(min(30, len(bottom_bytes))):
        col_pos = padding + i
        if col_pos < 30:
            display_buffer[75 + col_pos] = bottom_bytes[i]
    
    core_instance.fill(bytes(display_buffer))

# Example usage functions
def demo_double_height(core_instance):
    """Demonstrate double-height text capabilities."""
    print("Demo: Double Height Text")
    
    # Static display
    print("1. Static double-height text...")
    display_double_height_text(core_instance, "HELLO", justify='center')
    time.sleep(3)
    
    # Scrolling
    print("2. Scrolling double-height text...")
    scroll_double_height_left(core_instance, "SCROLLING TEXT", t=0.15)
    
    # Typewriter
    print("3. Typewriter double-height effect...")
    typewriter_double_height(core_instance, "TYPE", char_delay=0.5)
    time.sleep(2)
    
    # Clear
    core_instance.clear()
    print("Demo complete!")

# Integration with existing transition system
def double_height_plain(core_instance, message: str):
    """Plain double-height text display."""
    display_double_height_text(core_instance, message, justify='center')
    time.sleep(3)

def double_height_scroll(core_instance, message: str):
    """Scrolling double-height text."""
    scroll_double_height_left(core_instance, message)

def double_height_typewriter(core_instance, message: str):
    """Typewriter double-height text."""
    typewriter_double_height(core_instance, message)
    time.sleep(2)

# Add to your existing transition lists
DOUBLE_HEIGHT_TRANSITIONS = [
    double_height_plain,
    double_height_scroll, 
    double_height_typewriter
]

if __name__ == "__main__":
    # Test the double-height implementation
    from core import working_core
    
    print("Testing Double Height Text Implementation")
    print("=" * 50)
    
    try:
        demo_double_height(working_core)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
