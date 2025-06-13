#!/usr/bin/env python3
"""
Test the corrected buffer mapping for double-height text
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, clear

def test_corrected_mapping():
    """Test the corrected buffer mapping for double-height text."""
    print("🔧 Testing Corrected Buffer Mapping")
    print("=" * 50)
    
    # Test 1: Manual double-height 'I' with corrected mapping
    print("Test 1: Manual double-height 'I' (corrected mapping)")
    buffer1 = [0] * 105
    
    # Top row: center columns (positions 14-15)
    buffer1[14] = 0b1111111  # All 7 bits
    buffer1[15] = 0b1111111  # Make it 2 columns wide
    
    # Bottom row: same columns but at positions 75+14 and 75+15
    buffer1[75 + 14] = 0b1111111  # Position 89
    buffer1[75 + 15] = 0b1111111  # Position 90
    
    print(f"Top row positions 14-15: {buffer1[14]}, {buffer1[15]}")
    print(f"Bottom row positions 89-90: {buffer1[89]}, {buffer1[90]}")
    
    input("Press Enter to display corrected double-height 'I'...")
    working_core.fill(bytes(buffer1))
    time.sleep(3)
    clear()
    
    # Test 2: Compare with regular single height
    print("\nTest 2: Comparison - single height 'I' first")
    working_core.display_text("I", justify='center')
    input("Press Enter to see double-height version...")
    
    # Now show double-height using the corrected function
    from core.double_height_text import display_double_height_text
    display_double_height_text(working_core, "I", justify='center')
    input("Press Enter to continue...")
    clear()
    
    # Test 3: Test with 'HI' 
    print("\nTest 3: Double-height 'HI' with corrected mapping")
    display_double_height_text(working_core, "HI", justify='center')
    input("Press Enter to continue...")
    clear()
    
    print("✅ Buffer mapping test complete!")

def show_buffer_layout():
    """Show how the 105-byte buffer maps to the display."""
    print("\n📊 Buffer Layout Explanation")
    print("=" * 50)
    print("Your display buffer mapping:")
    print("Positions   0-29:  Top row (left to right)")
    print("Positions  30-74:  Unused/special mapping")  
    print("Positions 75-104:  Bottom row (left to right)")
    print()
    print("For double-height text:")
    print("- Character top half goes to positions 0-29")
    print("- Character bottom half goes to positions 75-104")
    print("- This creates one tall character spanning both rows")

if __name__ == "__main__":
    print("🧪 Buffer Mapping Correction Test")
    print("=" * 50)
    
    show_buffer_layout()
    
    choice = input("\nRun buffer mapping test? (y/n): ").strip().lower()
    if choice == 'y':
        test_corrected_mapping()
    else:
        print("Test skipped.")
    
    print("\nTest complete!")
