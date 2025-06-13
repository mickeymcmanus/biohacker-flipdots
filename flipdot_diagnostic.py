#!/usr/bin/env python3
"""
Flipdot Diagnostic Tool

This tool helps debug the serial communication with your flipdot display
by using the exact same protocol as your working core.py file.
"""

import serial
import time
from core import core  # Import your working core module

def test_original_vs_new():
    """Test both your original system and the new system side by side."""
    
    print("=== Testing Original Core Module ===")
    
    # Test with your original core
    try:
        print("1. Testing original core.flip() function...")
        core.flip("HELLO")
        time.sleep(3)
        
        print("2. Testing original core.clear()...")
        core.clear()
        time.sleep(2)
        
        print("3. Testing original scrolling...")
        message_bytes = core.getbytes("SCROLL TEST")
        core.scrollleft(message_bytes, t=0.2)
        time.sleep(2)
        
        print("Original core works!")
        
    except Exception as e:
        print(f"Original core error: {e}")
    
    print("\n=== Now Testing New System ===")
    
    # Test new system with same data
    try:
        from core.reconfigurable_flipdot import create_display
        display = create_display("current", port="/dev/tty.usbserial-A3000lDq")
        
        print("1. Testing new system clear...")
        display.clear()
        time.sleep(2)
        
        print("2. Testing raw serial commands like original...")
        # Try to send the same commands as original
        display.serial.write(b'\x81\x82')  # RESET + ROW1 like original
        display.serial.write(core.getbytes("TEST")[:30])  # Use original character encoding
        time.sleep(3)
        
        display.clear()
        
    except Exception as e:
        print(f"New system error: {e}")

def analyze_original_protocol():
    """Analyze what your original core.py actually sends."""
    
    print("=== Analyzing Original Protocol ===")
    
    # Look at what your original system sends for a simple message
    test_message = "HI"
    
    print(f"Original getbytes('{test_message}'):")
    original_bytes = core.getbytes(test_message)
    print(f"Length: {len(original_bytes)}")
    print(f"Hex: {original_bytes.hex()}")
    print(f"Bytes: {[hex(b) for b in original_bytes]}")
    
    print(f"\nOriginal character dictionary entries:")
    for char in test_message:
        if char in core.dict:
            char_bytes = core.dict[char]
            print(f"'{char}': {char_bytes.hex()} ({[hex(b) for b in char_bytes]})")
    
    print(f"\nConstants from original:")
    print(f"TROW: {core.TROW}")
    print(f"TCOLUMN: {core.TCOLUMN}")
    print(f"ROW_BREAK: {getattr(core, 'ROW_BREAK', 'Not defined')}")

def test_minimal_display():
    """Test the most basic display functionality."""
    
    print("=== Minimal Display Test ===")
    
    # Use your original working serial connection
    try:
        ser = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400)
        
        print("1. Sending reset command...")
        ser.write(b'\x81')  # Reset from your original
        time.sleep(0.1)
        
        print("2. Sending row 1 command...")
        ser.write(b'\x82')  # ROW1 from your original  
        time.sleep(0.1)
        
        print("3. Sending simple pattern...")
        # Send a simple pattern - alternating columns
        for i in range(30):  # Your display width
            if i % 2 == 0:
                ser.write(b'\x7F')  # All bits on (should show as column of dots)
            else:
                ser.write(b'\x00')  # All bits off
        
        time.sleep(3)
        
        print("4. Clearing...")
        ser.write(b'\x81\x82')  # Reset + Row1
        ser.write(b'\x00' * 30)  # Clear top row
        ser.write(b'\x83')  # Row2
        ser.write(b'\x00' * 30)  # Clear bottom row
        
        ser.close()
        
    except Exception as e:
        print(f"Minimal test error: {e}")

def compare_configurations():
    """Compare original vs new configuration values."""
    
    print("=== Configuration Comparison ===")
    
    # Original values
    print("Original configuration:")
    print(f"  TROW: {core.TROW}")
    print(f"  TCOLUMN: {core.TCOLUMN}")
    
    # New system values  
    from core.reconfigurable_flipdot import DISPLAY_CONFIGS
    current_config = DISPLAY_CONFIGS["current"]
    
    print(f"\nNew 'current' configuration:")
    print(f"  total_height: {current_config.total_height}")
    print(f"  total_width: {current_config.total_width}")
    print(f"  modules_high: {current_config.modules_high}")
    print(f"  modules_wide: {current_config.modules_wide}")
    
    print(f"\nMismatch analysis:")
    if core.TROW != current_config.total_height:
        print(f"  HEIGHT MISMATCH: Original={core.TROW}, New={current_config.total_height}")
    if core.TCOLUMN != current_config.total_width:
        print(f"  WIDTH MISMATCH: Original={core.TCOLUMN}, New={current_config.total_width}")

if __name__ == "__main__":
    print("Flipdot Display Diagnostic Tool")
    print("="*40)
    
    try:
        analyze_original_protocol()
        print("\n" + "="*40)
        
        compare_configurations()
        print("\n" + "="*40)
        
        test_minimal_display()
        print("\n" + "="*40)
        
        test_original_vs_new()
        
    except KeyboardInterrupt:
        print("\nDiagnostic interrupted")
    except Exception as e:
        print(f"Diagnostic error: {e}")
        import traceback
        traceback.print_exc()
