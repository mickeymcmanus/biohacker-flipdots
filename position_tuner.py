#!/usr/bin/env python3
"""
Position Fine-Tuner

Test different positions to find the perfect spot for top-row text.
"""

from core import core
import time

def test_positions():
    """Test different positions for 'HELLO' to find the perfect spot."""
    
    message = "HELLO"
    text_bytes = core.getbytes(message.upper())
    padded_message = core.TCOLUMN * core.dict['space'] + text_bytes + core.TCOLUMN * core.dict['space']
    
    # Test positions around 105
    positions_to_test = [100, 101, 102, 103, 104, 105, 106, 107, 108]
    
    print(f"Testing positions for '{message}' to find perfect top-row placement...")
    
    for pos in positions_to_test:
        print(f"Testing position {pos}...")
        chunk = padded_message[pos:pos + core.TCOLUMN]
        core.fill(chunk)
        
        response = input(f"Position {pos}: How does '{message}' look? (good/missing-left/too-right/split): ")
        
        if response == "good":
            print(f"✅ Perfect position found: {pos}")
            return pos
        elif response == "missing-left":
            print(f"Need to move left (try lower number)")
        elif response == "too-right":
            print(f"Need to move right (try higher number)")
        elif response == "split":
            print(f"Still split across rows")
        
        time.sleep(0.5)
    
    print("Test completed. Which position looked best?")
    best_pos = input("Enter the best position number: ")
    return int(best_pos) if best_pos.isdigit() else 105

if __name__ == "__main__":
    best_position = test_positions()
    print(f"\nRecommended position: {best_position}")
    print(f"Update the code to use position {best_position} for top-row text.")
