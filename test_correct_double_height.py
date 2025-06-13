#!/usr/bin/env python3
"""
Test Correct Double Height

Now that we know the correct mapping, test proper double-height text.
"""

import time
from core.core import working_core, clear

def test_correct_double_height():
    """Test double height with the correct display mapping."""
    
    print("=== Testing Correct Double Height ===")
    
    test_cases = [
        ("A", "Single character"),
        ("HI", "Two characters"),
        ("TEST", "Four characters"),
        ("HELLO", "Five characters")
    ]
    
    for message, description in test_cases:
        print(f"\nTesting {description}: '{message}'")
        
        # Single height
        print("  Single height...")
        working_core.display_text(message, justify='center', height='single')
        time.sleep(2)
        
        # Double height with correct mapping
        print("  Double height...")
        working_core.display_text(message, justify='center', height='double')
        time.sleep(3)
        
        response = input(f"  Does '{message}' appear on BOTH top and bottom rows? (y/n): ")
        
        if response.lower() == 'y':
            print(f"  ✅ Double height working for '{message}'!")
        else:
            print(f"  ❌ Double height still not working for '{message}'")
            detail = input(f"    Describe what you see: ")
            print(f"    Details: {detail}")
        
        clear()
        time.sleep(1)

def test_double_height_justification():
    """Test different justifications for double height."""
    
    print("\n=== Testing Double Height Justification ===")
    
    justifications = ['left', 'center', 'right']
    message = "TEST"
    
    for justify in justifications:
        print(f"\nTesting {justify} justification:")
        
        working_core.display_text(message, justify=justify, height='double')
        time.sleep(3)
        
        response = input(f"  Is '{message}' {justify}-justified on both rows? (y/n): ")
        print(f"  {justify.capitalize()} justification: {response}")
        
        clear()
        time.sleep(1)

def compare_single_vs_double():
    """Direct comparison of single vs double height."""
    
    print("\n=== Single vs Double Comparison ===")
    
    message = "HI"
    
    for i in range(3):
        print(f"\nComparison {i+1}:")
        
        print("  Showing single height...")
        working_core.display_text(message, justify='center', height='single')
        time.sleep(2)
        
        print("  Now showing double height...")
        working_core.display_text(message, justify='center', height='double')
        time.sleep(2)
        
        response = input("  Is the difference clearly visible? (y/n): ")
        
        if response.lower() == 'y':
            print("  ✅ Double height is clearly more prominent!")
            break
        else:
            print("  ❌ Still not seeing the difference...")
        
        clear()
        time.sleep(1)

if __name__ == "__main__":
    # Test with correct mapping
    test_correct_double_height()
    
    # Test different justifications
    test_double_height_justification()
    
    # Direct comparison
    compare_single_vs_double()
    
    print("\n=== Test Complete ===")
    clear()
