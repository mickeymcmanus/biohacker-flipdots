#!/usr/bin/env python3
"""
Row Command Finder

Systematically test different commands to find what controls the bottom row.
"""

import serial
import time

def test_all_row_commands():
    """Test every possible row command to find what controls bottom row."""
    
    print("=== Systematic Row Command Test ===")
    print("Watch your display carefully and note which commands affect the bottom row!")
    
    ser = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400)
    
    try:
        # First, clear everything and establish baseline
        print("\n0. Clearing with known working top row command...")
        ser.write(b'\x81')  # RESET
        ser.write(b'\x82')  # ROW1 (we know this works)
        ser.write(b'\x00' * 30)
        time.sleep(2)
        
        # Test commands from 0x80 to 0x90
        test_commands = [
            0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x90
        ]
        
        for i, cmd in enumerate(test_commands):
            print(f"\n{i+1}. Testing command 0x{cmd:02X} for bottom row...")
            
            # First put a pattern on top row so we can see difference
            ser.write(b'\x81')  # RESET
            ser.write(b'\x82')  # Known working ROW1
            ser.write(b'\x55' * 30)  # Pattern on top
            
            # Now test the command for bottom row
            ser.write(b'\x81')  # RESET
            ser.write(bytes([cmd]))  # Test command
            ser.write(b'\xAA' * 30)  # Different pattern
            
            print(f"   Sent: RESET + 0x{cmd:02X} + pattern")
            print(f"   Look at display - does bottom row show pattern?")
            
            # Wait for user input to continue
            input("   Press Enter to try next command...")
            
        # Test double commands (like your original uses \x81\x81)
        print("\n=== Testing Double Commands ===")
        
        double_commands = [
            (0x81, 0x83), (0x81, 0x84), (0x82, 0x83), (0x82, 0x84),
            (0x83, 0x83), (0x84, 0x84), (0x85, 0x85)
        ]
        
        for i, (cmd1, cmd2) in enumerate(double_commands):
            print(f"\n{i+1}. Testing double command 0x{cmd1:02X} 0x{cmd2:02X}...")
            
            # Top row first
            ser.write(b'\x81\x82')  # Known working
            ser.write(b'\x33' * 30)  # Pattern
            
            # Test double command for bottom
            ser.write(bytes([cmd1, cmd2]))
            ser.write(b'\xCC' * 30)  # Different pattern
            
            print(f"   Sent: 0x{cmd1:02X} 0x{cmd2:02X} + pattern")
            print(f"   Look at display - does bottom row show pattern?")
            
            input("   Press Enter to try next command...")
            
        # Test positioning commands (like your original diagnostic showed)
        print("\n=== Testing Position Commands ===")
        
        # Your original diagnostic showed commands > 128 were position commands
        position_commands = [129, 130, 131, 132, 133, 134, 135]
        
        for cmd in position_commands:
            print(f"\nTesting position command {cmd} (0x{cmd:02X})...")
            
            ser.write(b'\x81')  # RESET
            ser.write(bytes([cmd]))  # Position command
            ser.write(b'\xFF' * 10)  # Bright pattern
            
            print(f"   Sent: RESET + {cmd} + pattern")
            print(f"   Look at display - what happens?")
            
            input("   Press Enter to try next command...")
            
        print("\n=== Final Clear Test ===")
        ser.write(b'\x81\x82')
        ser.write(b'\x00' * 30)
        
    except Exception as e:
        print(f"Test error: {e}")
        
    finally:
        ser.close()

def test_your_original_commands():
    """Test the exact commands from your original diagnostic output."""
    
    print("\n=== Testing Your Original Commands ===")
    
    ser = serial.Serial('/dev/tty.usbserial-A3000lDq', 38400)
    
    try:
        print("Your original clear() sends:")
        print("  - 8181 (2 bytes) + 105 zero bytes")  
        print("  - 8182 (2 bytes) + 105 zero bytes")
        print()
        print("Let's test this exactly but with 30 bytes...")
        
        # Test exact original sequence
        print("1. Testing 0x81 0x81 + data...")
        ser.write(b'\x81\x81')
        ser.write(b'\xFF' * 30)  # Bright pattern
        time.sleep(2)
        
        print("2. Testing 0x81 0x82 + data...")
        ser.write(b'\x81\x82')  
        ser.write(b'\x0F' * 30)  # Different pattern
        time.sleep(3)
        
        print("Did you see two different patterns?")
        input("Press Enter to continue...")
        
        # Clear test
        print("3. Testing clear with original sequence...")
        ser.write(b'\x81\x81')
        ser.write(b'\x00' * 30)
        ser.write(b'\x81\x82')
        ser.write(b'\x00' * 30)
        time.sleep(2)
        
        print("Did both rows clear?")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        ser.close()

if __name__ == "__main__":
    print("Row Command Finder")
    print("="*40)
    print("This will systematically test commands to find what controls your bottom row.")
    print("Watch your display carefully and note which commands work!")
    print()
    
    choice = input("Test (1) systematic commands or (2) your original commands? [1/2]: ")
    
    if choice == "2":
        test_your_original_commands()
    else:
        test_all_row_commands()
    
    print("\nDone! Which command(s) successfully controlled the bottom row?")
