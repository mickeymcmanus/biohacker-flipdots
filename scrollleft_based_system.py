#!/usr/bin/env python3
"""
System Based on Working scrollleft

Since your original scrollleft works with both rows, let's base everything on that approach.
"""

import serial
import time
from core import core

class ScrollBasedFlipdotDisplay:
    """Flipdot display based on your working scrollleft approach."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize display."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
    
    def clear(self) -> None:
        """Clear using scrollleft approach with empty data."""
        print("Clearing display...")
        # Use scrollleft with minimal empty data
        empty_bytes = b'\x00' * 60  # Enough to clear both rows
        self._scrollleft_single_frame(empty_bytes)
        time.sleep(0.1)
    
    def display_static_text(self, message: str) -> None:
        """Display static text using scrollleft approach."""
        print(f"Displaying static: '{message}'")
        
        # Get text bytes using original method
        text_bytes = core.getbytes(message.upper())
        
        # Pad to center the text
        if len(text_bytes) < 60:  # Can fit in display
            padding = (60 - len(text_bytes)) // 2
            padded_bytes = b'\x00' * padding + text_bytes + b'\x00' * padding
            if len(padded_bytes) < 60:
                padded_bytes += b'\x00' * (60 - len(padded_bytes))
        else:
            padded_bytes = text_bytes[:60]  # Truncate if too long
        
        self._scrollleft_single_frame(padded_bytes)
    
    def scroll_text(self, message: str, speed: float = 0.2) -> None:
        """Scroll text using your working scrollleft method."""
        print(f"Scrolling: '{message}'")
        
        # Use your original scrollleft directly - we know this works!
        text_bytes = core.getbytes(message.upper())
        core.scrollleft(text_bytes, t=speed)
    
    def _scrollleft_single_frame(self, message: bytes) -> None:
        """
        Display a single frame using the same approach as your working scrollleft.
        This mimics what scrollleft does for each frame.
        """
        # Look at your original scrollleft in core.py to see exactly what it does
        # We'll implement the same fill logic that scrollleft uses
        
        # Use your original fill method since scrollleft calls it
        core.fill(message)
    
    def fill_pattern(self, pattern: bytes) -> None:
        """Fill display with pattern using working approach."""
        print("Filling with pattern...")
        
        # Use original fill since it works when called by scrollleft
        core.fill(pattern)
    
    def test_pattern(self) -> None:
        """Test pattern using working methods."""
        print("Testing pattern...")
        
        # Create alternating pattern for both rows
        pattern = b''
        for i in range(60):  # 60 bytes for both rows
            if i % 2 == 0:
                pattern += b'\x7F'  # Bright
            else:
                pattern += b'\x00'  # Dark
        
        self.fill_pattern(pattern)
        time.sleep(3)
    
    def analyze_working_scrollleft(self):
        """Analyze what makes scrollleft work when others don't."""
        print("=== Analyzing Working scrollleft ===")
        
        # Test 1: What scrollleft does step by step
        print("1. Testing what scrollleft actually calls...")
        
        test_message = "HELLO WORLD"
        text_bytes = core.getbytes(test_message)
        print(f"Text bytes: {len(text_bytes)} bytes = {text_bytes.hex()}")
        
        # scrollleft adds padding like this:
        padded_message = core.TCOLUMN * core.dict['space'] + text_bytes + core.TCOLUMN * core.dict['space']
        print(f"Padded length: {len(padded_message)} bytes")
        print(f"TCOLUMN: {core.TCOLUMN}")
        
        # Test 2: Manual recreation of scrollleft's first frame
        print("\n2. Recreating scrollleft's first frame...")
        first_frame = padded_message[:core.TCOLUMN]
        print(f"First frame: {len(first_frame)} bytes")
        
        print("Calling core.fill() with first frame...")
        core.fill(first_frame)
        time.sleep(3)
        
        # Test 3: Manual recreation of scrollleft's middle frame
        print("\n3. Recreating scrollleft's middle frame...")
        middle_pos = len(padded_message) // 2
        middle_frame = padded_message[middle_pos:middle_pos + core.TCOLUMN]
        print(f"Middle frame: {len(middle_frame)} bytes")
        
        print("Calling core.fill() with middle frame...")
        core.fill(middle_frame)
        time.sleep(3)
        
        # Test 4: Check if it's about the data length
        print(f"\n4. Testing different data lengths...")
        
        for length in [30, 60, 105]:
            print(f"Testing with {length} bytes...")
            test_data = (b'\xFF\x00' * (length // 2))[:length]
            core.fill(test_data)
            time.sleep(2)
            
        return padded_message

def test_scroll_based_system():
    """Test the scroll-based system."""
    
    print("=== Testing Scroll-Based System ===")
    
    display = ScrollBasedFlipdotDisplay()
    
    try:
        print("1. Analyze working scrollleft...")
        padded_msg = display.analyze_working_scrollleft()
        
        print("\n2. Clear display...")
        display.clear()
        time.sleep(2)
        
        print("3. Test pattern...")
        display.test_pattern()
        time.sleep(3)
        
        print("4. Static text display...")
        display.display_static_text("HELLO")
        time.sleep(3)
        
        print("5. Scroll text (using working method)...")
        display.scroll_text("THIS IS A SCROLLING MESSAGE TEST")
        time.sleep(2)
        
        print("6. Final clear...")
        display.clear()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def compare_working_vs_broken():
    """Compare what works vs what doesn't."""
    
    print("=== Comparing Working vs Broken Methods ===")
    
    try:
        # What works
        print("✅ WORKING: original scrollleft")
        msg_bytes = core.getbytes("TEST MESSAGE")
        core.scrollleft(msg_bytes, t=0.3)
        time.sleep(1)
        
        print("❌ BROKEN: original flip")
        core.flip("TEST MESSAGE")
        time.sleep(3)
        
        print("❓ TESTING: original fill with scrollleft-sized data")
        # Try calling fill with the same data size that scrollleft uses
        padded = core.TCOLUMN * core.dict['space'] + msg_bytes
        first_chunk = padded[:core.TCOLUMN]
        core.fill(first_chunk)
        time.sleep(3)
        
        core.clear()
        
    except Exception as e:
        print(f"Error in comparison: {e}")

if __name__ == "__main__":
    print("Scroll-Based Flipdot System")
    print("="*40)
    print("Building on your working scrollleft function...")
    
    # First compare what works vs what doesn't
    compare_working_vs_broken()
    
    print("\n" + "="*40)
    
    # Then test our scroll-based system
    test_scroll_based_system()
