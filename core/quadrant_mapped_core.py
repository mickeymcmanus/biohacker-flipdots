#!/usr/bin/env python3
"""
Quadrant-Mapped Double Height Core

Fixed to work with your actual display buffer mapping:
- Bytes 0-15: Upper left quadrant
- Bytes 15-30: Upper right quadrant  
- Bytes 30-45: Lower left quadrant
- Bytes 45-60: Lower right quadrant
"""

# Import all your existing core functionality
try:
    from core.core import *
    print("✅ Imported existing core functions")
except ImportError:
    try:
        from .core import *
        print("✅ Imported existing core functions (relative)")
    except ImportError:
        print("❌ Could not import core.core - make sure it's in the core/ folder")

# Same double-height patterns as before
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

def display_double_height_char_QUADRANT(top_bytes, bottom_bytes):
    """
    Display double-height character using QUADRANT-based buffer mapping.
    
    Your display mapping:
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
    
    # Create 105-byte buffer
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
    """Convert normal pattern to double-wide (each # becomes ##)."""
    double_wide = []
    for row in normal_pattern:
        wide_row = ''
        for char in row:
            wide_row += char + char  # Double each character
        double_wide.append(wide_row)
    return double_wide

# Main text display functions with quadrant mapping
def display_text_single_height(message, justify='center'):
    """Display single-height text (original 7-pixel tall)."""
    working_core.display_text(message, justify=justify)

def display_text_double_height(message, justify='center'):
    """Display double-height text (14 pixels tall) using quadrant mapping."""
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
    
    display_double_height_char_QUADRANT(bytes(all_top_bytes), bytes(all_bottom_bytes))

def display_text_double_wide_double_height(message, justify='center'):
    """Display double-wide double-height text using quadrant mapping."""
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
    
    display_double_height_char_QUADRANT(bytes(all_top_bytes), bytes(all_bottom_bytes))

def test_quadrant_mapping():
    """Test the quadrant-based mapping."""
    print("🧪 Testing Quadrant-Based Buffer Mapping")
    print("=" * 50)
    
    # Test simple patterns first
    test_cases = [
        ("Simple 'I'", 'I'),
        ("Simple 'A'", 'A'), 
        ("Word 'HI'", 'HI'),
        ("Impact", 'IMPACT')
    ]
    
    for name, text in test_cases:
        choice = input(f"\nTest {name} ('{text}') with quadrant mapping? (y/n): ").strip().lower()
        if choice == 'y':
            print(f"Displaying '{text}' using quadrant mapping...")
            display_text_double_height(text)
            result = input("How does it look? (g)ood, (p)artial, (b)ad: ").strip().lower()
            clear()
            
            if result == 'g':
                print(f"✅ '{text}' looks good with quadrant mapping!")
            elif result == 'p':
                print(f"⚠️ '{text}' partially working")
            else:
                print(f"❌ '{text}' not working")

# Export functions
__all__ = [
    'working_core', 'clear', 'getbytes', 'fill', 'scrollleft',
    'display_text_single_height',
    'display_text_double_height', 
    'display_text_double_wide_double_height',
    'display_double_height_char_QUADRANT'
]

if __name__ == "__main__":
    print("🎨 Quadrant-Mapped Double Height Core")
    print("=" * 50)
    print("Fixed buffer mapping for your quadrant-based display")
    
    test_quadrant_mapping()
