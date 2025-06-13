#!/usr/bin/env python3
"""
Double Height Debug

Let's figure out exactly how to put text on both rows properly.
"""

import time
from core.core import working_core, clear, getbytes, dict, TCOLUMN

def debug_display_mapping():
    """Debug exactly how the 105-byte buffer maps to your display."""
    
    print("=== Debugging Display Mapping ===")
    
    # We know from earlier testing:
    # - Position 103 puts single-height text on top row perfectly
    # - Your display shows bytes 75-105 on top row, bytes 0-30 on bottom row
    
    # Test 1: Put text explicitly in top row area (bytes 75-105)
    print("Test 1: Text in top row area only")
    
    buffer = bytearray(TCOLUMN)  # 105 bytes of zeros
    test_text = getbytes("TOP")
    
    # Put text starting at byte 75 (top row area)
    for i, byte in enumerate(test_text[:30]):  # Max 30 bytes for top row
        buffer[75 + i] = byte
    
    working_core.fill(bytes(buffer))
    time.sleep(3)
    
    response = input("Where does 'TOP' appear? ")
    print(f"Top row test: {response}")
    
    clear()
    time.sleep(1)
    
    # Test 2: Put text explicitly in bottom row area (bytes 0-30)
    print("Test 2: Text in bottom row area only")
    
    buffer = bytearray(TCOLUMN)  # 105 bytes of zeros
    test_text = getbytes("BOT")
    
    # Put text starting at byte 0 (bottom row area)
    for i, byte in enumerate(test_text[:30]):  # Max 30 bytes for bottom row
        buffer[i] = byte
    
    working_core.fill(bytes(buffer))
    time.sleep(3)
    
    response = input("Where does 'BOT' appear? ")
    print(f"Bottom row test: {response}")
    
    clear()
    time.sleep(1)
    
    # Test 3: Put SAME text in BOTH areas
    print("Test 3: Same text in both areas (true double height)")
    
    buffer = bytearray(TCOLUMN)  # 105 bytes of zeros
    test_text = getbytes("HI")
    
    # Put text in top row area (bytes 75-105)
    for i, byte in enumerate(test_text[:30]):
        buffer[75 + i] = byte
    
    # Put SAME text in bottom row area (bytes 0-30)
    for i, byte in enumerate(test_text[:30]):
        buffer[i] = byte
    
    working_core.fill(bytes(buffer))
    time.sleep(3)
    
    response = input("Does 'HI' appear on BOTH rows? ")
    print(f"Double placement test: {response}")
    
    clear()
    time.sleep(1)

def test_centered_double_height():
    """Test centered double-height text."""
    
    print("=== Testing Centered Double Height ===")
    
    test_messages = ["A", "HI", "TEST"]
    
    for msg in test_messages:
        print(f"\nTesting centered double-height: '{msg}'")
        
        buffer = bytearray(TCOLUMN)  # 105 bytes of zeros
        text_bytes = getbytes(msg)
        
        # Calculate centering for 30-column display
        if len(text_bytes) <= 30:
            center_offset = (30 - len(text_bytes)) // 2
            
            # Put text in top row area (bytes 75-105), centered
            for i, byte in enumerate(text_bytes):
                if center_offset + i < 30:
                    buffer[75 + center_offset + i] = byte
            
            # Put SAME text in bottom row area (bytes 0-30), centered  
            for i, byte in enumerate(text_bytes):
                if center_offset + i < 30:
                    buffer[center_offset + i] = byte
        
        working_core.fill(bytes(buffer))
        time.sleep(3)
        
        response = input(f"Does '{msg}' appear centered on BOTH rows? (y/n): ")
        
        if response.lower() == 'y':
            print(f"✅ Centered double-height working for '{msg}'")
        else:
            print(f"❌ Still not working for '{msg}'")
        
        clear()
        time.sleep(1)

def create_working_double_height_function():
    """Create a double-height function that actually works."""
    
    def display_text_working_double(message: str, justify: str = 'center'):
        """Display text on both rows for true double-height effect."""
        
        buffer = bytearray(TCOLUMN)  # 105 bytes of zeros
        text_bytes = getbytes(message.upper())
        
        if len(text_bytes) <= 30:
            # Calculate positioning
            if justify == 'center':
                offset = (30 - len(text_bytes)) // 2
            elif justify == 'right':
                offset = 30 - len(text_bytes)
            else:  # left
                offset = 0
            
            # Put text in top row area (bytes 75-105)
            for i, byte in enumerate(text_bytes):
                if offset + i < 30:
                    buffer[75 + offset + i] = byte
            
            # Put SAME text in bottom row area (bytes 0-30)
            for i, byte in enumerate(text_bytes):
                if offset + i < 30:
                    buffer[offset + i] = byte
        
        working_core.fill(bytes(buffer))
    
    return display_text_working_double

if __name__ == "__main__":
    # Debug the display mapping
    debug_display_mapping()
    
    print("\n" + "="*50)
    
    # Test centered double height
    test_centered_double_height()
    
    print("\n" + "="*50)
    
    # Test the working function
    display_double = create_working_double_height_function()
    
    print("=== Testing Working Double Height Function ===")
    
    for msg in ["A", "HI", "TEST"]:
        print(f"\nTesting working function with '{msg}':")
        display_double(msg, justify='center')
        time.sleep(3)
        
        response = input(f"Does '{msg}' appear on both rows? (y/n): ")
        print(f"Working function test: {response}")
        
        clear()
        time.sleep(1)
