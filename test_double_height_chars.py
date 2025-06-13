#!/usr/bin/env python3
"""
Test Double Height Characters

Test the double-height character creation to make sure it works properly.
"""

import time
from core.core import working_core, clear, dict

def test_character_conversion():
    """Test converting single characters to double height."""
    
    print("=== Testing Character Conversion ===")
    
    # Test with simple characters
    test_chars = ['A', 'H', 'I', 'O']
    
    for char in test_chars:
        print(f"\nTesting character '{char}':")
        
        if char in dict:
            original_bytes = dict[char]
            print(f"Original bytes: {[hex(b) for b in original_bytes]}")
            
            # Test our double-height conversion
            try:
                for byte in original_bytes:
                    double_height_bytes = working_core.create_double_height_char(byte)
                    print(f"  Byte {hex(byte)} -> Double height: {[hex(b) for b in double_height_bytes]}")
                    
                    # Show bit patterns
                    print(f"    Original:  {format(byte, '07b')}")
                    print(f"    Double[0]: {format(double_height_bytes[0], '07b')}")
                    print(f"    Double[1]: {format(double_height_bytes[1], '07b')}")
                    
            except Exception as e:
                print(f"  ❌ Error converting {char}: {e}")
        else:
            print(f"  Character '{char}' not in dictionary")

def test_double_height_display():
    """Test displaying double-height characters."""
    
    print("\n=== Testing Double Height Display ===")
    
    test_messages = ["A", "HI", "TEST"]
    
    for msg in test_messages:
        print(f"\nTesting message: '{msg}'")
        
        try:
            # Single height
            print("  Single height...")
            working_core.display_text(msg, justify='center', height='single')
            time.sleep(2)
            
            # Double height
            print("  Double height...")
            working_core.display_text(msg, justify='center', height='double')
            time.sleep(3)
            
            clear()
            print(f"  ✅ {msg} - OK")
            
        except Exception as e:
            print(f"  ❌ {msg} - Error: {e}")
            import traceback
            traceback.print_exc()

def test_bit_stretching():
    """Test the bit stretching algorithm with simple patterns."""
    
    print("\n=== Testing Bit Stretching ===")
    
    # Test with simple bit patterns
    test_patterns = [
        0b0000001,  # Single bit at bottom
        0b1000000,  # Single bit at top  
        0b0001000,  # Single bit in middle
        0b1010101,  # Alternating pattern
        0b1111111,  # All bits on
    ]
    
    for pattern in test_patterns:
        print(f"\nTesting pattern: {format(pattern, '07b')}")
        try:
            result = working_core.create_double_height_char(pattern)
            print(f"  Result[0]: {format(result[0], '07b')}")
            print(f"  Result[1]: {format(result[1], '07b')}")
            
            # Visual representation
            print("  Visual:")
            print("  Original:  Double:")
            for i in range(7):
                orig_bit = "█" if pattern & (1 << (6-i)) else "."
                double_bit_0 = "█" if result[0] & (1 << (6-i)) else "."
                double_bit_1 = "█" if result[1] & (1 << (6-i)) else "."
                print(f"     {orig_bit}    ->  {double_bit_0}")
                if i < 6:  # Don't print extra line for last bit
                    print(f"          {double_bit_1}")
                    
        except Exception as e:
            print(f"  ❌ Error with pattern {format(pattern, '07b')}: {e}")

if __name__ == "__main__":
    # Test step by step
    test_bit_stretching()
    test_character_conversion()
    test_double_height_display()
