#!/usr/bin/env python3
"""
Simple Double Height Test

Test the simple double-height approach that should actually work.
"""

import time
from core.core import working_core, clear

def test_simple_double():
    """Test the simple double-height approach."""
    
    print("=== Simple Double Height Test ===")
    
    test_cases = [
        ("Single: A", lambda: working_core.display_text("A", justify='center', height='single')),
        ("Double: A", lambda: working_core.display_text("A", justify='center', height='double')),
        ("Single: HI", lambda: working_core.display_text("HI", justify='center', height='single')),  
        ("Double: HI", lambda: working_core.display_text("HI", justify='center', height='double')),
        ("Single: TEST", lambda: working_core.display_text("TEST", justify='left', height='single')),
        ("Double: TEST", lambda: working_core.display_text("TEST", justify='left', height='double')),
    ]
    
    for name, test_func in test_cases:
        print(f"\nTesting: {name}")
        clear()
        time.sleep(0.5)
        
        try:
            test_func()
            time.sleep(3)
            
            response = input(f"How does '{name}' look? (describe what you see): ")
            print(f"Result: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    clear()
    print("\nTest completed!")

def test_double_height_comparison():
    """Side-by-side comparison of single vs double height."""
    
    print("\n=== Side-by-Side Comparison ===")
    
    messages = ["A", "HI", "HELLO"]
    
    for msg in messages:
        print(f"\nComparing '{msg}':")
        
        # Single height
        print("  Showing single height...")
        working_core.display_text(msg, justify='center', height='single')
        time.sleep(2)
        
        # Double height  
        print("  Showing double height...")
        working_core.display_text(msg, justify='center', height='double')
        time.sleep(2)
        
        # Ask for comparison
        response = input(f"  Is double-height '{msg}' visibly taller/more prominent? (y/n): ")
        
        if response.lower() == 'y':
            print(f"  ✅ Double height working for '{msg}'")
        else:
            print(f"  ❌ Double height not working for '{msg}'")
        
        clear()
        time.sleep(0.5)

if __name__ == "__main__":
    # Test the simple approach
    test_simple_double()
    
    # Compare single vs double
    test_double_height_comparison()
