#!/usr/bin/env python3
"""
Final Enhanced Core with Working Quadrant Mapping

Now using the proven quadrant buffer mapping that works on your display.
Supports single-height, double-height, and double-wide double-height text.
"""

import time

# Import your existing core functionality
try:
    from .core import *
    print("✅ Imported existing core functions (relative)")
except ImportError:
    try:
        import sys
        import os
        # Add parent directory to path
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        from core.core import working_core, clear, getbytes, scrollleft
        print("✅ Imported existing core functions")
    except ImportError:
        print("❌ Could not import core functions")

# Complete double-height bitmap patterns (14 pixels tall)
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
    'Q': [
        ' #### ',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '#    #',
        '# ## #',
        '#   ##',
        '#    #',
        ' #####',
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

def create_double_wide_pattern(normal_pattern):
    """Convert normal pattern to double-wide (each # becomes ##)."""
    double_wide = []
    for row in normal_pattern:
        wide_row = ''
        for char in row:
            wide_row += char + char  # Double each character
        double_wide.append(wide_row)
    return double_wide

def display_double_height_char(top_bytes, bottom_bytes):
    """
    Display double-height character using PROVEN quadrant buffer mapping.
    
    Your display mapping (CONFIRMED WORKING):
    - Bytes 0-15: Upper left quadrant
    - Bytes 15-30: Upper right quadrant  
    - Bytes 30-45: Lower left quadrant
    - Bytes 45-60: Lower right quadrant
    """
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

# Main text display functions using WORKING buffer mapping
def display_text_single_height(message, justify='center'):
    """Display single-height text (original 7-pixel tall)."""
    working_core.display_text(message, justify=justify)

def display_text_double_height(message, justify='center'):
    """Display double-height text (14 pixels tall) using WORKING quadrant mapping."""
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
    
    display_double_height_char(bytes(all_top_bytes), bytes(all_bottom_bytes))

def display_text_double_wide_double_height(message, justify='center'):
    """Display double-wide double-height text using WORKING quadrant mapping."""
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
    
    display_double_height_char(bytes(all_top_bytes), bytes(all_bottom_bytes))

def scroll_text_double_height(message, delay=0.12):
    """Scroll double-height text using WORKING quadrant mapping."""
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
        time.sleep(delay)

def typewriter_text_double_height(message, char_delay=0.4):
    """Typewriter effect for double-height text using WORKING quadrant mapping."""
    for i in range(1, len(message) + 1):
        partial = message[:i]
        display_text_double_height(partial, justify='left')
        time.sleep(char_delay)

# Export enhanced core functions
__all__ = [
    # Original functions
    'working_core', 'clear', 'getbytes', 'fill', 'scrollleft', 
    
    # New multi-size text functions (WORKING versions)
    'display_text_single_height',
    'display_text_double_height', 
    'display_text_double_wide_double_height',
    'scroll_text_double_height',
    'typewriter_text_double_height',
]

if __name__ == "__main__":
    print("🎨 Final Enhanced Core with WORKING Quadrant Mapping")
    print("=" * 60)
    
    # Test all three sizes with WORKING system
    tests = [
        ("Single Height", lambda: display_text_single_height("HELLO")),
        ("Double Height", lambda: display_text_double_height("HELLO")),
        ("Double Wide + Height", lambda: display_text_double_wide_double_height("HI")),
        ("Scroll Double Height", lambda: scroll_text_double_height("SCROLLING")),
        ("Typewriter Double Height", lambda: typewriter_text_double_height("TYPE")),
    ]
    
    for name, test_func in tests:
        choice = input(f"\nTest {name}? (y/n): ").strip().lower()
        if choice == 'y':
            print(f"Testing {name}...")
            test_func()
            input("Press Enter to continue...")
            clear()
    
    print("✅ Final enhanced core test complete!")
    print("All functions now use the PROVEN WORKING quadrant buffer mapping!")
