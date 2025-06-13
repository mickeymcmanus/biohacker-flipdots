#!/usr/bin/env python3
"""
Exact Original Protocol Mimic

Let's copy your original flip() and fill() functions exactly, 
but modify only the constants to match your 30×14 display.
"""

import serial
import time
from core import core

class ExactOriginalMimic:
    """Exact copy of your original core functions with corrected constants."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize with your exact setup."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
    
    def flip(self, message: str, d: int = 1) -> None:
        """
        EXACT copy of your original flip() function,
        but with corrected row switching logic for 30-wide display.
        """
        i = 0
        self.serial.write(core.reset + core.row1)  # Use your original constants
        
        for k in message:
            i += 1
            try:
                c = core.dict[k]
            except KeyError:
                # Use '?' for unknown characters
                c = core.dict.get('?', b'\x00')
                
            # Switch to ROW2 when we've filled the top row
            # Your original switches at i > 15, but for 30-wide display,
            # we need to switch based on actual byte count
            if i > 5:  # Rough estimate - adjust this number
                if i == 6:  # First time switching to row 2
                    self.serial.write(core.reset + core.row2)
                # Reverse the string for the second row (from your original)
                c = c[::-1]
                
            self.serial.write(c)
    
    def fill_original_style(self, message: bytes, fillmask: int = 127) -> bytes:
        """
        Copy your original fill() function but adapt for 30-wide display.
        """
        self.serial.write(core.reset + core.row1)

        # Your original fill() sends 150 bytes total
        # Let's send 105 bytes like your working system but only put data in first 30
        for i in range(105):
            if i < 30:  # First 30 bytes go to top row (visible)
                if i < len(message):
                    self.serial.write(bytes([message[i] & fillmask]))
                else:
                    self.serial.write(b"\x00")
            else:  # Bytes 30-104 (not visible on your display)
                self.serial.write(b"\x00")

        # Now send ROW2 data
        self.serial.write(core.reset + core.row2)
        
        for i in range(105):
            if i < 30:  # First 30 bytes of row 2
                msg_index = 30 + i  # Start from byte 30 of message
                if msg_index < len(message):
                    # Apply your original's backward row logic
                    byte_val = message[msg_index] & fillmask
                    self.serial.write(bytes([byte_val]))
                else:
                    self.serial.write(b"\x00")
            else:  # Padding bytes
                self.serial.write(b"\x00")

        return message
    
    def clear_original_style(self) -> None:
        """Clear using your original method."""
        # Your original clear() calls fill() with empty bytes
        self.fill_original_style(b'\x00' * 105)
    
    def test_with_original_constants(self):
        """Test using your original's exact constants and methods."""
        print("Testing with original constants...")
        print(f"Original reset: {core.reset.hex()}")
        print(f"Original row1: {core.row1.hex()}")  
        print(f"Original row2: {core.row2.hex()}")
        
        # Test clear
        print("1. Clear test...")
        self.clear_original_style()
        time.sleep(2)
        
        # Test simple message
        print("2. Simple message test...")
        self.flip("HI")
        time.sleep(3)
        
        # Test longer message to trigger row 2
        print("3. Longer message test...")
        self.flip("HELLO WORLD TEST")
        time.sleep(3)
        
        # Test fill with pattern
        print("4. Fill pattern test...")
        pattern = b'\xFF\x00' * 30  # 60 bytes total
        self.fill_original_style(pattern)
        time.sleep(3)
        
        # Final clear
        print("5. Final clear...")
        self.clear_original_style()

def test_original_system_direct():
    """Test your original system directly to see exactly what it does."""
    
    print("=== Testing Original System Directly ===")
    
    try:
        print("1. Original flip('HELLO WORLD')...")
        core.flip("HELLO WORLD")
        time.sleep(3)
        
        print("2. Original flip with very long message...")
        core.flip("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") 
        time.sleep(5)
        
        print("3. Original clear...")
        core.clear()
        time.sleep(2)
        
        print("4. Original scrollleft...")
        msg_bytes = core.getbytes("SCROLL TEST MESSAGE")
        print(f"Message bytes: {len(msg_bytes)} bytes")
        core.scrollleft(msg_bytes, t=0.2)
        time.sleep(2)
        
        print("5. Original fill with pattern...")
        pattern = bytes([0xFF if i % 2 == 0 else 0x00 for i in range(60)])
        core.fill(pattern)
        time.sleep(3)
        
        core.clear()
        
    except Exception as e:
        print(f"Error testing original: {e}")
        import traceback
        traceback.print_exc()

def analyze_original_behavior():
    """Let's understand what your original system actually does."""
    
    print("=== Analyzing Original Behavior ===")
    
    print("Your original constants:")
    print(f"TROW: {core.TROW}")
    print(f"TCOLUMN: {core.TCOLUMN}")  
    print(f"ROW_BREAK: {getattr(core, 'ROW_BREAK', 'Not defined')}")
    
    print(f"\nSerial commands:")
    print(f"reset: {core.reset.hex()}")
    print(f"row1: {core.row1.hex()}")
    print(f"row2: {core.row2.hex()}")
    
    print(f"\nIn flip() function:")
    print(f"- Switch to ROW2 when i > 15")
    print(f"- For your 30-wide display, this might be wrong")
    print(f"- Maybe should switch when character position reaches edge?")
    
    print(f"\nTesting character positions:")
    test_msg = "HELLO"
    char_count = 0
    byte_count = 0
    
    for char in test_msg:
        char_count += 1
        char_bytes = core.dict.get(char, b'\x00')
        byte_count += len(char_bytes)
        print(f"Char {char_count}: '{char}' = {len(char_bytes)} bytes, total bytes: {byte_count}")
        
        if char_count > 15:
            print(f"  -> Would switch to ROW2 here (original logic)")
        
        if byte_count > 30:
            print(f"  -> Should switch to ROW2 here (for 30-wide display)")

if __name__ == "__main__":
    print("Exact Original Protocol Analysis")
    print("="*40)
    
    # First analyze what the original does
    analyze_original_behavior()
    
    print("\n" + "="*40)
    
    # Test original system directly  
    test_original_system_direct()
    
    print("\n" + "="*40)
    
    # Test our mimic
    try:
        mimic = ExactOriginalMimic()
        mimic.test_with_original_constants()
    except Exception as e:
        print(f"Mimic test failed: {e}")
