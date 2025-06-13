#!/usr/bin/env python3
"""
Working Flipdot Core - With Proper Bottom Row Support

Now that we know the bottom row works but displays backwards, 
let's create a proper implementation.
"""

import serial
import time
from core import core  # Import your working original for character data

class WorkingFlipdotDisplay:
    """Flipdot display that properly handles both rows including backward bottom row."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize with your exact setup."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
        
        # Display configuration for your 2×6 setup
        self.width = 30  # 6 modules × 5 pixels each
        self.height = 14  # 2 modules × 7 pixels each
        self.row_height = 7  # Each module row is 7 pixels high
    
    def clear(self) -> None:
        """Clear both rows properly."""
        print("Clearing display...")
        
        # Clear using the method that we know works from your original
        # Your original clear() sends \x81\x81 + data, then \x81\x82 + data
        
        # Clear top row
        self.serial.write(b'\x81\x81')
        self.serial.write(b'\x00' * 105)  # Send 105 bytes like original
        
        # Clear bottom row  
        self.serial.write(b'\x81\x82')
        self.serial.write(b'\x00' * 105)  # Send 105 bytes like original
        
        time.sleep(0.1)
    
    def display_text_both_rows(self, message: str) -> None:
        """Display text across both rows, handling backward bottom row."""
        print(f"Displaying: '{message}'")
        
        # Use your original's character encoding
        text_bytes = core.getbytes(message.upper())
        print(f"Text bytes: {len(text_bytes)} bytes")
        
        if len(text_bytes) <= 30:
            # Short message - display on top row only
            self._display_top_row(text_bytes)
            self._clear_bottom_row()
        else:
            # Long message - split across both rows
            top_part = text_bytes[:30]
            bottom_part = text_bytes[30:60]  # Next 30 bytes
            
            self._display_top_row(top_part)
            self._display_bottom_row_reversed(bottom_part)
    
    def _display_top_row(self, data: bytes) -> None:
        """Display data on top row (normal direction)."""
        # Pad to 105 bytes like your original system expects
        padded_data = data[:30] + b'\x00' * 75  # Only first 30 bytes visible
        
        self.serial.write(b'\x81\x81')  # Your original's top row command
        self.serial.write(padded_data)
    
    def _display_bottom_row_reversed(self, data: bytes) -> None:
        """Display data on bottom row with proper reversal."""
        # Reverse the byte order for bottom row (like your original flip() does)
        reversed_data = data[::-1]
        
        # Pad to 105 bytes
        padded_data = reversed_data[:30] + b'\x00' * 75
        
        self.serial.write(b'\x81\x82')  # Your original's bottom row command
        self.serial.write(padded_data)
    
    def _clear_bottom_row(self) -> None:
        """Clear just the bottom row."""
        self.serial.write(b'\x81\x82')
        self.serial.write(b'\x00' * 105)
    
    def scroll_text(self, message: str, speed: float = 0.2) -> None:
        """Scroll text across both rows."""
        print(f"Scrolling: '{message}'")
        
        text_bytes = core.getbytes(message.upper())
        
        # Add padding for smooth scrolling
        padded = b'\x00' * 30 + text_bytes + b'\x00' * 30
        
        for i in range(len(padded) - 30 + 1):
            chunk = padded[i:i+30]
            
            if len(text_bytes) > 30:
                # For long messages, show part on each row
                top_chunk = chunk[:15] if len(chunk) > 15 else chunk
                bottom_chunk = chunk[15:30] if len(chunk) > 15 else b''
                
                self._display_top_row(top_chunk)
                if bottom_chunk:
                    self._display_bottom_row_reversed(bottom_chunk)
                else:
                    self._clear_bottom_row()
            else:
                # Short message on top row only
                self._display_top_row(chunk)
                self._clear_bottom_row()
            
            time.sleep(speed)
    
    def test_pattern(self) -> None:
        """Display test pattern on both rows."""
        print("Displaying test pattern...")
        
        # Top row pattern
        top_pattern = b'\x7F\x00' * 15  # Alternating columns
        self._display_top_row(top_pattern)
        
        # Bottom row pattern (will appear reversed)
        bottom_pattern = b'\x0F\x70' * 15  # Different pattern
        self._display_bottom_row_reversed(bottom_pattern)
        
        time.sleep(3)
    
    def display_message_properly(self, message: str) -> None:
        """Display message with proper handling of both rows."""
        
        if len(message) <= 5:  # Very short - center on top
            self.display_text_both_rows(f"  {message}  ")
        elif len(message) <= 15:  # Medium - top row
            self.display_text_both_rows(message)
        else:  # Long - split across rows
            # Split at word boundary if possible
            words = message.split()
            top_line = ""
            bottom_line = ""
            
            for word in words:
                if len(top_line + word) <= 15:
                    top_line += word + " "
                else:
                    bottom_line += word + " "
            
            # Display top line normally
            top_bytes = core.getbytes(top_line.strip().upper())
            self._display_top_row(top_bytes)
            
            # Display bottom line (will be reversed by hardware)  
            if bottom_line.strip():
                bottom_bytes = core.getbytes(bottom_line.strip().upper())
                self._display_bottom_row_reversed(bottom_bytes)
            else:
                self._clear_bottom_row()

def test_working_display():
    """Test the working display system."""
    
    print("=== Testing Working Display System ===")
    
    display = WorkingFlipdotDisplay()
    
    try:
        print("1. Clear display...")
        display.clear()
        time.sleep(2)
        
        print("2. Test pattern...")
        display.test_pattern()
        time.sleep(3)
        
        print("3. Short message...")
        display.display_message_properly("HELLO")
        time.sleep(3)
        
        print("4. Medium message...")
        display.display_message_properly("HELLO WORLD")
        time.sleep(3)
        
        print("5. Long message (split across rows)...")
        display.display_message_properly("THIS IS A VERY LONG MESSAGE")
        time.sleep(4)
        
        print("6. Scrolling message...")
        display.scroll_text("SCROLLING TEXT ACROSS THE DISPLAY")
        time.sleep(2)
        
        print("7. Final clear...")
        display.clear()
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Working Flipdot Display Test")
    print("="*40)
    print("Now that we know both rows work, let's test proper implementation!")
    
    test_working_display()
