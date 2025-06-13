#!/usr/bin/env python3
"""
Debug version of double height text to diagnose display issues
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, getbytes, clear

def debug_display_buffer(buffer, title="Display Buffer"):
    """Print the display buffer in a readable format."""
    print(f"\n{title}:")
    print("=" * 50)
    print(f"Buffer length: {len(buffer)} bytes")
    
    # Show first 30 bytes (top row)
    print("Top row (bytes 0-29):")
    top_row = buffer[:30] if len(buffer) >= 30 else buffer
    for i, byte in enumerate(top_row):
        print(f"{i:2d}: {byte:3d} (0b{byte:07b})")
    
    # Show bytes 30-59 (bottom row) 
    if len(buffer) >= 60:
        print("\nBottom row (bytes 30-59):")
        bottom_row = buffer[30:60]
        for i, byte in enumerate(bottom_row):
            print(f"{i+30:2d}: {byte:3d} (0b{byte:07b})")
    
    # Show remaining bytes if any
    if len(buffer) > 60:
        print(f"\nRemaining bytes (60-{len(buffer)-1}):")
        remaining = buffer[60:]
        for i, byte in enumerate(remaining):
            print(f"{i+60:2d}: {byte:3d} (0b{byte:07b})")

def debug_character_generation():
    """Debug the character generation process."""
    print("🔍 Debug: Character Generation")
    print("=" * 50)
    
    # Test simple character
    test_char = 'A'
    print(f"Testing character: '{test_char}'")
    
    # Check if character exists in dictionary
    from core.double_height_text import double_height_dict
    
    if test_char in double_height_dict:
        char_data = double_height_dict[test_char]
        print(f"Character data found: {len(char_data)} bytes")
        print(f"Raw data: {char_data}")
        
        # Split into top and bottom
        char_width = len(char_data) // 2
        top_part = char_data[:char_width]
        bottom_part = char_data[char_width:]
        
        print(f"\nTop part ({len(top_part)} bytes): {top_part}")
        print(f"Bottom part ({len(bottom_part)} bytes): {bottom_part}")
        
        # Show binary representation
        print(f"\nTop part binary:")
        for i, byte in enumerate(top_part):
            print(f"  {i}: {byte:3d} = 0b{byte:07b}")
            
        print(f"\nBottom part binary:")
        for i, byte in enumerate(bottom_part):
            print(f"  {i}: {byte:3d} = 0b{byte:07b}")
    else:
        print(f"❌ Character '{test_char}' not found in dictionary!")
        print(f"Available characters: {list(double_height_dict.keys())}")

def debug_bytes_generation(message):
    """Debug the byte generation for a message."""
    print(f"\n🔍 Debug: Bytes Generation for '{message}'")
    print("=" * 50)
    
    from core.double_height_text import get_double_height_bytes
    
    try:
        top_bytes, bottom_bytes = get_double_height_bytes(message)
        
        print(f"Message: '{message}'")
        print(f"Top bytes length: {len(top_bytes)}")
        print(f"Bottom bytes length: {len(bottom_bytes)}")
        
        print(f"\nTop bytes: {list(top_bytes)}")
        print(f"Bottom bytes: {list(bottom_bytes)}")
        
        # Show binary
        print(f"\nTop bytes binary:")
        for i, byte in enumerate(top_bytes):
            print(f"  {i:2d}: {byte:3d} = 0b{byte:07b}")
            
        print(f"\nBottom bytes binary:")
        for i, byte in enumerate(bottom_bytes):
            print(f"  {i:2d}: {byte:3d} = 0b{byte:07b}")
            
        return top_bytes, bottom_bytes
        
    except Exception as e:
        print(f"❌ Error generating bytes: {e}")
        return None, None

def debug_display_process(message):
    """Debug the entire display process."""
    print(f"\n🔍 Debug: Display Process for '{message}'")
    print("=" * 50)
    
    from core.double_height_text import get_double_height_bytes
    
    # Step 1: Generate bytes
    top_bytes, bottom_bytes = debug_bytes_generation(message)
    if not top_bytes or not bottom_bytes:
        return
    
    # Step 2: Create display buffer
    text_width = len(top_bytes)
    padding = max(0, (30 - text_width) // 2)  # Center
    
    print(f"\nDisplay positioning:")
    print(f"Text width: {text_width}")
    print(f"Padding: {padding}")
    
    # Create padded display bytes
    display_top = bytes([0] * padding) + top_bytes + bytes([0] * (30 - padding - len(top_bytes)))
    display_bottom = bytes([0] * padding) + bottom_bytes + bytes([0] * (30 - padding - len(bottom_bytes)))
    
    print(f"Display top length: {len(display_top)}")
    print(f"Display bottom length: {len(display_bottom)}")
    
    # Combine for full display
    full_display = display_top + display_bottom
    
    # Pad to 105 bytes if needed
    if len(full_display) < 105:
        full_display += bytes([0] * (105 - len(full_display)))
    elif len(full_display) > 105:
        full_display = full_display[:105]
    
    print(f"Full display buffer length: {len(full_display)}")
    
    # Show the buffer
    debug_display_buffer(full_display, f"Final Display Buffer for '{message}'")
    
    return full_display

def test_regular_vs_double():
    """Compare regular single-height vs double-height display."""
    print("\n🔍 Debug: Regular vs Double Height Comparison")
    print("=" * 50)
    
    test_msg = "HI"
    
    # Test regular single-height
    print("1. Regular single-height display:")
    regular_bytes = getbytes(test_msg)
    print(f"Regular bytes: {list(regular_bytes)}")
    debug_display_buffer(regular_bytes, "Regular Display")
    
    print("\n" + "="*30)
    input("Press Enter to display regular text...")
    working_core.display_text(test_msg, justify='center')
    time.sleep(3)
    
    # Test double-height
    print("\n2. Double-height display:")
    double_buffer = debug_display_process(test_msg)
    
    print("\n" + "="*30)
    input("Press Enter to display double-height text...")
    if double_buffer:
        working_core.fill(double_buffer)
        time.sleep(3)
    
    clear()

def simple_double_height_test():
    """Very simple test of double height functionality."""
    print("\n🔍 Simple Double Height Test")
    print("=" * 50)
    
    # Create a simple test pattern manually
    # Let's make a simple 'I' character that spans both rows
    
    print("Creating manual double-height 'I'...")
    
    # Top row: center column with full height
    top_row = [0] * 30
    top_row[14] = 0b1111111  # Center column, all 7 bits set
    top_row[15] = 0b1111111  # Make it 2 columns wide
    
    # Bottom row: same pattern
    bottom_row = [0] * 30  
    bottom_row[14] = 0b1111111
    bottom_row[15] = 0b1111111
    
    # Create full 105-byte buffer
    manual_buffer = bytes(top_row + bottom_row + [0] * 45)  # Pad to 105
    
    debug_display_buffer(manual_buffer, "Manual Double Height 'I'")
    
    print("\n" + "="*30)
    input("Press Enter to display manual double-height pattern...")
    working_core.fill(manual_buffer)
    time.sleep(3)
    
    clear()

if __name__ == "__main__":
    print("🔧 Double Height Debug Tool")
    print("=" * 50)
    
    # Run debug tests
    debug_character_generation()
    
    choice = input("\nRun comparison test? (y/n): ").strip().lower()
    if choice == 'y':
        test_regular_vs_double()
    
    choice = input("\nRun simple manual test? (y/n): ").strip().lower()
    if choice == 'y':
        simple_double_height_test()
    
    print("\nDebug session complete.")
