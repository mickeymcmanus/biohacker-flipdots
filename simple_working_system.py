#!/usr/bin/env python3
"""
Simple Working System - Copy What Works Exactly

Since scrollleft and type_text work perfectly, let's just use their exact methods.
"""

import serial
import time
from core import core

class SimpleWorkingSystem:
    """Simple system that copies your working methods exactly."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize display."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
        
    def clear(self) -> None:
        """Clear using original method."""
        core.clear()
    
    def display_text_static(self, message: str, positioning: str = 'auto') -> None:
        """Display static text with smart positioning based on message length."""
        print(f"Displaying: '{message}' with {positioning} positioning")
        
        # Use EXACT same setup as your working scrollleft
        text_bytes = core.getbytes(message.upper())
        print(f"Message '{message}' = {len(text_bytes)} bytes")
        
        # This is EXACTLY what scrollleft does for padding
        padded_message = core.TCOLUMN * core.dict['space'] + text_bytes + core.TCOLUMN * core.dict['space']
        
        if positioning == 'auto':
            # Choose position based on message length
            if len(text_bytes) <= 25:
                # Short message - position it to appear mostly on top row
                # Position 105 puts text at start of visible area
                static_position = 105 - len(text_bytes) // 2
            elif len(text_bytes) <= 50:
                # Medium message - position to show nicely across both rows  
                static_position = 90
            else:
                # Long message - use scrollleft's starting position
                static_position = 83
        elif positioning == 'top_row':
            # Force to top row
            static_position = 105 - len(text_bytes)
        elif positioning == 'start_visible':
            # Position where text starts becoming visible
            static_position = 83
        else:
            # Default to what worked in analysis
            static_position = 83
        
        print(f"Using position {static_position}")
        
        # Get the chunk exactly like scrollleft does
        chunk = padded_message[static_position:static_position + core.TCOLUMN]
        
        # Use core.fill exactly like scrollleft does
        core.fill(chunk)
    
    def display_text_top_only(self, message: str) -> None:
        """Display short text on top row only."""
        print(f"Displaying on top row only: '{message}'")
        
        text_bytes = core.getbytes(message.upper())
        
        # Position text so it appears on top row
        # We need to find the right position to make text appear on top row
        padded_message = core.TCOLUMN * core.dict['space'] + text_bytes + core.TCOLUMN * core.dict['space']
        
        # Previous position was almost right but missing leftmost column
        # Let's try a position that's 1-2 positions earlier
        if len(text_bytes) <= 30:
            # Adjust position to include the leftmost column
            static_position = 103 + (30 - len(text_bytes)) // 2  # Was 105, now 103
        else:
            static_position = 103  # Was 105, now 103
        
        print(f"Top-only position: {static_position}")
        
        chunk = padded_message[static_position:static_position + core.TCOLUMN]
        core.fill(chunk)
    
    def display_text_split_properly(self, message: str) -> None:
        """Display text split properly across both rows."""
        print(f"Displaying split across rows: '{message}'")
        
        words = message.upper().split()
        
        # Try to split at word boundary
        first_part = ""
        second_part = ""
        
        for word in words:
            test_first = (first_part + " " + word).strip()
            if len(core.getbytes(test_first)) <= 30:
                first_part = test_first
            else:
                second_part = (second_part + " " + word).strip()
        
        print(f"Split: '{first_part}' / '{second_part}'")
        
        # Display first part positioned for top row
        if first_part:
            self.display_text_static(first_part, positioning='top_row')
            time.sleep(0.1)
        
        # Add second part positioned for bottom row
        if second_part:
            # This is tricky - we need to add to existing display
            # For now, let's just show the split version
            full_message = first_part + " " + second_part
            self.display_text_static(full_message, positioning='start_visible')
    
    def scroll_text(self, message: str, speed: float = 0.2) -> None:
        """Scroll text - just use your working scrollleft."""
        text_bytes = core.getbytes(message.upper())
        core.scrollleft(text_bytes, t=speed)
    
    def type_text(self, message: str, char_delay: float = 0.2) -> None:
        """Type text - copy the working type_text approach."""
        print(f"Typing: '{message}'")
        
        # This works perfectly, so let's copy it exactly
        for i in range(1, len(message) + 1):
            partial_message = message[:i]
            self.display_text_static(partial_message)
            time.sleep(char_delay)
    
    def flash_message(self, message: str, times: int = 5) -> None:
        """Flash message."""
        for _ in range(times):
            self.display_text_static(message)
            time.sleep(0.5)
            self.clear()
            time.sleep(0.3)
    
    def test_pattern(self) -> None:
        """Test pattern using core.fill with simple pattern."""
        print("Test pattern...")
        
        # Create simple alternating pattern
        pattern = b''
        for i in range(core.TCOLUMN):
            if i % 2 == 0:
                pattern += b'\x7F'
            else:
                pattern += b'\x00'
        
        core.fill(pattern)
        time.sleep(3)

def test_simple_system():
    """Test the simple system with different positioning options."""
    
    print("=== Testing Simple Working System ===")
    
    system = SimpleWorkingSystem()
    
    try:
        print("1. Clear...")
        system.clear()
        time.sleep(2)
        
        print("2. Test 'HELLO' with different positions...")
        
        print("   a) Auto positioning...")
        system.display_text_static("HELLO", positioning='auto')
        time.sleep(3)
        
        print("   b) Top row only...")
        system.display_text_top_only("HELLO")
        time.sleep(3)
        
        print("3. Test 'ALERT' with different positions...")
        
        print("   a) Auto positioning...")
        system.display_text_static("ALERT", positioning='auto')
        time.sleep(3)
        
        print("   b) Top row only...")
        system.display_text_top_only("ALERT")
        time.sleep(3)
        
        print("4. Test 'HELLO WORLD' with split...")
        system.display_text_split_properly("HELLO WORLD")
        time.sleep(4)
        
        print("5. Test patterns...")
        system.test_pattern()
        time.sleep(2)
        
        print("6. Working examples...")
        print("   Type text (we know this works)...")
        system.type_text("HI")
        time.sleep(2)
        
        print("   Scroll text (we know this works)...")  
        system.scroll_text("SCROLL TEST")
        
        print("7. Final clear...")
        system.clear()
        
        print("✅ Test complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def analyze_scrollleft_frames():
    """Analyze what scrollleft does frame by frame."""
    
    print("=== Analyzing scrollleft frames ===")
    
    message = "HELLO WORLD"
    text_bytes = core.getbytes(message.upper())
    print(f"Message: '{message}' = {len(text_bytes)} bytes")
    
    # Recreate scrollleft's padding
    padded_message = core.TCOLUMN * core.dict['space'] + text_bytes + core.TCOLUMN * core.dict['space']
    print(f"Padded length: {len(padded_message)} bytes")
    
    message_len = len(padded_message) - core.TCOLUMN
    print(f"Will scroll through {message_len} positions")
    
    # Show a few key frames
    key_frames = [0, message_len//4, message_len//2, 3*message_len//4, message_len-1]
    
    for i, frame_pos in enumerate(key_frames):
        print(f"\nFrame {i+1} (position {frame_pos}):")
        chunk = padded_message[frame_pos:frame_pos + core.TCOLUMN]
        print(f"Chunk length: {len(chunk)} bytes")
        
        # Show this frame
        core.fill(chunk)
        time.sleep(2)
        
        response = input(f"Describe what you see for frame {i+1}: ")
        print(f"Frame {i+1}: {response}")

if __name__ == "__main__":
    print("Simple Working System")
    print("="*40)
    
    choice = input("(1) Test simple system, (2) Analyze scrollleft frames: ")
    
    if choice == "2":
        analyze_scrollleft_frames()
    else:
        test_simple_system()
