#!/usr/bin/env python3
"""
Visual test to see what's actually being displayed
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, getbytes, clear

def test_display_mapping():
    """Test how the display buffer maps to actual display."""
    print("🔍 Testing Display Buffer Mapping")
    print("=" * 50)
    
    # Test 1: Light up just the first column of top row
    print("Test 1: First column, top row only")
    buffer1 = [0] * 105
    buffer1[0] = 0b1111111  # All 7 bits in first column
    
    input("Press Enter to display...")
    working_core.fill(bytes(buffer1))
    time.sleep(3)
    clear()
    
    # Test 2: Light up just the first column of bottom row  
    print("Test 2: First column, bottom row only")
    buffer2 = [0] * 105
    buffer2[30] = 0b1111111  # First column of second row
    
    input("Press Enter to display...")
    working_core.fill(bytes(buffer2))
    time.sleep(3)
    clear()
    
    # Test 3: Light up both - should create a tall column
    print("Test 3: First column, both rows (double height)")
    buffer3 = [0] * 105
    buffer3[0] = 0b1111111   # Top row
    buffer3[30] = 0b1111111  # Bottom row - same column
    
    input("Press Enter to display...")
    working_core.fill(bytes(buffer3))
    time.sleep(3)
    clear()
    
    # Test 4: Create a simple double-height pattern
    print("Test 4: Simple double-height rectangle")
    buffer4 = [0] * 105
    
    # Fill columns 10-15 in both rows
    for col in range(10, 16):
        buffer4[col] = 0b1111111      # Top row
        buffer4[col + 30] = 0b1111111 # Bottom row
    
    input("Press Enter to display...")
    working_core.fill(bytes(buffer4))
    time.sleep(3)
    clear()

def test_character_comparison():
    """Compare single vs double height side by side."""
    print("🔍 Character Comparison Test")
    print("=" * 50)
    
    # Show regular 'A' first
    print("Regular single-height 'A':")
    working_core.display_text("A", justify='center')
    input("Press Enter to continue...")
    clear()
    
    # Now show what our double-height 'A' produces
    print("Double-height 'A' attempt:")
    from core.double_height_text import display_double_height_text
    display_double_height_text(working_core, "A", justify='center')
    input("Press Enter to continue...")
    clear()
    
    # Show them side by side with positions
    print("Side by side - Regular 'A' on left, Double 'A' on right:")
    
    # Create a buffer with both
    buffer = [0] * 105
    
    # Regular 'A' on left (columns 5-10)
    regular_a = getbytes("A")
    for i, byte in enumerate(regular_a):
        if i + 5 < 30:
            buffer[i + 5] = byte
    
    # Double-height 'A' on right (columns 20-25)
    from core.double_height_text import get_double_height_bytes
    top_bytes, bottom_bytes = get_double_height_bytes("A")
    
    for i, byte in enumerate(top_bytes):
        if i + 20 < 30:
            buffer[i + 20] = byte
            
    for i, byte in enumerate(bottom_bytes):
        if i + 50 < 105:  # 20 + 30 for bottom row offset
            buffer[i + 50] = byte
    
    working_core.fill(bytes(buffer))
    input("Press Enter to continue...")
    clear()

def test_step_by_step():
    """Step through the double height process manually."""
    print("🔍 Step-by-Step Double Height Creation")
    print("=" * 50)
    
    from core.double_height_text import double_height_dict
    
    char = 'A'
    print(f"Creating double-height '{char}'")
    
    if char not in double_height_dict:
        print(f"Character '{char}' not in dictionary!")
        return
    
    char_data = double_height_dict[char]
    print(f"Character data: {char_data}")
    
    # Split the data
    char_width = len(char_data) // 2
    top_part = char_data[:char_width]
    bottom_part = char_data[char_width:]
    
    print(f"Top part: {top_part}")
    print(f"Bottom part: {bottom_part}")
    
    # Show just the top part
    print("Step 1: Top part only")
    buffer1 = [0] * 105
    for i, byte in enumerate(top_part):
        if i + 12 < 30:  # Center it
            buffer1[i + 12] = byte
    
    working_core.fill(bytes(buffer1))
    input("Press Enter for next step...")
    
    # Show just the bottom part
    print("Step 2: Bottom part only")
    buffer2 = [0] * 105
    for i, byte in enumerate(bottom_part):
        if i + 42 < 105:  # 12 + 30 for bottom row
            buffer2[i + 42] = byte
    
    working_core.fill(bytes(buffer2))
    input("Press Enter for next step...")
    
    # Show both together
    print("Step 3: Both parts together")
    buffer3 = [0] * 105
    for i, byte in enumerate(top_part):
        if i + 12 < 30:
            buffer3[i + 12] = byte
    for i, byte in enumerate(bottom_part):
        if i + 42 < 105:
            buffer3[i + 42] = byte
    
    working_core.fill(bytes(buffer3))
    input("Press Enter to continue...")
    clear()

if __name__ == "__main__":
    print("👁️  Visual Double Height Test")
    print("=" * 50)
    
    print("This will help us see what's actually happening on the display.")
    print("Make sure you can see your flipdot display!")
    
    tests = [
        ("1", "Display Buffer Mapping", test_display_mapping),
        ("2", "Character Comparison", test_character_comparison), 
        ("3", "Step-by-Step Creation", test_step_by_step),
    ]
    
    print("\nAvailable tests:")
    for key, desc, _ in tests:
        print(f"{key}. {desc}")
    print("a. Run all tests")
    print("q. Quit")
    
    choice = input("\nSelect test: ").strip().lower()
    
    if choice == 'q':
        print("Goodbye!")
    elif choice == 'a':
        for _, desc, test_func in tests:
            print(f"\n🎯 Running: {desc}")
            test_func()
            print(f"✅ {desc} completed")
    else:
        for key, desc, test_func in tests:
            if choice == key:
                print(f"\n🎯 Running: {desc}")
                test_func()
                print(f"✅ {desc} completed")
                break
        else:
            print("Invalid choice")
    
    print("\nVisual test complete!")
