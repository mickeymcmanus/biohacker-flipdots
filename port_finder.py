#!/usr/bin/env python3
"""
Port Finder - Manual detection and testing of serial ports
"""

import serial
import serial.tools.list_ports
import time

def list_all_ports():
    """List all available serial ports with details."""
    print("All available serial ports:")
    print("-" * 60)
    
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found!")
        return []
    
    for i, port in enumerate(ports):
        print(f"{i+1}. {port.device}")
        print(f"   Description: {port.description}")
        print(f"   Hardware ID: {port.hwid}")
        if hasattr(port, 'manufacturer') and port.manufacturer:
            print(f"   Manufacturer: {port.manufacturer}")
        print()
    
    return [port.device for port in ports]

def test_port(port_name, baud=38400):
    """Test a specific port."""
    try:
        print(f"Testing {port_name} at {baud} baud...")
        with serial.Serial(port_name, baud, timeout=2) as ser:
            # Try to send a simple command
            ser.write(b'\x81')  # Reset command
            time.sleep(0.1)
            ser.write(b'\x00' * 10)  # Some null bytes
            print(f"✅ {port_name} - Connection successful!")
            return True
    except serial.SerialException as e:
        print(f"❌ {port_name} - Serial error: {e}")
    except PermissionError as e:
        print(f"❌ {port_name} - Permission denied: {e}")
        print("   Try: sudo usermod -a -G dialout $USER")
        print("   Then log out and back in")
    except Exception as e:
        print(f"❌ {port_name} - Other error: {e}")
    
    return False

def interactive_port_selection():
    """Interactive port selection and testing."""
    available_ports = list_all_ports()
    
    if not available_ports:
        return None
    
    while True:
        try:
            choice = input(f"\nEnter port number (1-{len(available_ports)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            port_index = int(choice) - 1
            if 0 <= port_index < len(available_ports):
                selected_port = available_ports[port_index]
                
                if test_port(selected_port):
                    return selected_port
                else:
                    retry = input("Port test failed. Try another? (y/n): ").strip().lower()
                    if retry != 'y':
                        return None
            else:
                print("Invalid selection!")
                
        except ValueError:
            print("Please enter a valid number!")

def main():
    """Main function for port finding."""
    print("Flipdot Display Port Finder")
    print("=" * 40)
    
    # First, try automatic detection of likely candidates
    print("Scanning for likely flipdot display ports...")
    
    ports = serial.tools.list_ports.comports()
    candidates = []
    
    for port in ports:
        device = port.device
        desc = port.description.lower() if port.description else ""
        
        # Linux USB serial patterns
        if any(pattern in device for pattern in ["/dev/ttyUSB", "/dev/ttyACM"]):
            candidates.append(device)
        # Check description for common USB-serial chips
        elif any(keyword in desc for keyword in ["ftdi", "arduino", "usb", "serial", "ch340", "cp210"]):
            candidates.append(device)
    
    if candidates:
        print(f"\nFound {len(candidates)} potential flipdot ports:")
        for port in candidates:
            print(f"  - {port}")
        
        print("\nTesting candidates...")
        for port in candidates:
            if test_port(port):
                print(f"\n🎉 SUCCESS! Your flipdot display is likely on: {port}")
                print(f"Update your core.py to use: '{port}'")
                return port
    
    print("\nAutomatic detection failed. Manual selection:")
    selected_port = interactive_port_selection()
    
    if selected_port:
        print(f"\n🎉 Selected port: {selected_port}")
        print(f"Update your core.py to use: '{selected_port}'")
        
        # Generate the code snippet
        print("\nCode snippet for your core.py:")
        print("-" * 30)
        print(f"# Replace the port in your WorkingFlipdotCore.__init__ method:")
        print(f"def __init__(self, port: str = '{selected_port}', baud: int = 38400):")
        print("-" * 30)
    
    return selected_port

if __name__ == "__main__":
    main()