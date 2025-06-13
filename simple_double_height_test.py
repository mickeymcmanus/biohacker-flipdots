#!/usr/bin/env python3
"""
Simple Double Height Test

Test double height functionality directly without complex imports.
"""

import time
import sys
import os

# Add the path to find our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.core import (
        working_core, 
        display_text_single, 
        display_text_double, 
        getbytes, 
        getbytes_double,
        scrollleft,
        scrollleft_double,
        clear
    )
    print("✅ Successfully imported double height functions")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Let's try the basic functions...")
    
    try:
        from core.core import working_core, clear
        print("✅ Basic functions imported")
        
        # Test basic functionality
        clear()
        working_core.display_text("SINGLE", height='single')
        time.sleep(3)
        
        working_core.display_text("DOUBLE", height='double')  
        time.sleep(3)
        
        clear()
        print("✅ Basic double height test completed")
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        import traceback
        traceback.print_exc()
    
    sys.exit(1)

def test_double_height():
    """Test double height functionality."""
    
    print("=== Double Height Test ===")
    
    try:
        print("1. Clear display...")
        clear()
        time.sleep(1)
        
        print("2. Single height text...")
        display_text_single("HELLO", justify='center')
        time.sleep(3)
        
        print("3. Double height text...")
        display_text_double("HELLO", justify='center') 
        time.sleep(3)
        
        print("4. Single height scroll...")
        msg_single = getbytes("SINGLE HEIGHT SCROLL")
        scrollleft(msg_single, t=0.2)
        time.sleep(1)
        
        print("5. Double height scroll...")
        msg_double = getbytes_double("DOUBLE HEIGHT")
        scrollleft_double(msg_double, t=0.2)
        time.sleep(1)
        
        print("6. Comparison...")
        for i in range(3):
            display_text_single("SINGLE", justify='center')
            time.sleep(1)
            display_text_double("DOUBLE", justify='center')
            time.sleep(1)
        
        clear()
        print("✅ Double height test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_double_height()
