#!/usr/bin/env python3
"""
Find Correct Display Mapping

We need to systematically test where each part of the 105-byte buffer appears on your display.
"""

import time
from core.core import working_core, clear, getbytes, TCOLUMN

def test_buffer_sections():
    """Test different sections of the 105-byte buffer to find where they appear."""
    
    print("=== Testing Buffer Sections Systematically ===")
    
    # We'll test in sections of 15 bytes each
    sections = [
        (0, 15, "Section 0-15"),
        (15, 30, "Section 15-30"), 
        (30, 45, "Section 30-45"),
        (45, 60, "Section 45-60"),
        (60, 75, "Section 60-75"),
        (75, 90, "Section 75-90"),
        (90, 105, "Section 90-105"),
    ]
    
    for start, end, name in sections:
        print(f"\nTesting {name} (bytes {start}-{end}):")
        
        buffer = bytearray(TCOLUMN)  # All zeros
        
        # Fill this section with alternating pattern to make it visible
        for i in range(start, min(end, TCOLUMN)):
            buffer[i] = 0x7F if (i % 2 == 0) else 0x00  # Alternating on/off
        
        working_core.fill(bytes(buffer))
        time.sleep(2)
        
        response = input(f"  Where do you see the alternating pattern for {name}? (describe location): ")
        print(f"  Result: {response}")
        
        clear()
        time.sleep(1)

def test_known_working_position():
    """Test around the position we know works (103) to understand the pattern."""
    
    print("\n=== Testing Around Known Working Position 103 ===")
    
    # We know position 103 in the scrollleft padding works
    # Let's see what that actually corresponds to in the buffer
    
    print("First, let's reproduce what works:")
    working_core.display_text("TEST", justify='center', height='single')
    time.sleep(3)
    response = input("Confirm this 'TEST' looks good (y/n): ")
    
    if response.lower() != 'y':
        print("Something's wrong with the basic function!")
        return
    
    clear()
    time.sleep(1)
    
    # Now let's manually put text at different positions in the buffer
    test_positions = [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105]
    
    for pos in test_positions:
        if pos < TCOLUMN:
            print(f"\nTesting text at buffer position {pos}:")
            
            buffer = bytearray(TCOLUMN)  # All zeros
            test_bytes = getbytes("X")  # Single character
            
            # Put the character at this position
            for i, byte in enumerate(test_bytes):
                if pos + i < TCOLUMN:
                    buffer[pos + i] = byte
            
            working_core.fill(bytes(buffer))
            time.sleep(2)
            
            response = input(f"  Where does 'X' appear at position {pos}? ")
            print(f"  Position {pos}: {response}")
            
            clear()
            time.sleep(1)

def test_bottom_row_systematically():
    """Try to find where the bottom row actually maps to."""
    
    print("\n=== Finding Bottom Row Mapping ===")
    
    # We know bytes 0-30 show on upper row, far left
    # Let's test other ranges to find the bottom row
    
    ranges_to_test = [
        (30, 45, "bytes 30-45"),
        (45, 60, "bytes 45-60"), 
        (60, 75, "bytes 60-75"),
        (20, 35, "bytes 20-35"),
        (35, 50, "bytes 35-50"),
        (50, 65, "bytes 50-65"),
    ]
    
    for start, end, name in ranges_to_test:
        print(f"\nTesting {name} for bottom row:")
        
        buffer = bytearray(TCOLUMN)
        
        # Put a distinctive pattern in this range
        pattern = getbytes("BOT")
        for i, byte in enumerate(pattern):
            if start + i < end and start + i < TCOLUMN:
                buffer[start + i] = byte
        
        working_core.fill(bytes(buffer))
        time.sleep(2)
        
        response = input(f"  Does 'BOT' appear on bottom row for {name}? (y/n): ")
        print(f"  {name}: {response}")
        
        if response.lower() == 'y':
            print(f"  ✅ Found bottom row mapping: {name}")
        
        clear()
        time.sleep(1)

if __name__ == "__main__":
    # Test buffer sections systematically
    test_buffer_sections()
    
    print("\n" + "="*60)
    
    # Test around the known working position
    test_known_working_position()
    
    print("\n" + "="*60)
    
    # Try to find the bottom row
    test_bottom_row_systematically()
