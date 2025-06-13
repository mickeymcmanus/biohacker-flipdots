#!/usr/bin/env python3
"""
Simple Direct Core - Based on Working Diagnostic

Uses the exact same approach as the working diagnostic test.
"""

import serial
import time
from core import core  # Import your original for character data

class SimpleFlipdotDisplay:
    """Simple display that uses the working diagnostic approach."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize with direct serial connection."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
    
    def clear(self) -> None:
        """Clear display using the working diagnostic method."""
        print("Clearing display...")
        
        # Clear top row - this worked in diagnostic
        self.serial.write(b'\x81')  # RESET
        self.serial.write(b'\x82')  # ROW1
        self.serial.write(b'\x00' * 30)  # Clear 30 columns
        
        # Clear bottom row - try different approach
        self.serial.write(b'\x81')  # RESET
        self.serial.write(b'\x83')  # Try ROW2 as \x83 instead of \x82
        self.serial.write(b'\x00' * 30)  # Clear 30 columns
        
        time.sleep(0.1)  # Small delay like in diagnostic
    
    def test_pattern(self) -> None:
        """Display test pattern using working diagnostic method."""
        print("Displaying test pattern...")
        
        # Top row pattern - this worked
        self.serial.write(b'\x81')  # RESET
        self.serial.write(b'\x82')  # ROW1
        for i in range(30):
            if i % 2 == 0:
                self.serial.write(b'\x7F')  # All dots on
            else:
                self.serial.write(b'\x00')  # All dots off
        
        # Bottom row pattern - try same approach
        self.serial.write(b'\x81')  # RESET
        self.serial.write(b'\x83')  # ROW2
        for i in range(30):
            if i % 2 == 1:  # Opposite pattern
                self.serial.write(b'\x7F')  # All dots on
            else:
                self.serial.write(b'\x00')  # All dots off
        
        time.sleep(0.1)
    
    def display_text_simple(self, text: str) -> None:
        """Display text using the working diagnostic approach."""
        print(f"Displaying text: '{text}'")
        
        # Top row
        self.serial.write(b'\x81')  # RESET
        self.serial.write(b'\x82')  # ROW1
        
        bytes_sent = 0
        for char in text.upper():
            if char in core.dict and bytes_sent < 25:  # Leave room for padding
                char_bytes = core.dict[char]
                self.serial.write(char_bytes)
                bytes_sent += len(char_bytes)
                
                # Add space between characters
                if bytes_sent < 25:
                    self.serial.write(core.dict['space'])
                    bytes_sent += len(core.dict['space'])
        
        # Pad rest of top row
        remaining = 30 - bytes_sent
        if remaining > 0:
            self.serial.write(b'\x00' * remaining)
        
        # Bottom row - try simple approach
        self.serial.write(b'\x81')  # RESET
        self.serial.write(b'\x83')  # ROW2 
        self.serial.write(b'\x00' * 30)  # Just clear bottom row for now
        
        time.sleep(0.1)
    
    def scroll_text_simple(self, text: str, speed: float = 0.2) -> None:
        """Simple scrolling using working approach."""
        print(f"Scrolling text: '{text}'")
        
        # Get text as bytes using original method
        text_bytes = core.getbytes(text)
        print(f"Text bytes: {len(text_bytes)} bytes")
        
        # Add padding for smooth scroll
        padded = b'\x00' * 30 + text_bytes + b'\x00' * 30
        
        # Scroll through the text
        for i in range(len(padded) - 30 + 1):
            chunk = padded[i:i+30]
            
            # Display chunk on top row
            self.serial.write(b'\x81')  # RESET
            self.serial.write(b'\x82')  # ROW1
            
            if len(chunk) < 30:
                chunk += b'\x00' * (30 - len(chunk))
            
            self.serial.write(chunk)
            
            # Clear bottom row
            self.serial.write(b'\x81')  # RESET
            self.serial.write(b'\x83')  # ROW2
            self.serial.write(b'\x00' * 30)
            
            time.sleep(speed)

def test_different_row_commands():
    """Test different row command sequences to find what works."""
    
    print("=== Testing Different Row Commands ===")
    
    display = SimpleFlipdotDisplay()
    
    # Test 1: Clear with different commands
    print("\n1. Testing clear with \\x82 and \\x83...")
    display.serial.write(b'\x81\x82')  # RESET + ROW1
    display.serial.write(b'\x00' * 30)
    display.serial.write(b'\x81\x83')  # RESET + ROW2
    display.serial.write(b'\x00' * 30)
    time.sleep(2)
    
    # Test 2: Pattern on both rows
    print("2. Testing pattern on both rows...")
    display.serial.write(b'\x81\x82')  # Top row
    display.serial.write(b'\x55' * 30)  # Pattern
    display.serial.write(b'\x81\x83')  # Bottom row  
    display.serial.write(b'\xAA' * 30)  # Different pattern
    time.sleep(3)
    
    # Test 3: Try original's exact sequence
    print("3. Testing original's exact sequence...")
    display.serial.write(b'\x81\x81')  # Like your original
    display.serial.write(b'\x7F' * 30)  # Pattern
    display.serial.write(b'\x81\x82')  # Like your original
    display.serial.write(b'\x3F' * 30)  # Different pattern
    time.sleep(3)
    
    # Test 4: Simple clear test
    print("4. Final clear test...")
    display.clear()
    time.sleep(2)

def test_simple_display():
    """Test the simple display approach."""
    
    print("=== Testing Simple Display ===")
    
    display = SimpleFlipdotDisplay()
    
    try:
        print("1. Clear display...")
        display.clear()
        time.sleep(2)
        
        print("2. Test pattern...")
        display.test_pattern()
        time.sleep(3)
        
        print("3. Display text...")
        display.display_text_simple("HI")
        time.sleep(3)
        
        print("4. Scroll text...")
        display.scroll_text_simple("HELLO WORLD")
        time.sleep(2)
        
        print("5. Final clear...")
        display.clear()
        
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Simple Direct Core Test")
    print("="*30)
    
    # First test different row commands
    test_different_row_commands()
    
    print("\n" + "="*30)
    
    # Then test the simple display
    test_simple_display()
