#!/usr/bin/env python3
"""
Double Height using your proven working buffer positions

This approach examines exactly how your working scrollleft() function 
places text and replicates that for double-height characters.
"""

import time
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.core import working_core, getbytes, clear

def analyze_working_position():
    """
    Analyze exactly where your working scrollleft places text.
    This will help us understand the buffer mapping.
    """
    print("🔍 Analyzing your working text positioning...")
    
    # Test with a simple character that we can see clearly
    test_char = "I"
    test_bytes = getbytes(test_char)
    
    print(f"Single character '{test_char}' generates {len(test_bytes)} bytes:")
    for i, byte in enumerate(test_bytes):
        print(f"  Byte {i}: {byte} (0b{byte:07b})")
    
    # Now let's see where position 103 places this
    padded_message = b'\x00' * 105 + test_bytes + b'\x00' * 105  # Your proven padding
    chunk = padded_message[103:103 + 105]  # Your proven position 103
    
    print(f"\nAt position 103, the 105-byte buffer contains:")
    for i, byte in enumerate(chunk):
        if byte != 0:  # Only show non-zero bytes
            print(f"  Buffer position {i}: {byte} (0b{byte:07b})")
    
    return chunk

def create_manual_double_height():
    """
    Create double-height text by manually placing bytes at the correct positions.
    """
    print("\n🔧 Creating manual double-height 'I'...")
    
    # First, let's see where a normal 'I' appears
    normal_chunk = analyze_working_position()
    
    # Now create a double-height version
    # We'll take the pattern and extend it vertically
    double_buffer = [0] * 105
    
    # Find where the 'I' character data is in the normal buffer
    for i, byte in enumerate(normal_chunk):
        if byte != 0:
            print(f"Found character data at buffer position {i}: {byte}")
            
            # Place the top half of double-height character
            double_buffer[i] = byte
            
            # Now we need to find where to place the bottom half
            # Let's try placing it at various offsets to see what works
            
            # Try offset +30 (if it's row-based)
            if i + 30 < 105:
                double_buffer[i + 30] = byte
                print(f"  Also placing at position {i + 30} (offset +30)")
            
            # Try offset +45 (if it's quadrant-based)  
            if i + 45 < 105:
                double_buffer[i + 45] = byte
                print(f"  Also placing at position {i + 45} (offset +45)")
    
    return bytes(double_buffer)

def test_double_height_offsets():
    """
    Test different offsets to find the correct double-height mapping.
    """
    print("\n🧪 Testing different double-height offsets...")
    
    # Get a working single-height 'I'
    test_bytes = getbytes("I")
    padded_message = b'\x00' * 105 + test_bytes + b'\x00' * 105
    base_chunk = padded_message[103:103 + 105]
    
    # Test different offsets for the bottom half
    offsets_to_try = [15, 30, 45, 60, 75]
    
    for offset in offsets_to_try:
        print(f"\nTesting offset +{offset}:")
        
        double_buffer = list(base_chunk)  # Start with the working top half
        
        # Add bottom half at this offset
        for i, byte in enumerate(base_chunk):
            if byte != 0 and i + offset < 105:
                double_buffer[i + offset] = byte
                print(f"  Adding bottom half: position {i} -> {i + offset}")
        
        print(f"Buffer preview (showing non-zero positions):")
        for i, byte in enumerate(double_buffer):
            if byte != 0:
                print(f"  Position {i}: {byte}")
        
        input(f"Press Enter to test offset +{offset} on display...")
        working_core.fill(bytes(double_buffer))
        time.sleep(3)
        clear()

def smart_double_height(message):
    """
    Create double-height text using the discovered correct offset.
    """
    print(f"\n🎯 Smart double-height for '{message}'")
    
    # Use your proven method to get the base positioning
    text_bytes = getbytes(message)
    padded_message = b'\x00' * 105 + text_bytes + b'\x00' * 105
    base_chunk = padded_message[103:103 + 105]  # Your proven position
    
    # Create double-height by duplicating at the correct offset
    # We'll try the most likely offset based on your hardware description
    double_buffer = list(base_chunk)
    
    # Based on your 2×6 module description, try offset +30 first
    # (This assumes upper half in positions 0-29, lower half in 30-59)
    OFFSET = 30  # We can adjust this based on test results
    
    for i, byte in enumerate(base_chunk):
        if byte != 0 and i + OFFSET < 105:
            double_buffer[i + OFFSET] = byte
    
    return bytes(double_buffer)

def test_smart_double_height():
    """Test the smart double-height approach."""
    print("🎯 Testing Smart Double Height")
    print("=" * 50)
    
    test_chars = ["I", "A", "HI"]
    
    for char in test_chars:
        print(f"\nTesting '{char}':")
        
        # Show normal version first
        print("1. Normal single-height:")
        working_core.display_text(char, justify='center')
        input("Press Enter to continue...")
        clear()
        
        # Show double-height version
        print("2. Smart double-height:")
        buffer = smart_double_height(char)
        working_core.fill(buffer)
        input("Press Enter to continue...")
        clear()

if __name__ == "__main__":
    print("🔧 Proven Double Height Method")
    print("=" * 50)
    print("This uses your working scrollleft positioning as the foundation.")
    
    choice = input("\nAnalyze working position? (y/n): ").strip().lower()
    if choice == 'y':
        analyze_working_position()
    
    choice = input("\nTest different offsets to find correct mapping? (y/n): ").strip().lower()
    if choice == 'y':
        test_double_height_offsets()
    
    choice = input("\nTest smart double height? (y/n): ").strip().lower()
    if choice == 'y':
        test_smart_double_height()
    
    print("\nTesting complete!")
