#!/usr/bin/env python3
"""
Refined Double Height Characters

Now that we know the buffer mapping works, create properly designed 
double-height characters that look good on your display.
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, getbytes, clear, dict as char_dict

def display_double_height_char(top_bytes, bottom_bytes):
    """Display double-height character using proven method."""
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105  
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    top_chunk = padded_top[103:103 + 105]
    bottom_chunk = padded_bottom[103:103 + 105] 
    
    double_buffer = list(top_chunk)
    for i, byte in enumerate(bottom_chunk):
        if i + 30 < 105:
            double_buffer[i + 30] = byte
    
    working_core.fill(bytes(double_buffer))

# Based on your single-height patterns, create better double-height versions
# Your single 'A' is: [63, 72, 72, 72, 63] = [0b0111111, 0b1001000, 0b1001000, 0b1001000, 0b0111111]

REFINED_DOUBLE_HEIGHT = {
    'A': {
        # Top half: Peak and upper sides of A
        'top': [0b0011100, 0b0100010, 0b0100010, 0b0100010, 0b0011100, 0b0000000],
        # Bottom half: Crossbar and legs  
        'bottom': [0b1111111, 0b1001000, 0b1001000, 0b1001000, 0b1111111, 0b0000000]
    },
    'B': {
        # B is tricky - top has upper curves, bottom has lower curves
        'top': [0b1111111, 0b1001000, 0b1001000, 0b0110000, 0b0000000],
        'bottom': [0b0110000, 0b1001000, 0b1001000, 0b1111111, 0b0000000]
    },
    'C': {
        # C: Top curve and bottom curve
        'top': [0b0111110, 0b1000001, 0b1000000, 0b1000000, 0b0000000],
        'bottom': [0b1000000, 0b1000000, 0b1000001, 0b0111110, 0b0000000]
    },
    'D': {
        # D: Curved right side
        'top': [0b1111111, 0b1000001, 0b1000001, 0b0100010, 0b0000000],
        'bottom': [0b0100010, 0b1000001, 0b1000001, 0b1111111, 0b0000000] 
    },
    'E': {
        # E: Top bar, middle bar, bottom bar
        'top': [0b1111111, 0b1001000, 0b1001000, 0b1000000, 0b0000000],
        'bottom': [0b1001000, 0b1001000, 0b1001000, 0b1111111, 0b0000000]
    },
    'F': {
        # F: Top bar, middle bar, but no bottom bar
        'top': [0b1111111, 0b1001000, 0b1001000, 0b1000000, 0b0000000],
        'bottom': [0b1000000, 0b1000000, 0b1000000, 0b1000000, 0b0000000]
    },
    'G': {
        # G: Like C but with inner horizontal line
        'top': [0b0111110, 0b1000001, 0b1000000, 0b1000000, 0b0000000],
        'bottom': [0b1001111, 0b1001001, 0b1000001, 0b0111110, 0b0000000]
    },
    'H': {
        # H: Two vertical lines with crossbar in middle
        'top': [0b1111111, 0b0001000, 0b0001000, 0b0001000, 0b0000000],
        'bottom': [0b0001000, 0b0001000, 0b0001000, 0b1111111, 0b0000000]
    },
    'I': {
        # I: Top and bottom bars with center line
        'top': [0b1000001, 0b1111111, 0b1000001, 0b0000000],
        'bottom': [0b1000001, 0b1111111, 0b1000001, 0b0000000]
    },
    'J': {
        # J: Top bar, then curve at bottom
        'top': [0b1100000, 0b1000000, 0b1000000, 0b1111111, 0b0000000],
        'bottom': [0b0000010, 0b0000001, 0b1000001, 0b0111110, 0b0000000]
    },
    'K': {
        # K: Vertical line with diagonal lines
        'top': [0b1111111, 0b0001000, 0b0010100, 0b0100010, 0b0000000],
        'bottom': [0b0010100, 0b0100010, 0b1000001, 0b0000000]
    },
    'L': {
        # L: Vertical line with bottom bar
        'top': [0b1111111, 0b0000001, 0b0000001, 0b0000001, 0b0000000],
        'bottom': [0b0000001, 0b0000001, 0b0000001, 0b0000001, 0b0000000]
    },
    'M': {
        # M: Two peaks
        'top': [0b1111111, 0b0100000, 0b0010000, 0b0100000, 0b1111111, 0b0000000],
        'bottom': [0b1111111, 0b0000000, 0b0000000, 0b0000000, 0b1111111, 0b0000000]
    },
    'N': {
        # N: Diagonal connection
        'top': [0b1111111, 0b0010000, 0b0001000, 0b0000100, 0b0000000],
        'bottom': [0b0010000, 0b0001000, 0b0000100, 0b1111111, 0b0000000]
    },
    'O': {
        # O: Oval shape
        'top': [0b0111110, 0b1000001, 0b1000001, 0b1000001, 0b0000000],
        'bottom': [0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000]
    },
    'P': {
        # P: Top part with crossbar, plain bottom
        'top': [0b1111111, 0b1001000, 0b1001000, 0b0110000, 0b0000000],
        'bottom': [0b1000000, 0b1000000, 0b1000000, 0b1000000, 0b0000000]
    },
    'Q': {
        # Q: Like O but with tail
        'top': [0b0111110, 0b1000001, 0b1000001, 0b1000001, 0b0000000],
        'bottom': [0b1000001, 0b1000011, 0b1000001, 0b0111111, 0b0000000]
    },
    'R': {
        # R: Like P but with leg
        'top': [0b1111111, 0b1001000, 0b1001000, 0b0110000, 0b0000000],
        'bottom': [0b0010100, 0b0001010, 0b0000101, 0b1000011, 0b0000000]
    },
    'S': {
        # S: Curve at top and bottom
        'top': [0b0110010, 0b1001001, 0b1001000, 0b1000000, 0b0000000],
        'bottom': [0b0000001, 0b0001001, 0b1001001, 0b0100110, 0b0000000]
    },
    'T': {
        # T: Top bar with center stem
        'top': [0b1000000, 0b1000000, 0b1111111, 0b1000000, 0b1000000, 0b0000000],
        'bottom': [0b0000000, 0b0000000, 0b0000001, 0b0000000, 0b0000000, 0b0000000]
    },
    'U': {
        # U: Straight sides, curved bottom
        'top': [0b1111110, 0b0000001, 0b0000001, 0b0000001, 0b0000000],
        'bottom': [0b0000001, 0b0000001, 0b0000001, 0b1111110, 0b0000000]
    },
    'V': {
        # V: Angled lines meeting at bottom
        'top': [0b1110000, 0b0001100, 0b0000011, 0b0001100, 0b1110000, 0b0000000],
        'bottom': [0b0000000, 0b0000000, 0b0000001, 0b0000000, 0b0000000, 0b0000000]
    },
    'W': {
        # W: Like upside down M
        'top': [0b1111110, 0b0000001, 0b0000110, 0b0000001, 0b1111110, 0b0000000],
        'bottom': [0b0000000, 0b0000000, 0b0111000, 0b0000000, 0b0000000, 0b0000000]
    },
    'X': {
        # X: Diagonal cross
        'top': [0b1100011, 0b0010100, 0b0001000, 0b0010100, 0b1100011, 0b0000000],
        'bottom': [0b1100011, 0b0010100, 0b0001000, 0b0010100, 0b1100011, 0b0000000]
    },
    'Y': {
        # Y: Lines meeting at center, then single line down
        'top': [0b1100000, 0b0010000, 0b0001111, 0b0010000, 0b1100000, 0b0000000],
        'bottom': [0b0000000, 0b0000000, 0b0000001, 0b0000000, 0b0000000, 0b0000000]
    },
    'Z': {
        # Z: Diagonal line
        'top': [0b1000011, 0b1000101, 0b1001001, 0b1010001, 0b1100001, 0b0000000],
        'bottom': [0b1000011, 0b1000101, 0b1001001, 0b1010001, 0b1100001, 0b0000000]
    },
    ' ': {
        'top': [0b0000000, 0b0000000, 0b0000000],
        'bottom': [0b0000000, 0b0000000, 0b0000000]
    }
}

def create_double_height_message(message):
    """Create double-height message bytes."""
    top_bytes = []
    bottom_bytes = []
    
    for char in message.upper():
        if char in REFINED_DOUBLE_HEIGHT:
            pattern = REFINED_DOUBLE_HEIGHT[char]
            top_bytes.extend(pattern['top'])
            bottom_bytes.extend(pattern['bottom'])
        else:
            # Use space for unknown characters
            pattern = REFINED_DOUBLE_HEIGHT[' ']
            top_bytes.extend(pattern['top'])
            bottom_bytes.extend(pattern['bottom'])
    
    return bytes(top_bytes), bytes(bottom_bytes)

def display_refined_double_height(message):
    """Display refined double-height text."""
    print(f"Displaying refined double-height: '{message}'")
    top_bytes, bottom_bytes = create_double_height_message(message)
    display_double_height_char(top_bytes, bottom_bytes)

def scroll_refined_double_height(message):
    """Scroll refined double-height text.""" 
    print(f"Scrolling refined double-height: '{message}'")
    top_bytes, bottom_bytes = create_double_height_message(message)
    
    # Create scrolling animation
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    total_length = len(padded_top) - 105
    
    for offset in range(0, total_length, 2):
        top_chunk = padded_top[offset:offset + 105]
        bottom_chunk = padded_bottom[offset:offset + 105]
        
        double_buffer = list(top_chunk)
        for i, byte in enumerate(bottom_chunk):
            if i + 30 < 105:
                double_buffer[i + 30] = byte
        
        working_core.fill(bytes(double_buffer))
        time.sleep(0.12)

def test_refined_characters():
    """Test the refined double-height characters."""
    print("🎯 Testing Refined Double-Height Characters")
    print("=" * 50)
    
    # Test individual characters that should look good
    test_chars = ['A', 'H', 'I', 'E', 'L', 'O']
    
    for char in test_chars:
        print(f"\nTesting refined '{char}':")
        
        # Show single height for comparison
        print("1. Single height:")
        working_core.display_text(char, justify='center')
        input("Press Enter to see refined double height...")
        clear()
        
        # Show refined double height
        print("2. Refined double height:")
        display_refined_double_height(char)
        input("Press Enter to continue...")
        clear()

def test_words():
    """Test double-height words."""
    print("🎯 Testing Double-Height Words")
    print("=" * 50)
    
    words = ['HI', 'HELLO', 'TEST', 'BIG']
    
    for word in words:
        print(f"\nTesting word: '{word}'")
        
        choice = input(f"Display static '{word}'? (y/n): ").strip().lower()
        if choice == 'y':
            display_refined_double_height(word)
            time.sleep(3)
            clear()
        
        choice = input(f"Scroll '{word}'? (y/n): ").strip().lower()
        if choice == 'y':
            scroll_refined_double_height(word)
            clear()

if __name__ == "__main__":
    print("🎨 Refined Double Height Characters")
    print("=" * 50)
    print("Using improved character patterns designed for your display.")
    
    choice = input("\nTest individual characters? (y/n): ").strip().lower()
    if choice == 'y':
        test_refined_characters()
    
    choice = input("\nTest words? (y/n): ").strip().lower()
    if choice == 'y':
        test_words()
    
    choice = input("\nQuick test - display 'BIG' in double height? (y/n): ").strip().lower()
    if choice == 'y':
        display_refined_double_height("BIG")
        time.sleep(4)
        clear()
    
    print("✅ Refined double height test complete!")
