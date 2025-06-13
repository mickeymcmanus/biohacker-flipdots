#!/usr/bin/env python3
"""
Final Working Flipdot System

Based on your working scrollleft, this creates a complete system that properly
uses both rows of your display.
"""

import serial
import time
from core import core

class WorkingFlipdotSystem:
    """Complete flipdot system based on your working scrollleft approach."""
    
    def __init__(self, port: str = '/dev/tty.usbserial-A3000lDq', baud: int = 38400):
        """Initialize display."""
        try:
            self.serial = serial.Serial(port, baud, timeout=1)
            print(f"Connected to flipdot display on {port}")
        except (serial.SerialException, OSError) as e:
            print(f"Could not connect to {port}: {e}")
            raise
    
    def clear(self) -> None:
        """Clear display using the working scrollleft approach."""
        # Create empty data the same size as scrollleft uses
        empty_data = b'\x00' * core.TCOLUMN
        core.fill(empty_data)
    
    def display_text_static(self, message: str, justify: str = 'center') -> None:
        """Display static text using scrollleft's working method."""
        print(f"Displaying: '{message}'")
        
        # Use original getbytes to convert text
        text_bytes = core.getbytes(message.upper())
        
        # Create display buffer the same size scrollleft uses (TCOLUMN = 105)
        if justify == 'center':
            # Center the text
            if len(text_bytes) < core.TCOLUMN:
                padding = (core.TCOLUMN - len(text_bytes)) // 2
                display_data = (b'\x00' * padding + text_bytes + 
                               b'\x00' * (core.TCOLUMN - len(text_bytes) - padding))
            else:
                display_data = text_bytes[:core.TCOLUMN]
        elif justify == 'left':
            display_data = text_bytes + b'\x00' * (core.TCOLUMN - len(text_bytes))
        else:  # right
            display_data = b'\x00' * (core.TCOLUMN - len(text_bytes)) + text_bytes
        
        # Use core.fill() exactly like scrollleft does
        core.fill(display_data)
    
    def scroll_text(self, message: str, speed: float = 0.2, direction: str = 'left') -> None:
        """Scroll text - just use your working scrollleft."""
        print(f"Scrolling: '{message}'")
        
        text_bytes = core.getbytes(message.upper())
        
        if direction == 'left':
            # Use your working scrollleft
            core.scrollleft(text_bytes, t=speed)
        else:
            # For right scroll, we can use rotateright if it exists
            if hasattr(core, 'rotateright'):
                core.rotateright(text_bytes, t=speed)
            else:
                # Fallback to left scroll
                core.scrollleft(text_bytes, t=speed)
    
    def display_pattern(self, pattern_type: str = 'alternating') -> None:
        """Display test patterns with correct positioning."""
        print(f"Displaying {pattern_type} pattern...")
        
        # Create 105-byte buffer
        display_data = bytearray(b'\x00' * core.TCOLUMN)
        
        if pattern_type == 'alternating':
            # Alternating columns on both visible areas
            # Bottom row (bytes 0-30)
            for i in range(30):
                if i % 2 == 0:
                    display_data[i] = 0x7F
                else:
                    display_data[i] = 0x00
            # Top row (bytes 75-105)
            for i in range(30):
                if i % 2 == 1:  # Opposite pattern
                    display_data[75 + i] = 0x7F
                else:
                    display_data[75 + i] = 0x00
                    
        elif pattern_type == 'stripes':
            # Horizontal stripes
            pattern_byte = 0x55  # 01010101 pattern
            # Fill visible areas
            for i in range(30):
                display_data[i] = pattern_byte        # Bottom row
                display_data[75 + i] = pattern_byte   # Top row
                
        elif pattern_type == 'checkerboard':
            # Checkerboard pattern
            for i in range(30):
                if (i // 5) % 2 == 0:
                    display_data[i] = 0x33        # Bottom row
                    display_data[75 + i] = 0xCC   # Top row
                else:
                    display_data[i] = 0xCC        # Bottom row  
                    display_data[75 + i] = 0x33   # Top row
        else:
            # Solid pattern
            for i in range(30):
                display_data[i] = 0x7F        # Bottom row
                display_data[75 + i] = 0x7F   # Top row
        
        core.fill(bytes(display_data))
    
    def flash_message(self, message: str, times: int = 5, on_time: float = 0.5, off_time: float = 0.3) -> None:
        """Flash a message on and off."""
        print(f"Flashing: '{message}' {times} times")
        
        for _ in range(times):
            self.display_text_static(message)
            time.sleep(on_time)
            self.clear()
            time.sleep(off_time)
    
    def type_text(self, message: str, char_delay: float = 0.2) -> None:
        """Type text character by character."""
        print(f"Typing: '{message}'")
        
        for i in range(1, len(message) + 1):
            partial_message = message[:i]
            self.display_text_static(partial_message, justify='left')
            time.sleep(char_delay)
    
    def display_two_lines(self, line1: str, line2: str) -> None:
        """Display two lines of text (experimental - based on scrollleft working)."""
        print(f"Two lines: '{line1}' / '{line2}'")
        
        # Convert both lines
        line1_bytes = core.getbytes(line1.upper())
        line2_bytes = core.getbytes(line2.upper())
        
        # Try to create a buffer that puts line1 in first ~30 bytes, line2 in next ~30 bytes
        combined = b''
        
        # First 30 bytes for top row
        if len(line1_bytes) <= 30:
            combined += line1_bytes + b'\x00' * (30 - len(line1_bytes))
        else:
            combined += line1_bytes[:30]
        
        # Next 30 bytes for bottom row
        if len(line2_bytes) <= 30:
            combined += line2_bytes + b'\x00' * (30 - len(line2_bytes))
        else:
            combined += line2_bytes[:30]
        
        # Pad to full TCOLUMN size
        if len(combined) < core.TCOLUMN:
            combined += b'\x00' * (core.TCOLUMN - len(combined))
        else:
            combined = combined[:core.TCOLUMN]
        
        core.fill(combined)

def create_transition_functions(display):
    """Create transition functions that work with both rows."""
    
    def righttoleft(message: str):
        """Right to left scroll transition."""
        display.scroll_text(message, speed=0.2)
    
    def upnext(message: str):
        """Up next announcement transition."""
        # Flash "UP NEXT"
        display.flash_message("UP NEXT", times=3, on_time=0.3, off_time=0.2)
        time.sleep(0.5)
        # Show the message
        display.scroll_text(message, speed=0.15)
    
    def pop(message: str):
        """Pop transition."""
        display.flash_message(message, times=7, on_time=0.25, off_time=0.25)
        display.clear()
        time.sleep(1)
    
    def typewriter(message: str):
        """Typewriter transition."""
        display.type_text(message, char_delay=0.1)
        time.sleep(2)
        display.clear()
    
    def plain(message: str):
        """Plain scroll transition."""
        display.scroll_text(message)
    
    return {
        'righttoleft': righttoleft,
        'upnext': upnext,
        'pop': pop,
        'typewriter': typewriter,
        'plain': plain
    }

def test_complete_system():
    """Test the complete working system."""
    
    print("=== Testing Complete Working System ===")
    
    display = WorkingFlipdotSystem()
    
    try:
        print("1. Clear display...")
        display.clear()
        time.sleep(2)
        
        print("2. Static text display...")
        display.display_text_static("HELLO WORLD", justify='center')
        time.sleep(3)
        
        print("3. Test patterns...")
        for pattern in ['alternating', 'stripes', 'checkerboard']:
            display.display_pattern(pattern)
            time.sleep(2)
        
        print("4. Flash message...")
        display.flash_message("ALERT", times=3)
        time.sleep(1)
        
        print("5. Typewriter effect...")
        display.type_text("TYPING TEXT")
        time.sleep(2)
        
        print("6. Two line test (experimental)...")
        display.display_two_lines("LINE ONE", "LINE TWO")
        time.sleep(3)
        
        print("7. Scroll text...")
        display.scroll_text("THIS IS A LONG SCROLLING MESSAGE TO TEST BOTH ROWS")
        time.sleep(2)
        
        print("8. Test transitions...")
        transitions = create_transition_functions(display)
        
        transitions['pop']("POP EFFECT")
        transitions['typewriter']("TYPEWRITER")
        transitions['upnext']("FINAL MESSAGE")
        
        print("9. Final clear...")
        display.clear()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def create_playlist_system():
    """Create a playlist system using the working display."""
    
    display = WorkingFlipdotSystem()
    transitions = create_transition_functions(display)
    
    # Sample playlist like your original
    playlist = [
        {"function": transitions['righttoleft'], "parameter": "bioPunk"},
        {"function": transitions['upnext'], "parameter": "WELCOME"},
        {"function": transitions['typewriter'], "parameter": "HELLO WORLD"},
        {"function": transitions['pop'], "parameter": "SYSTEM ONLINE"},
        {"function": display.scroll_text, "parameter": "This is a long message that will scroll across both rows of the display"},
    ]
    
    print("=== Running Playlist ===")
    
    try:
        for i, item in enumerate(playlist):
            print(f"Playing item {i+1}: {item.get('parameter', 'No parameter')}")
            
            if item['parameter']:
                item['function'](item['parameter'])
            else:
                item['function']()
            
            time.sleep(1)  # Pause between items
        
        display.clear()
        print("✅ Playlist completed!")
        
    except KeyboardInterrupt:
        print("\nPlaylist interrupted")
        display.clear()
    except Exception as e:
        print(f"Playlist error: {e}")
        display.clear()

if __name__ == "__main__":
    print("Final Working Flipdot System")
    print("="*40)
    print("Based on your working scrollleft function!")
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'playlist':
        create_playlist_system()
    else:
        test_complete_system()
