#!/usr/bin/env python3
"""
Systematic Double Height Character Builder

Build proper double-height characters by analyzing your working single-height patterns
and creating proper 14-pixel tall versions.
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, getbytes, clear, dict as char_dict

def analyze_single_height_char(char):
    """Analyze how a single-height character is constructed."""
    if char in char_dict:
        char_bytes = char_dict[char]
        print(f"\nAnalyzing single-height '{char}':")
        print(f"Bytes: {char_bytes}")
        print(f"As list: {list(char_bytes)}")
        print("Bit patterns:")
        for i, byte in enumerate(char_bytes):
            print(f"  Column {i}: {byte:3d} = 0b{byte:07b} = {format_bits_visual(byte)}")
        return char_bytes
    return None

def format_bits_visual(byte_val):
    """Convert a byte to visual representation."""
    bits = format(byte_val, '07b')
    return ''.join('█' if bit == '1' else '·' for bit in bits)

def create_stretched_double_height(char):
    """
    Create double-height by stretching single-height characters vertically.
    Each bit becomes 2 bits tall.
    """
    if char not in char_dict:
        return None, None
    
    single_bytes = char_dict[char]
    top_bytes = []
    bottom_bytes = []
    
    for byte_val in single_bytes:
        # Extract the 7 bits
        bits = [(byte_val >> i) & 1 for i in range(7)]
        
        # Create stretched version - each bit becomes 2 bits tall
        # Top half gets bits 3-6 (upper part), bottom half gets bits 0-3 (lower part)
        top_val = 0
        bottom_val = 0
        
        # Method 1: Split the 7 bits between top and bottom
        # Top gets upper 4 bits, bottom gets lower 3 bits + stretched versions
        for i in range(7):
            if i >= 3:  # Upper bits go to top
                top_val |= (bits[i] << (i - 3))
                top_val |= (bits[i] << (i - 2)) if i - 2 >= 0 else 0
            else:  # Lower bits go to bottom  
                bottom_val |= (bits[i] << i)
                bottom_val |= (bits[i] << (i + 1)) if i + 1 < 7 else 0
        
        top_bytes.append(top_val & 0x7F)  # Keep 7 bits
        bottom_bytes.append(bottom_val & 0x7F)
    
    return bytes(top_bytes), bytes(bottom_bytes)

def create_proper_double_height(char):
    """
    Create proper double-height characters by designing them manually
    based on the single-height patterns.
    """
    
    # Manually designed double-height patterns based on your working single chars
    double_patterns = {
        'A': {
            'top': [0b0011110, 0b0100001, 0b0100001, 0b0111111, 0b0000000],  # Top peak + crossbar
            'bottom': [0b1000001, 0b1000001, 0b1000001, 0b1000001, 0b0000000]  # Legs continue down
        },
        'H': {
            'top': [0b1111111, 0b0001000, 0b0001000, 0b0001000, 0b0000000],    # Left line + start right
            'bottom': [0b1111111, 0b0001000, 0b0001000, 0b1111111, 0b0000000]  # Continue + crossbar + right
        },
        'I': {
            'top': [0b0100001, 0b0111111, 0b0100001, 0b0000000],     # Top bar
            'bottom': [0b0100001, 0b0111111, 0b0100001, 0b0000000]   # Bottom bar
        },
        'E': {
            'top': [0b1111111, 0b1001001, 0b1001001, 0b1000001, 0b0000000],    # Top + middle bars
            'bottom': [0b1000001, 0b1000001, 0b1000001, 0b1111111, 0b0000000]  # Continue + bottom bar
        },
        'L': {
            'top': [0b1111111, 0b0000001, 0b0000001, 0b0000001, 0b0000000],    # Vertical line only
            'bottom': [0b0000001, 0b0000001, 0b0000001, 0b1111111, 0b0000000]  # Continue + bottom bar
        },
        'O': {
            'top': [0b0111110, 0b1000001, 0b1000001, 0b1000001, 0b0000000],    # Top curve + sides
            'bottom': [0b1000001, 0b1000001, 0b1000001, 0b0111110, 0b0000000]  # Sides + bottom curve
        },
        'T': {
            'top': [0b1100000, 0b1100000, 0b1111111, 0b1100000, 0b1100000, 0b0000000],  # Top bar
            'bottom': [0b0000000, 0b0000000, 0b0000011, 0b0000000, 0b0000000, 0b0000000]  # Center stem
        },
        ' ': {
            'top': [0b0000000, 0b0000000, 0b0000000],
            'bottom': [0b0000000, 0b0000000, 0b0000000]
        }
    }
    
    if char.upper() in double_patterns:
        pattern = double_patterns[char.upper()]
        return bytes(pattern['top']), bytes(pattern['bottom'])
    
    return None, None

def display_double_height_comparison(char):
    """Display single vs double height comparison."""
    print(f"\n🔍 Comparing single vs double height for '{char}'")
    
    # Show single height first
    print("1. Single height:")
    working_core.display_text(char, justify='center')
    input("Press Enter to see stretched double height...")
    clear()
    
    # Show stretched version
    print("2. Stretched double height:")
    top_bytes, bottom_bytes = create_stretched_double_height(char)
    if top_bytes and bottom_bytes:
        display_double_height_char(top_bytes, bottom_bytes)
        input("Press Enter to see proper double height...")
        clear()
    
    # Show proper version
    print("3. Proper double height:")
    top_bytes, bottom_bytes = create_proper_double_height(char)
    if top_bytes and bottom_bytes:
        display_double_height_char(top_bytes, bottom_bytes)
        input("Press Enter to continue...")
        clear()

def display_double_height_char(top_bytes, bottom_bytes):
    """Display double-height character using proven method."""
    # Use your proven positioning method (position 103 + 30 offset)
    padded_top = b'\x00' * 105 + top_bytes + b'\x00' * 105  
    padded_bottom = b'\x00' * 105 + bottom_bytes + b'\x00' * 105
    
    top_chunk = padded_top[103:103 + 105]
    bottom_chunk = padded_bottom[103:103 + 105] 
    
    double_buffer = list(top_chunk)
    for i, byte in enumerate(bottom_chunk):
        if i + 30 < 105:
            double_buffer[i + 30] = byte
    
    working_core.fill(bytes(double_buffer))

def create_simple_double_height(char):
    """
    Create simple double-height by taking single-height pattern 
    and splitting it logically between top and bottom.
    """
    if char not in char_dict:
        return None, None
    
    single_bytes = char_dict[char]
    
    # Simple approach: duplicate the pattern but make top and bottom complementary
    top_bytes = []
    bottom_bytes = []
    
    for byte_val in single_bytes:
        # Top half: keep upper 4 bits, clear lower 3 bits
        top_val = (byte_val & 0b1111000)  # Keep bits 6,5,4,3
        # Shift down to use full 7-bit range
        top_val = top_val >> 1
        
        # Bottom half: keep lower 4 bits, extend upward  
        bottom_val = (byte_val & 0b0001111) << 3  # Move bits 3,2,1,0 up
        bottom_val |= (byte_val & 0b0001111)      # Also keep them at bottom
        
        top_bytes.append(top_val & 0x7F)
        bottom_bytes.append(bottom_val & 0x7F)
    
    return bytes(top_bytes), bytes(bottom_bytes)

def test_all_approaches():
    """Test all different approaches to double-height."""
    test_chars = ['A', 'H', 'I', 'E']
    
    for char in test_chars:
        print(f"\n{'='*50}")
        print(f"TESTING CHARACTER: '{char}'")
        print('='*50)
        
        # Analyze the original
        analyze_single_height_char(char)
        
        # Test different approaches
        approaches = [
            ("Stretched", create_stretched_double_height),
            ("Simple", create_simple_double_height), 
            ("Proper", create_proper_double_height)
        ]
        
        for name, func in approaches:
            print(f"\n--- {name} Double Height ---")
            top_bytes, bottom_bytes = func(char)
            
            if top_bytes and bottom_bytes:
                print(f"Top bytes: {list(top_bytes)}")
                print(f"Bottom bytes: {list(bottom_bytes)}")
                
                choice = input(f"Display {name.lower()} double-height '{char}'? (y/n): ").strip().lower()
                if choice == 'y':
                    display_double_height_char(top_bytes, bottom_bytes)
                    input("Press Enter to continue...")
                    clear()

if __name__ == "__main__":
    print("🔧 Systematic Double Height Character Builder")
    print("=" * 60)
    print("We know the buffer mapping works (+30 offset, position 103)")
    print("Now let's build proper character patterns.")
    
    choice = input("\nAnalyze and test all approaches? (y/n): ").strip().lower()
    if choice == 'y':
        test_all_approaches()
    else:
        # Quick test of just the 'A' that worked
        print("\nQuick test of improved 'A':")
        top_bytes, bottom_bytes = create_proper_double_height('A')
        if top_bytes and bottom_bytes:
            display_double_height_char(top_bytes, bottom_bytes)
            time.sleep(3)
            clear()
    
    print("✅ Character building test complete!")
