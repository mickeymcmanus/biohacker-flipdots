#!/usr/bin/env python3
"""
Direct Protocol Test - Use original core.py to understand the exact protocol
"""

import time
from core import core

def test_original_step_by_step():
    """Test your original core step by step to see exact commands."""
    
    print("=== Testing Original Core Step by Step ===")
    
    # Test 1: Clear display
    print("1. Clearing display...")
    core.clear()
    time.sleep(2)
    
    # Test 2: Simple message that fits
    print("2. Simple message: 'HI'")
    core.flip("HI")
    time.sleep(3)
    
    # Test 3: Longer message
    print("3. Longer message: 'HELLO WORLD'")
    core.flip("HELLO WORLD")  
    time.sleep(3)
    
    # Test 4: Scrolling
    print("4. Scrolling message")
    message_bytes = core.getbytes("SCROLL TEST")
    print(f"   Message bytes length: {len(message_bytes)}")
    core.scrollleft(message_bytes, t=0.2)
    time.sleep(2)
    
    # Test 5: Fill with pattern
    print("5. Fill with test pattern")
    test_pattern = b'\x7F\x00\x7F\x00' * 8  # Alternating pattern
    core.fill(test_pattern)
    time.sleep(3)
    
    print("6. Final clear")
    core.clear()

def analyze_original_commands():
    """Analyze what your original core actually sends by patching the serial write."""
    
    print("\n=== Analyzing Original Commands ===")
    
    # Store original write method
    original_write = core.ser_main.write
    sent_commands = []
    
    def capture_write(data):
        """Capture what gets sent to serial."""
        sent_commands.append(data)
        print(f"SERIAL SEND: {data.hex()} ({len(data)} bytes)")
        return original_write(data)
    
    # Patch the write method
    core.ser_main.write = capture_write
    
    try:
        print("\nTesting core.clear():")
        sent_commands.clear()
        core.clear()
        
        print(f"\nTesting core.flip('HI'):")
        sent_commands.clear()
        core.flip("HI")
        
        print(f"\nTesting simple fill:")
        sent_commands.clear()
        core.fill(b'\x7F\x00\x7F\x00')
        
    finally:
        # Restore original write method
        core.ser_main.write = original_write
    
    return sent_commands

def test_manual_protocol():
    """Test sending commands manually to understand the protocol."""
    
    print("\n=== Manual Protocol Test ===")
    
    import serial
    ser = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400)
    
    try:
        print("1. Manual clear...")
        ser.write(b'\x81')  # RESET
        ser.write(b'\x82')  # ROW1
        ser.write(b'\x00' * 30)  # Clear 30 columns
        time.sleep(1)
        
        print("2. Manual simple pattern...")
        ser.write(b'\x81')  # RESET
        ser.write(b'\x82')  # ROW1
        # Simple alternating pattern
        for i in range(30):
            if i % 2 == 0:
                ser.write(b'\x7F')  # All dots on
            else:
                ser.write(b'\x00')  # All dots off
        time.sleep(3)
        
        print("3. Manual text 'HI'...")
        ser.write(b'\x81')  # RESET  
        ser.write(b'\x82')  # ROW1
        
        # Send 'H' character bytes from original dict
        h_bytes = core.dict['H']  # Should be b'\x7f\x08\x08\x08\x7f'
        ser.write(h_bytes)
        
        # Send space
        ser.write(core.dict['space'])  # Should be b'\x00'
        
        # Send 'I' character bytes
        i_bytes = core.dict['I']  # Should be b'\x7f'
        ser.write(i_bytes)
        
        # Pad rest with zeros
        remaining = 30 - len(h_bytes) - len(core.dict['space']) - len(i_bytes)
        ser.write(b'\x00' * remaining)
        
        time.sleep(3)
        
        print("4. Manual clear...")
        ser.write(b'\x81\x82')
        ser.write(b'\x00' * 30)
        
    finally:
        ser.close()

if __name__ == "__main__":
    print("Direct Protocol Testing")
    print("="*40)
    
    try:
        # First test that original works
        test_original_step_by_step()
        
        # Then analyze what it sends
        analyze_original_commands() 
        
        # Finally test manual protocol
        test_manual_protocol()
        
    except KeyboardInterrupt:
        print("\nTest interrupted")
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()
