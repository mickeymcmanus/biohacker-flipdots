#!/usr/bin/env python3
"""
True Double Height Characters

Create actual 14-pixel tall characters by designing new character patterns
that are twice as tall as the original 7-pixel patterns.
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, getbytes, clear

# True double-height character patterns
# Each character is defined as [top_7_pixels, bottom_7_pixels]
# Using the same bit patterns as your existing single-height characters but stretched vertically

TRUE_DOUBLE_HEIGHT_CHARS = {
    'A': {
        'top':    [0b0111111, 0b1000000, 0b1000000, 0b0111111, 0b0000000],  # Top half of A - wider
        'bottom': [0b1111111, 0b0001000, 0b0001000, 0b1111111, 0b0000000]   # Bottom half of A - base
    },
    'H': {
        'top':    [0b1111111, 0b0001000, 0b0001000, 0b0000000],  # Top half - vertical lines  
        'bottom': [0b1111111, 0b0001000, 0b0001000, 0b1111111, 0b0000000]   # Bottom half - connected
    },
    'I': {
        'top':    [0b1111111, 0b0000000],  # Top half - full width bar
        'bottom': [0b1111111, 0b0000000]   # Bottom half - full width bar  
    },
    'E': {
        'top':    [0b1111111, 0b1000000, 0b1110000, 0b0000000],  # Top + middle bar
        'bottom': [0b1000000, 0b1000000, 0b1111111, 0b0000000]   # Bottom bar
    },
    'L': {
        'top':    [0b1111111, 0b0000001, 0b0000000],  # Vertical line
        'bottom': [0b0000001, 0b0000001, 0b1111111, 0b0000000]   # Bottom bar
    },
    'O': {
        'top':    [0b0111110, 0b1000001, 0b1000001, 0b0000000],  # Top curve
        'bottom': [0b1000001, 0b1000001, 0b0111110, 0b0000000]   # Bottom curve
    },
    'T': {
        'top':    [0b1111111, 0b0010000, 0b0010000, 0b0000000],  # Top bar + stem start
        'bottom': [0b0010000, 0b0010000, 0b0010000, 0b0000000]   # Stem continues
    },
    ' ': {
        'top':    [0b0000000, 0b0000000, 0b0000000],
        'bottom': [0b0000000, 0b0000000, 0b0000000]
    }
}

def create_true_double_height_bytes(message):
    """
    Create byte arrays for true double-height text.
    Returns (top_bytes, bottom_bytes) where each is 7 pixels tall.
    """
    top_bytes = []
    bottom_bytes = []
    
    for char in message.upper():
        if char in TRUE_DOUBLE_HEIGHT_CHARS:
            char_def = TRUE_DOUBLE_HEIGHT_CHARS[char]
            
            # Add the character's top and bottom parts
            top_bytes.extend(char_def['top'])
            bottom_bytes.extend(char_def['bottom'])
            
            # Add spacing between characters
            top_bytes.append(0)
            bottom_bytes.append(0)
        else:
            # Unknown character - use space
            top_bytes.extend([0, 0, 0, 0])
            bottom_bytes.extend([0, 0, 0, 0])
    
    return bytes(top_bytes), bytes(bottom_bytes)

def display_true_double_height(message):
    """
    Display true double-height text using the proven +30 offset method.
    """
    print(f"Displaying true double-height: '{message}'")
    
    # Create the true double-height character bytes
    top_bytes, bottom_bytes = create_true_double_height_bytes(message)
    
    print(f"Top bytes: {len(top_bytes)} bytes")
    print(f"Bottom bytes: {len(bottom_bytes)} bytes")
    
    # Use your proven positioning method (position 103)
    # Create padded message like your working scrollleft does
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    # Extract the chunk at your proven position 103
    top_chunk = padded_top[103:103 + 105]
    bottom_chunk = padded_bottom[103:103 + 105]
    
    # Create the double-height buffer
    double_buffer = list(top_chunk)  # Start with top half
    
    # Add bottom half at +30 offset (which we discovered works)
    for i, byte in enumerate(bottom_chunk):
        if i + 30 < 105:
            double_buffer[i + 30] = byte
    
    # Display it
    working_core.fill(bytes(double_buffer))

def test_individual_chars():
    """Test individual double-height characters."""
    print("🔤 Testing Individual True Double-Height Characters")
    print("=" * 50)
    
    test_chars = ['I', 'H', 'A', 'E', 'L', 'O', 'T']
    
    for char in test_chars:
        print(f"\nTesting character: '{char}'")
        
        # Show the character definition
        if char in TRUE_DOUBLE_HEIGHT_CHARS:
            char_def = TRUE_DOUBLE_HEIGHT_CHARS[char]
            print(f"Top pattern: {[bin(b) for b in char_def['top']]}")
            print(f"Bottom pattern: {[bin(b) for b in char_def['bottom']]}")
        
        # Show single-height version first
        print("1. Normal single-height:")
        working_core.display_text(char, justify='center')
        input("Press Enter to see double-height...")
        clear()
        
        # Show true double-height version
        print("2. True double-height:")
        display_true_double_height(char)
        input("Press Enter to continue...")
        clear()

def create_better_double_height_patterns():
    """
    Create improved double-height patterns by analyzing your existing single-height characters.
    """
    print("🎨 Creating Better Double-Height Patterns")
    print("=" * 50)
    
    # Let's analyze your existing 'H' character
    h_bytes = getbytes('H')
    print(f"Your single-height 'H': {[bin(b) for b in h_bytes]}")
    
    # Create a proper double-height 'H' by stretching it vertically
    # Top half: upper part of the H
    h_top = [
        0b1000001,  # |     |
        0b1000001,  # |     |  
        0b1000001,  # |     |
        0b1111111,  # |-----|  (crossbar)
        0b0000000   # spacing
    ]
    
    # Bottom half: lower part of the H  
    h_bottom = [
        0b1111111,  # |-----| (crossbar continues)
        0b1000001,  # |     |
        0b1000001,  # |     |
        0b1000001,  # |     |
        0b0000000   # spacing
    ]
    
    print(f"Double-height 'H' top: {[bin(b) for b in h_top]}")
    print(f"Double-height 'H' bottom: {[bin(b) for b in h_bottom]}")
    
    # Test this improved pattern
    input("Press Enter to test improved double-height 'H'...")
    
    # Create buffer using proven method
    top_bytes = bytes(h_top)
    bottom_bytes = bytes(h_bottom)
    
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    top_chunk = padded_top[103:103 + 105]
    bottom_chunk = padded_bottom[103:103 + 105]
    
    double_buffer = list(top_chunk)
    for i, byte in enumerate(bottom_chunk):
        if i + 30 < 105:
            double_buffer[i + 30] = byte
    
    working_core.fill(bytes(double_buffer))
    input("Press Enter to continue...")
    clear()

def scroll_true_double_height(message):
    """Scroll true double-height text."""
    print(f"Scrolling true double-height: '{message}'")
    
    top_bytes, bottom_bytes = create_true_double_height_bytes(message)
    
    # Create scrolling animation using your proven method
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    total_length = len(padded_top) - 105
    
    for offset in range(0, total_length, 2):  # Scroll by 2 pixels
        top_chunk = padded_top[offset:offset + 105]
        bottom_chunk = padded_bottom[offset:offset + 105]
        
        # Create double-height buffer
        double_buffer = list(top_chunk)
        for i, byte in enumerate(bottom_chunk):
            if i + 30 < 105:
                double_buffer[i + 30] = byte
        
        working_core.fill(bytes(double_buffer))
        time.sleep(0.15)

if __name__ == "__main__":
    print("🎯 True Double Height Character Test")
    print("=" * 50)
    print("This creates actual 14-pixel tall characters instead of duplicating 7-pixel ones.")
    
    choice = input("\nTest individual characters? (y/n): ").strip().lower()
    if choice == 'y':
        test_individual_chars()
    
    choice = input("\nCreate better patterns? (y/n): ").strip().lower()
    if choice == 'y':
        create_better_double_height_patterns()
    
    choice = input("\nTest scrolling double-height text? (y/n): ").strip().lower()
    if choice == 'y':
        scroll_true_double_height("HELLO")
    
    choice = input("\nTest word 'HI' in true double-height? (y/n): ").strip().lower()
    if choice == 'y':
        display_true_double_height("HI")
        time.sleep(3)
        clear()
    
    print("✅ True double-height test complete!")
