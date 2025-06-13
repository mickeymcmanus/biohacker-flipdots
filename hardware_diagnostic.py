#!/usr/bin/env python3
"""
Hardware Diagnostic Test

Test if the bottom row hardware is working at all using your original system.
"""

from core import core
import time

def test_original_system_bottom_row():
    """Test if your original system can display on bottom row."""
    
    print("=== Testing Original System for Bottom Row ===")
    print("This will test if your original core.py can display anything on the bottom row.")
    
    try:
        # Test 1: Use original flip() with a long message
        print("\n1. Testing original flip() with long message...")
        print("   (Should overflow to bottom row if it works)")
        
        # Your original flip() switches to ROW2 when i > 15
        long_message = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        core.flip(long_message)
        time.sleep(5)
        
        print("   Did you see any text on the bottom row?")
        response = input("   (y/n): ").lower()
        
        if response == 'y':
            print("   ✅ Bottom row hardware works with original system!")
            return True
        else:
            print("   ❌ No bottom row display with original system")
        
        # Test 2: Force original system to use ROW2
        print("\n2. Testing original system ROW2 directly...")
        
        # Clear first
        core.clear()
        time.sleep(1)
        
        # Try to manually trigger ROW2 logic in original flip()
        # The original code switches to ROW2 when i > 15
        very_long_message = "1234567890123456789012345678901234567890"
        core.flip(very_long_message)
        time.sleep(5)
        
        print("   Did you see any text on the bottom row now?")
        response = input("   (y/n): ").lower()
        
        if response == 'y':
            print("   ✅ Bottom row works with very long message!")
            return True
        
        # Test 3: Check original constants
        print(f"\n3. Checking original system constants...")
        print(f"   TROW: {core.TROW}")
        print(f"   TCOLUMN: {core.TCOLUMN}")
        print(f"   ROW_BREAK: {getattr(core, 'ROW_BREAK', 'Not defined')}")
        
        if core.TROW == 7:
            print("   ⚠️  Original system thinks display is only 7 pixels high!")
            print("   This might explain why bottom row doesn't work.")
        
        # Test 4: Try original fill() with lots of data
        print("\n4. Testing original fill() with 105 bytes of data...")
        
        # Create 105 bytes of alternating pattern
        pattern = b''
        for i in range(105):
            if i < 30:
                pattern += b'\xFF'  # First 30 bright
            elif i < 60:
                pattern += b'\x0F'  # Next 30 dim
            else:
                pattern += b'\x00'  # Rest off
                
        core.fill(pattern)
        time.sleep(5)
        
        print("   Did you see the pattern change from bright to dim across the display?")
        response = input("   (y/n): ").lower()
        
        if response == 'y':
            print("   ✅ Original fill() can send different data to different parts!")
        
        # Test 5: Clear and check
        print("\n5. Final clear test with original system...")
        core.clear()
        time.sleep(2)
        
        print("   Did the ENTIRE display clear (both top and bottom)?")
        response = input("   (y/n): ").lower()
        
        if response == 'y':
            print("   ✅ Original clear works on whole display!")
            return True
        else:
            print("   ❌ Original clear only clears top row")
            return False
            
    except Exception as e:
        print(f"Error testing original system: {e}")
        return False

def analyze_display_wiring():
    """Help analyze if it's a wiring/hardware issue."""
    
    print("\n=== Display Hardware Analysis ===")
    
    print("Let's check your display setup:")
    print("1. You have 2 rows of 6 modules each (2×6 configuration)")
    print("2. Each module is 5×7 pixels")  
    print("3. Total display should be 30×14 pixels")
    print()
    
    print("Questions about your hardware:")
    print()
    
    # Check physical wiring
    response = input("1. Are both rows of modules physically connected to the same controller? (y/n): ").lower()
    if response == 'n':
        print("   ⚠️  This might be the issue! Both rows need to connect to the same controller.")
    
    # Check power
    response = input("2. Do you see any LEDs or indicators on the bottom row modules? (y/n): ").lower()
    if response == 'n':
        print("   ⚠️  Bottom row modules might not be getting power.")
    
    # Check addressing
    response = input("3. Are the bottom row modules configured as a continuation of the top row? (y/n): ").lower()
    if response == 'n':
        print("   ⚠️  Bottom row might need different addressing configuration.")
    
    # Check original working state
    response = input("4. Did the bottom row EVER work with your original system? (y/n): ").lower()
    if response == 'n':
        print("   ⚠️  This suggests a hardware or configuration issue, not a software problem.")
        print("   The bottom row may need:")
        print("   - Different wiring")
        print("   - Hardware jumper settings")
        print("   - Module addressing configuration")
    else:
        print("   ✅ Bottom row worked before, so it's likely a software protocol issue.")

def check_module_addressing():
    """Check if modules need individual addressing."""
    
    print("\n=== Module Addressing Test ===")
    print("Some flipdot displays require individual module addressing.")
    print("Let's test if your modules need specific addresses...")
    
    import serial
    
    ser = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400)
    
    try:
        # Test addressing individual modules
        print("\nTesting individual module addresses...")
        
        # Common flipdot module addresses
        module_addresses = [0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87]
        
        for addr in module_addresses:
            print(f"Testing module address 0x{addr:02X}...")
            
            # Try addressing specific module
            ser.write(bytes([addr]))  # Module address
            ser.write(b'\xFF' * 7)    # Full column pattern
            time.sleep(1)
            
            print(f"Did any part of the display light up with address 0x{addr:02X}?")
            response = input("(y/n): ").lower()
            
            if response == 'y':
                print(f"   ✅ Address 0x{addr:02X} controls some part of the display!")
            
            # Clear
            ser.write(bytes([addr]))
            ser.write(b'\x00' * 7)
            time.sleep(0.5)
    
    finally:
        ser.close()

if __name__ == "__main__":
    print("Hardware Diagnostic Test")
    print("="*40)
    print("This will help determine if the issue is hardware or software.")
    print()
    
    # Test if original system can use bottom row
    bottom_row_works = test_original_system_bottom_row()
    
    if not bottom_row_works:
        print("\n" + "="*40)
        analyze_display_wiring()
        
        print("\n" + "="*40)  
        check_module_addressing()
    
    print("\n" + "="*40)
    print("SUMMARY:")
    
    if bottom_row_works:
        print("✅ Bottom row hardware works - this is a software protocol issue")
        print("   We need to figure out the right commands to control it")
    else:
        print("❌ Bottom row doesn't respond to original system either")
        print("   This suggests:")
        print("   1. Hardware/wiring issue")
        print("   2. Module configuration issue") 
        print("   3. Different addressing scheme needed")
        print()
        print("Check your flipdot display documentation for:")
        print("   - Module addressing requirements")
        print("   - Hardware jumper settings")
        print("   - Wiring configuration for multi-row displays")
