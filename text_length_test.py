#!/usr/bin/env python3
"""
Text Length Analyzer

Check exactly how many bytes different messages take up.
"""

from core import core

def analyze_text_lengths():
    """Analyze byte lengths of various text messages."""
    
    test_messages = [
        "HI",
        "HELLO", 
        "HELLO WORLD",
        "ALERT",
        "TYPING TEXT",
        "A",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "THE QUICK BROWN FOX"
    ]
    
    print("Text Length Analysis")
    print("="*50)
    
    for msg in test_messages:
        text_bytes = core.getbytes(msg.upper())
        print(f"'{msg}' = {len(text_bytes)} bytes")
        
        # Show which row(s) it would use
        if len(text_bytes) <= 30:
            print(f"  -> Fits on single row (top row: bytes 75-{75 + len(text_bytes) - 1})")
        elif len(text_bytes) <= 60:
            print(f"  -> Needs both rows")
            print(f"     Bottom: bytes 0-29 (30 bytes)")
            print(f"     Top: bytes 75-{75 + (len(text_bytes) - 30) - 1} ({len(text_bytes) - 30} bytes)")
        else:
            print(f"  -> Too long! Needs truncation")
        
        print()

def test_specific_positioning():
    """Test specific positioning to understand the layout."""
    
    print("Specific Positioning Test")
    print("="*50)
    
    from final_working_system import WorkingFlipdotSystem
    
    display = WorkingFlipdotSystem()
    
    # Test messages of different lengths
    test_cases = [
        ("HI", "Very short"),
        ("HELLO", "Short"), 
        ("HELLO WORLD", "Medium"),
        ("THIS IS A LONGER MESSAGE", "Long")
    ]
    
    for msg, description in test_cases:
        print(f"\nTesting: '{msg}' ({description})")
        text_bytes = core.getbytes(msg.upper())
        print(f"Byte length: {len(text_bytes)}")
        
        display.display_text_static(msg, justify='left')
        
        response = input(f"Where does '{msg}' appear? (describe position): ")
        print(f"User sees: {response}")
        
        time.sleep(1)

if __name__ == "__main__":
    import time
    
    # First analyze lengths
    analyze_text_lengths()
    
    print("\n" + "="*50)
    
    # Then test positioning if user wants
    response = input("Test positioning on actual display? (y/n): ")
    if response.lower() == 'y':
        test_specific_positioning()
