#!/usr/bin/env python3
"""
Enhanced Transitions Module with Double Height Text Support

Updated transitions that include both single-height and double-height text options.
"""

import time
import random
import sys
import os

# Add the parent directory to the path so we can import from core
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

try:
    from core.core import working_core, getbytes, scrollleft, fillfrombottomup, fillfromtopdown, erasefromtopdown, erasefrombottomup, fillrandomorder, eraserandomorder, clear
    print("✅ Enhanced transitions: Found core.core module")
except ImportError as e:
    print(f"❌ Enhanced transitions: Could not import from core.core: {e}")
    # Fallback if core is in same directory level
    try:
        from core import working_core, getbytes, scrollleft, fillfrombottomup, fillfromtopdown, erasefromtopdown, erasefrombottomup, fillrandomorder, eraserandomorder, clear
        print("✅ Enhanced transitions: Found core module (alternate path)")
    except ImportError as e2:
        print(f"❌ Enhanced transitions: Could not import core: {e2}")
        raise

# Import the double-height functions
try:
    from core.double_height_text import (
        display_double_height_text, 
        scroll_double_height_left, 
        typewriter_double_height,
        get_double_height_bytes
    )
    print("✅ Enhanced transitions: Found double_height_text module")
except ImportError as e:
    print(f"❌ Enhanced transitions: Could not import from core.double_height_text: {e}")
    print("Make sure double_height_text.py is in the core/ folder")
    # Try fallback
    try:
        from double_height_text import (
            display_double_height_text, 
            scroll_double_height_left, 
            typewriter_double_height,
            get_double_height_bytes
        )
        print("✅ Enhanced transitions: Found double_height_text (alternate path)")
    except ImportError as e2:
        print(f"❌ Enhanced transitions: Could not import double_height_text: {e2}")
        raise

# Original single-height transitions (unchanged)
def upnext(message: str):
    """Up next announcement with flashing."""
    for j in range(3):
        for i in range(5):
            working_core.display_text("UP NEXT", justify='center')
            time.sleep(0.25)
            clear()
            time.sleep(0.2)
            working_core.display_text("UP NEXT", justify='center')
            time.sleep(0.1)
            clear()
            time.sleep(0.2)
        
        if j == 2:
            scrollleft(getbytes(message), t=0.15, d=3)
        else:
            msg_bytes = getbytes(message)
            scrollleft(msg_bytes, t=0.15, d=3)

def righttoleft(message: str):
    """Simple right to left scroll."""
    msg_bytes = getbytes(message)
    scrollleft(msg_bytes, t=0.2)

def pop(message: str):
    """Flashing pop effect."""
    clear()
    for i in range(7):
        working_core.display_text(message, justify='center')
        time.sleep(0.25)
        clear()
        time.sleep(0.25)
    clear()
    time.sleep(1)

def magichat(message: str):
    """Magic hat effect with multi-screen support."""
    long_string = message
    screens = []
    more = True
    
    while more:
        if len(long_string) <= 21:
            screens.append(long_string)
            more = False
            break
        
        for i in range(21, 0, -1):
            if long_string[i] == " ":
                test_bytes = getbytes(long_string[:i])
                if len(test_bytes) < 60:
                    screens.append(long_string[:i])
                    long_string = long_string[i+1:]
                    break
    
    for screen in screens:
        msg_bytes = getbytes(screen)
        fillfrombottomup(msg_bytes, t=0.3)
        time.sleep(1)
        if screen != screens[-1]:
            erasefromtopdown(msg_bytes, t=0.2)

def typewriter(message: str):
    """Typewriter effect."""
    for i in range(1, len(message) + 1):
        partial = message[:i]
        working_core.display_text(partial, justify='left')
        time.sleep(0.1)
    time.sleep(2)

# NEW: Double-height transitions
def double_height_plain(message: str):
    """Plain double-height text display."""
    display_double_height_text(working_core, message, justify='center')
    time.sleep(3)

def double_height_scroll(message: str):
    """Scrolling double-height text."""
    scroll_double_height_left(working_core, message, t=0.2)

def double_height_typewriter(message: str):
    """Typewriter double-height text."""
    typewriter_double_height(working_core, message, char_delay=0.3)
    time.sleep(2)

def double_height_pop(message: str):
    """Double-height flashing pop effect."""
    clear()
    for i in range(5):
        display_double_height_text(working_core, message, justify='center')
        time.sleep(0.3)
        clear()
        time.sleep(0.3)
    clear()
    time.sleep(1)

def double_height_upnext(message: str):
    """Double-height up next announcement."""
    # Flash "UP NEXT" in double height
    for i in range(3):
        display_double_height_text(working_core, "UP NEXT", justify='center')
        time.sleep(0.4)
        clear()
        time.sleep(0.3)
    
    # Show the message
    scroll_double_height_left(working_core, message, t=0.15)

def double_height_magic_reveal(message: str):
    """Double-height magic reveal effect - builds from bottom up using correct buffer mapping."""
    top_bytes, bottom_bytes = get_double_height_bytes(message)
    
    # Calculate centering
    text_width = len(top_bytes)
    padding = max(0, (30 - text_width) // 2)
    
    # Build the effect with bitmasks
    bitmask_sequence = [1, 3, 7, 15, 31, 63, 127]  # Progressive reveal
    
    for mask in bitmask_sequence:
        # Create display buffer with correct mapping
        display_buffer = [0] * 105
        
        # Apply mask and fill top row (positions 0-29)
        for i in range(min(30, len(top_bytes))):
            col_pos = padding + i
            if col_pos < 30:
                display_buffer[col_pos] = top_bytes[i] & mask
        
        # Apply mask and fill bottom row (positions 75-104)
        for i in range(min(30, len(bottom_bytes))):
            col_pos = padding + i
            if col_pos < 30:
                display_buffer[75 + col_pos] = bottom_bytes[i] & mask
        
        working_core.fill(bytes(display_buffer))
        time.sleep(0.3)
    
    time.sleep(2)

def double_height_wave(message: str):
    """Double-height wave effect - text appears to wave using correct buffer mapping."""
    base_top, base_bottom = get_double_height_bytes(message)
    text_width = len(base_top)
    padding = max(0, (30 - text_width) // 2)
    
    # Create wave effect by shifting bits
    for wave_cycle in range(3):
        for shift in range(4):
            display_buffer = [0] * 105
            
            if shift == 0:
                # Normal position
                wave_top = base_top
                wave_bottom = base_bottom
            elif shift == 1:
                # Shift up - move some bits from bottom to top
                wave_top = bytes([(b << 1) & 127 for b in base_top])
                wave_bottom = bytes([((b << 1) & 127) | ((base_top[i] >> 6) & 1) if i < len(base_top) else (b << 1) & 127 
                                   for i, b in enumerate(base_bottom)])
            elif shift == 2:
                # Shift up more
                wave_top = bytes([(b << 2) & 127 for b in base_top])
                wave_bottom = bytes([((b << 2) & 127) | ((base_top[i] >> 5) & 3) if i < len(base_top) else (b << 2) & 127 
                                   for i, b in enumerate(base_bottom)])
            else:
                # Back to normal
                wave_top = base_top
                wave_bottom = base_bottom
            
            # Fill top row (positions 0-29)
            for i in range(min(30, len(wave_top))):
                col_pos = padding + i
                if col_pos < 30:
                    display_buffer[col_pos] = wave_top[i]
            
            # Fill bottom row (positions 75-104)
            for i in range(min(30, len(wave_bottom))):
                col_pos = padding + i
                if col_pos < 30:
                    display_buffer[75 + col_pos] = wave_bottom[i]
            
            working_core.fill(bytes(display_buffer))
            time.sleep(0.2)
    
    time.sleep(1)

# Enhanced transition lists
SINGLE_HEIGHT_TRANSITIONS = [righttoleft, upnext, pop, magichat, typewriter]
DOUBLE_HEIGHT_TRANSITIONS = [
    double_height_plain, 
    double_height_scroll, 
    double_height_typewriter, 
    double_height_pop,
    double_height_upnext,
    double_height_magic_reveal,
    double_height_wave
]

ALL_TRANSITIONS = SINGLE_HEIGHT_TRANSITIONS + DOUBLE_HEIGHT_TRANSITIONS

# Mixed mode transitions (combines single and double height)
def mixed_announcement(message: str):
    """Mixed height announcement - double height title, single height message."""
    # Split message into title and content
    parts = message.split(' - ', 1) if ' - ' in message else [message[:8], message[8:]]
    title = parts[0]
    content = parts[1] if len(parts) > 1 else ""
    
    # Double height title
    display_double_height_text(working_core, title, justify='center')
    time.sleep(2)
    
    # Single height content scroll if there's more
    if content:
        clear()
        time.sleep(0.5)
        righttoleft(content)

def size_transition(message: str):
    """Transition from double height to single height."""
    # Show in double height first
    display_double_height_text(working_core, message[:6], justify='center')  # Show first 6 chars
    time.sleep(2)
    
    # Transition to single height with full message
    clear()
    time.sleep(0.3)
    working_core.display_text(message, justify='center')
    time.sleep(3)

def emphasis_transition(message: str):
    """Emphasize key words in double height."""
    words = message.split()
    
    for i, word in enumerate(words):
        clear()
        if len(word) <= 6 and (i == 0 or i == len(words) - 1):  # First or last word
            display_double_height_text(working_core, word, justify='center')
        else:
            working_core.display_text(word, justify='center')
        time.sleep(1.5)
    
    # Show full message at end
    clear()
    time.sleep(0.5)
    righttoleft(message)

# Random selection functions
def random_single_height(message: str):
    """Random single-height transition."""
    random.choice(SINGLE_HEIGHT_TRANSITIONS)(message)

def random_double_height(message: str):
    """Random double-height transition."""
    random.choice(DOUBLE_HEIGHT_TRANSITIONS)(message)

def random_any(message: str):
    """Random transition from any available."""
    random.choice(ALL_TRANSITIONS)(message)

def random_mixed(message: str):
    """Random mixed-mode transition."""
    mixed_transitions = [mixed_announcement, size_transition, emphasis_transition]
    random.choice(mixed_transitions)(message)

# Smart transition selector
def smart_transition(message: str):
    """Intelligently select transition based on message characteristics."""
    msg_len = len(message)
    
    if msg_len <= 6:
        # Short message - good for double height
        random_double_height(message)
    elif msg_len <= 12:
        # Medium message - could work with either
        if random.random() < 0.6:  # Favor double height
            random_double_height(message)
        else:
            random_single_height(message)
    elif msg_len <= 20:
        # Long message - better for single height or mixed
        if random.random() < 0.3:
            random_mixed(message)
        else:
            random_single_height(message)
    else:
        # Very long message - single height only
        random_single_height(message)

# Test function
def test_all_transitions():
    """Test all transition types."""
    test_messages = [
        ("Short", "HELLO"),
        ("Medium", "HELLO WORLD"), 
        ("Long", "THIS IS A LONGER MESSAGE"),
    ]
    
    print("Testing Single Height Transitions:")
    print("-" * 40)
    for name, msg in test_messages:
        print(f"Testing {name} message: '{msg}'")
        for transition_name, transition_func in [
            ("Right to Left", righttoleft),
            ("Pop", pop),
            ("Magic Hat", magichat),
            ("Typewriter", typewriter)
        ]:
            print(f"  {transition_name}...")
            try:
                transition_func(msg)
                clear()
                time.sleep(0.5)
            except Exception as e:
                print(f"    Error: {e}")
    
    print("\nTesting Double Height Transitions:")
    print("-" * 40)
    short_msg = "HELLO"
    for transition_name, transition_func in [
        ("Plain", double_height_plain),
        ("Scroll", double_height_scroll),
        ("Typewriter", double_height_typewriter),
        ("Pop", double_height_pop),
        ("Magic Reveal", double_height_magic_reveal),
        ("Wave", double_height_wave)
    ]:
        print(f"  {transition_name}...")
        try:
            transition_func(short_msg)
            clear()
            time.sleep(0.5)
        except Exception as e:
            print(f"    Error: {e}")
    
    print("\nTesting Mixed Mode Transitions:")
    print("-" * 40)
    mixed_msg = "TITLE - This is the content part"
    for transition_name, transition_func in [
        ("Mixed Announcement", mixed_announcement),
        ("Size Transition", size_transition), 
        ("Emphasis", emphasis_transition)
    ]:
        print(f"  {transition_name}...")
        try:
            transition_func(mixed_msg)
            clear()
            time.sleep(0.5)
        except Exception as e:
            print(f"    Error: {e}")

# Updated playlist format with height specification
def create_enhanced_playlist():
    """Create an enhanced playlist with mixed height transitions.""" 
    return [
        {"function": double_height_plain, "parameter": "BIOPUNK", "type": "double"},
        {"function": double_height_upnext, "parameter": "BIOLOGY", "type": "double"},
        {"function": magichat, "parameter": "exploring digital frontiers", "type": "single"},
        {"function": double_height_wave, "parameter": "HACKER", "type": "double"},
        {"function": mixed_announcement, "parameter": "NEXT - Advanced bioengineering concepts", "type": "mixed"},
        {"function": emphasis_transition, "parameter": "FUTURE TECH PREVIEW", "type": "mixed"},
        {"function": smart_transition, "parameter": "Adaptive display technology", "type": "smart"},
    ]

# Utility functions for playlist management
def execute_playlist_item(item):
    """Execute a single playlist item safely."""
    try:
        if item.get("parameter"):
            item["function"](item["parameter"])
        else:
            item["function"]()
        
        # Log the transition type
        transition_type = item.get("type", "unknown")
        print(f"Executed {item['function'].__name__} ({transition_type})")
        
    except Exception as e:
        print(f"Error executing {item.get('function', 'unknown')}: {e}")
        clear()  # Clear display on error

def run_enhanced_playlist(playlist=None, loop=True):
    """Run an enhanced playlist with error handling."""
    if playlist is None:
        playlist = create_enhanced_playlist()
    
    print(f"Running enhanced playlist with {len(playlist)} items...")
    
    try:
        while True:
            for item in playlist:
                execute_playlist_item(item)
                time.sleep(1)  # Brief pause between transitions
            
            if not loop:
                break
                
    except KeyboardInterrupt:
        print("\nPlaylist stopped by user")
        clear()

if __name__ == "__main__":
    print("Enhanced Transitions with Double Height Support")
    print("=" * 50)
    
    # Quick demo
    print("Running quick demo...")
    try:
        double_height_plain("DEMO")
        time.sleep(2)
        clear()
        print("Demo complete!")
        
        # Uncomment to run full test
        # test_all_transitions()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()