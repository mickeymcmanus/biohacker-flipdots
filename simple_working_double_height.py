#!/usr/bin/env python3
"""
Simple Working Double Height System

Place this file in your main project directory (same level as core/ folder).
This is a complete, working double-height text system that's easy to integrate.
"""

import sys
import os
import time
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing core
try:
    from core.core import working_core, clear, getbytes, scrollleft
    print("✅ Successfully imported working_core")
except ImportError as e:
    print(f"❌ Could not import core: {e}")
    print("Make sure this file is in the same directory as your core/ folder")
    sys.exit(1)

# Double-height patterns (proven to work)
DOUBLE_HEIGHT_PATTERNS = {
    'A': [
        '  ##  ',  # 0
        ' #  # ',  # 1  
        '#    #',  # 2
        '#    #',  # 3
        '#    #',  # 4
        '######',  # 5
        '#    #',  # 6
        '#    #',  # 7
        '#    #',  # 8
        '#    #',  # 9
        '#    #',  # 10
        '#    #',  # 11
        '      ',  # 12
        '      '   # 13
    ],
    'B': [
        '##### ',
        '#    #',
        '#    #',
        '#    #',
        '##### ',
        '##### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '##### ',
        '      ',
        '      '
    ],
    'C': [
        ' #### ',
        '#    #',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    'D': [
        '##### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '##### ',
        '      ',
        '      '
    ],
    'E': [
        '######',
        '#     ',
        '#     ',
        '#     ',
        '##### ',
        '##### ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '######',
        '      ',
        '      '
    ],
    'F': [
        '######',
        '#     ',
        '#     ',
        '#     ',
        '##### ',
        '##### ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '      ',
        '      '
    ],
    'G': [
        ' #### ',
        '#    #',
        '#     ',
        '#     ',
        '#     ',
        '# ####',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    'H': [
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '######',
        '######',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'I': [
        '######',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '######',
        '      ',
        '      '
    ],
    'J': [
        '######',
        '    ##',
        '    ##',
        '    ##',
        '    ##',
        '    ##',
        '    ##',
        '    ##',
        '    ##',
        '#   ##',
        '#   ##',
        ' #### ',
        '      ',
        '      '
    ],
    'K': [
        '#    #',
        '#   # ',
        '#  #  ',
        '# #   ',
        '##    ',
        '##    ',
        '# #   ',
        '#  #  ',
        '#   # ',
        '#    #',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'L': [
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '######',
        '      ',
        '      '
    ],
    'M': [
        '#    #',
        '##  ##',
        '# ## #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'N': [
        '#    #',
        '##   #',
        '# #  #',
        '#  # #',
        '#   ##',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'O': [
        ' #### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    'P': [
        '##### ',
        '#    #',
        '#    #',
        '#    #',
        '##### ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '      ',
        '      '
    ],
    'R': [
        '##### ',
        '#    #',
        '#    #',
        '#    #',
        '##### ',
        '# #   ',
        '#  #  ',
        '#   # ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'S': [
        ' #### ',
        '#    #',
        '#     ',
        ' #    ',
        '  ##  ',
        '   ## ',
        '    # ',
        '     #',
        '     #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    'T': [
        '######',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      '
    ],
    'U': [
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    'V': [
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #  # ',
        ' #  # ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      '
    ],
    'W': [
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '# ## #',
        '# ## #',
        '##  ##',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'X': [
        '#    #',
        ' #  # ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        ' #  # ',
        '#    #',
        '#    #',
        '      ',
        '      '
    ],
    'Y': [
        '#    #',
        ' #  # ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      '
    ],
    'Z': [
        '######',
        '    # ',
        '   #  ',
        '  #   ',
        ' #    ',
        '#     ',
        '#     ',
        ' #    ',
        '  #   ',
        '   #  ',
        '    # ',
        '######',
        '      ',
        '      '
    ],
    '0': [
        ' #### ',
        '#    #',
        '#   ##',
        '#  # #',
        '# #  #',
        '##   #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    '1': [
        '  ##  ',
        ' ###  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '######',
        '      ',
        '      '
    ],
    '2': [
        ' #### ',
        '#    #',
        '     #',
        '    ##',
        '   ## ',
        '  ##  ',
        ' ##   ',
        '##    ',
        '#     ',
        '#     ',
        '#     ',
        '######',
        '      ',
        '      '
    ],
    '3': [
        ' #### ',
        '#    #',
        '     #',
        '     #',
        ' #### ',
        ' #### ',
        '     #',
        '     #',
        '     #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    '4': [
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '######',
        '     #',
        '     #',
        '     #',
        '     #',
        '     #',
        '     #',
        '     #',
        '      ',
        '      '
    ],
    '5': [
        '######',
        '#     ',
        '#     ',
        '#     ',
        '##### ',
        '     #',
        '     #',
        '     #',
        '     #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    '6': [
        ' #### ',
        '#    #',
        '#     ',
        '#     ',
        '##### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    '7': [
        '######',
        '     #',
        '    # ',
        '   #  ',
        '  #   ',
        ' #    ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '#     ',
        '      ',
        '      '
    ],
    '8': [
        ' #### ',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        ' #### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    '9': [
        ' #### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        ' #####',
        '     #',
        '     #',
        '     #',
        '#    #',
        '#    #',
        ' #### ',
        '      ',
        '      '
    ],
    ' ': [
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      ',
        '      '
    ],
    '!': [
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      '
    ],
    '?': [
        ' #### ',
        '#    #',
        '     #',
        '    ##',
        '   ## ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      ',
        '  ##  ',
        '  ##  ',
        '  ##  ',
        '      ',
        '      '
    ]
}

def create_bitmap_from_pattern(pattern):
    """Convert a visual pattern into bytes for double-height display."""
    if len(pattern) != 14:
        raise ValueError("Pattern must be exactly 14 rows")
    
    width = len(pattern[0]) if pattern else 0
    top_bytes = []
    bottom_bytes = []
    
    for col in range(width):
        top_byte = 0
        bottom_byte = 0
        
        # Top 7 rows (0-6)
        for row in range(7):
            if row < len(pattern) and col < len(pattern[row]):
                if pattern[row][col] == '#':
                    top_byte |= (1 << (6 - row))
        
        # Bottom 7 rows (7-13)
        for row in range(7, 14):
            if row < len(pattern) and col < len(pattern[row]):
                if pattern[row][col] == '#':
                    bottom_byte |= (1 << (13 - row))
        
        top_bytes.append(top_byte)
        bottom_bytes.append(bottom_byte)
    
    return bytes(top_bytes), bytes(bottom_bytes)

def display_double_height_WORKING(top_bytes, bottom_bytes):
    """Display double-height using the PROVEN WORKING quadrant mapping."""
    # Use your proven position 103 for horizontal positioning
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105  
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    top_chunk = padded_top[103:103 + 105]
    bottom_chunk = padded_bottom[103:103 + 105] 
    
    # Create 105-byte buffer using WORKING quadrant mapping
    quadrant_buffer = [0] * 105
    
    # Map top row to upper quadrants (0-15 and 15-30)
    for i in range(min(30, len(top_chunk))):
        if i < 15:
            # Upper left quadrant (bytes 0-14)
            quadrant_buffer[i] = top_chunk[i]
        else:
            # Upper right quadrant (bytes 15-29) 
            quadrant_buffer[i] = top_chunk[i]
    
    # Map bottom row to lower quadrants (30-45 and 45-60)
    for i in range(min(30, len(bottom_chunk))):
        if i < 15:
            # Lower left quadrant (bytes 30-44)
            quadrant_buffer[30 + i] = bottom_chunk[i]
        else:
            # Lower right quadrant (bytes 45-59)
            quadrant_buffer[30 + i] = bottom_chunk[i]
    
    working_core.fill(bytes(quadrant_buffer))

def create_double_wide_pattern(normal_pattern):
    """Convert normal pattern to double-wide."""
    double_wide = []
    for row in normal_pattern:
        wide_row = ''
        for char in row:
            wide_row += char + char  # Double each character
        double_wide.append(wide_row)
    return double_wide

# ============================================================================
# MAIN FUNCTIONS - Simple to use
# ============================================================================

def single_text(message):
    """Display single-height text (7 pixels tall)."""
    working_core.display_text(message, justify='center')

def double_text(message):
    """Display double-height text (14 pixels tall)."""
    all_top_bytes = []
    all_bottom_bytes = []
    
    for char in message.upper()[:5]:  # Limit to fit display
        if char in DOUBLE_HEIGHT_PATTERNS:
            pattern = DOUBLE_HEIGHT_PATTERNS[char]
            top_bytes, bottom_bytes = create_bitmap_from_pattern(pattern)
            all_top_bytes.extend(top_bytes)
            all_bottom_bytes.extend(bottom_bytes)
            # Add spacing between characters
            all_top_bytes.append(0)
            all_bottom_bytes.append(0)
    
    display_double_height_WORKING(bytes(all_top_bytes), bytes(all_bottom_bytes))

def wide_text(message):
    """Display double-wide double-height text (14 pixels tall, 2x wider)."""
    all_top_bytes = []
    all_bottom_bytes = []
    
    for char in message.upper()[:3]:  # Fewer chars due to width
        if char in DOUBLE_HEIGHT_PATTERNS:
            # Create double-wide pattern
            normal_pattern = DOUBLE_HEIGHT_PATTERNS[char]
            wide_pattern = create_double_wide_pattern(normal_pattern)
            
            top_bytes, bottom_bytes = create_bitmap_from_pattern(wide_pattern)
            all_top_bytes.extend(top_bytes)
            all_bottom_bytes.extend(bottom_bytes)
            # Add spacing between characters
            all_top_bytes.append(0)
            all_bottom_bytes.append(0)
    
    display_double_height_WORKING(bytes(all_top_bytes), bytes(all_bottom_bytes))

def scroll_double_text(message):
    """Scroll double-height text."""
    all_top_bytes = []
    all_bottom_bytes = []
    
    for char in message.upper():
        if char in DOUBLE_HEIGHT_PATTERNS:
            pattern = DOUBLE_HEIGHT_PATTERNS[char]
            top_bytes, bottom_bytes = create_bitmap_from_pattern(pattern)
            all_top_bytes.extend(top_bytes)
            all_bottom_bytes.extend(bottom_bytes)
            # Add spacing
            all_top_bytes.append(0)
            all_bottom_bytes.append(0)
    
    # Create scrolling animation
    padded_top = b'\x00' * 105 + bytes(all_top_bytes) + b'\x00' * 105
    padded_bottom = b'\x00' * 105 + bytes(all_bottom_bytes) + b'\x00' * 105
    
    total_length = len(padded_top) - 105
    
    for offset in range(0, total_length, 2):
        top_chunk = padded_top[offset:offset + 105]
        bottom_chunk = padded_bottom[offset:offset + 105]
        
        # Use WORKING quadrant mapping for scrolling
        quadrant_buffer = [0] * 105
        
        # Map to quadrants
        for i in range(min(30, len(top_chunk))):
            if i < 15:
                quadrant_buffer[i] = top_chunk[i]
            else:
                quadrant_buffer[i] = top_chunk[i]
        
        for i in range(min(30, len(bottom_chunk))):
            if i < 15:
                quadrant_buffer[30 + i] = bottom_chunk[i]
            else:
                quadrant_buffer[30 + i] = bottom_chunk[i]
        
        working_core.fill(bytes(quadrant_buffer))
        time.sleep(0.12)

# ============================================================================
# TRANSITION FUNCTIONS
# ============================================================================

def double_flash(message):
    """Flash double-height text."""
    for _ in range(5):
        double_text(message)
        time.sleep(0.3)
        clear()
        time.sleep(0.3)

def wide_dramatic(message):
    """Dramatic double-wide text."""
    for i in range(3):
        wide_text(message)
        time.sleep(0.2)
        clear()
        time.sleep(0.1)
    wide_text(message)
    time.sleep(3)

def impact_text(message):
    """Maximum impact based on message length."""
    if len(message) <= 3:
        wide_dramatic(message)
    elif len(message) <= 6:
        double_flash(message)
    else:
        single_text(message)
        time.sleep(3)

def smart_text(message):
    """Smart text sizing."""
    if len(message) <= 3:
        wide_text(message)
    elif len(message) <= 6:
        double_text(message)
    else:
        single_text(message)
    time.sleep(3)

# ============================================================================
# SIMPLE PLAYLIST EXAMPLE
# ============================================================================

def demo_playlist():
    """Simple demo playlist."""
    demos = [
        ("Single Height", lambda: single_text("HELLO WORLD")),
        ("Double Height", lambda: double_text("HELLO")),
        ("Wide Text", lambda: wide_text("BIG")),
        ("Double Flash", lambda: double_flash("FLASH")),
        ("Wide Dramatic", lambda: wide_dramatic("WOW")),
        ("Scroll Double", lambda: scroll_double_text("SCROLLING TEXT")),
        ("Impact Text", lambda: impact_text("GO")),
        ("Smart Text Short", lambda: smart_text("HI")),
        ("Smart Text Long", lambda: smart_text("LONGER MESSAGE")),
    ]
    
    for name, demo_func in demos:
        print(f"\n🎯 {name}")
        demo_func()
        time.sleep(1)
        clear()
        time.sleep(0.5)

if __name__ == "__main__":
    print("🎨 Simple Working Double Height System")
    print("=" * 50)
    print("Easy-to-use double-height text for your flipdot display!")
    
    # Quick test menu
    print("\nAvailable functions:")
    print("- single_text('message')     # 7 pixels tall")
    print("- double_text('message')     # 14 pixels tall")  
    print("- wide_text('message')       # 14 pixels tall, 2x wider")
    print("- scroll_double_text('msg')  # Scrolling double-height")
    print("- double_flash('message')    # Flashing double-height")
    print("- wide_dramatic('message')   # Dramatic wide text")
    print("- impact_text('message')     # Auto-sizing for impact")
    print("- smart_text('message')      # Smart size selection")
    
    choice = input("\nRun quick test? (y/n): ").strip().lower()
    if choice == 'y':
        print("\n1. Single height:")
        single_text("HELLO")
        time.sleep(2)
        clear()
        
        print("\n2. Double height:")
        double_text("BIG")
        time.sleep(2)
        clear()
        
        print("\n3. Wide text:")
        wide_text("WOW")
        time.sleep(2)
        clear()
        
        print("\n4. Impact text:")
        impact_text("GO")
        time.sleep(1)
        clear()
    
    choice = input("\nRun full demo playlist? (y/n): ").strip().lower()
    if choice == 'y':
        demo_playlist()
    
    print("\n✅ Simple working double height system ready!")
    print("🎉 You can now use single_text(), double_text(), and wide_text() in your playlists!")
