#!/usr/bin/env python3
"""
Final Enhanced Transitions with Working Quadrant Mapping

Now using the PROVEN quadrant buffer mapping that works on your display.
Provides transitions for single-height, double-height, and double-wide text.
"""

import time
import random

# Import your existing transitions
try:
    from .transition import *
    print("✅ Imported existing single-height transitions")
except ImportError:
    print("⚠️ Could not import existing transitions - using fallbacks")

# Import the WORKING enhanced core
try:
    from .final_enhanced_core import (
        working_core, clear,
        display_text_single_height,
        display_text_double_height,
        display_text_double_wide_double_height,
        scroll_text_double_height,
        typewriter_text_double_height,
        getbytes, scrollleft
    )
    print("✅ Imported WORKING enhanced core functions")
except ImportError:
    try:
        from final_enhanced_core import (
            working_core, clear,
            display_text_single_height,
            display_text_double_height,
            display_text_double_wide_double_height,
            scroll_text_double_height,
            typewriter_text_double_height,
            getbytes, scrollleft
        )
        print("✅ Imported WORKING enhanced core functions (direct)")
    except ImportError as e:
        print(f"❌ Could not import WORKING enhanced core: {e}")
        # Fallback imports
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from core.core import working_core, clear, getbytes, scrollleft

# ============================================================================
# SINGLE HEIGHT TRANSITIONS (Original 7-pixel text)
# ============================================================================

def single_plain(message):
    """Plain single-height display."""
    display_text_single_height(message, justify='center')
    time.sleep(3)

def single_scroll(message):
    """Scrolling single-height text."""
    msg_bytes = getbytes(message)
    scrollleft(msg_bytes, t=0.2)

def single_typewriter(message):
    """Typewriter single-height text."""
    for i in range(1, len(message) + 1):
        partial = message[:i]
        display_text_single_height(partial, justify='left')
        time.sleep(0.1)
    time.sleep(2)

def single_flash(message):
    """Flash single-height text."""
    for _ in range(5):
        display_text_single_height(message, justify='center')
        time.sleep(0.3)
        clear()
        time.sleep(0.3)

def single_upnext(message):
    """Up next style with single-height."""
    # Flash "UP NEXT"
    for i in range(3):
        display_text_single_height("UP NEXT", justify='center')
        time.sleep(0.3)
        clear()
        time.sleep(0.3)
    
    time.sleep(0.5)
    # Show message
    single_scroll(message)

# ============================================================================
# DOUBLE HEIGHT TRANSITIONS (14-pixel text) - WORKING VERSIONS
# ============================================================================

def double_plain(message):
    """Plain double-height display using WORKING quadrant mapping."""
    display_text_double_height(message, justify='center')
    time.sleep(3)

def double_scroll(message):
    """Scrolling double-height text using WORKING quadrant mapping."""
    scroll_text_double_height(message)

def double_typewriter(message):
    """Typewriter double-height text using WORKING quadrant mapping."""
    typewriter_text_double_height(message)
    time.sleep(2)

def double_flash(message):
    """Flash double-height text using WORKING quadrant mapping."""
    for _ in range(5):
        display_text_double_height(message, justify='center')
        time.sleep(0.3)
        clear()
        time.sleep(0.3)

def double_upnext(message):
    """Up next style with double-height using WORKING quadrant mapping."""
    # Flash "UP NEXT"
    for i in range(3):
        display_text_double_height("UP NEXT", justify='center')
        time.sleep(0.4)
        clear()
        time.sleep(0.4)
    
    time.sleep(0.5)
    # Show message
    double_scroll(message)

def double_dramatic(message):
    """Dramatic entrance for double-height text."""
    # Quick flash sequence
    for i in range(3):
        display_text_double_height(message, justify='center')
        time.sleep(0.2)
        clear()
        time.sleep(0.1)
    
    # Final display
    display_text_double_height(message, justify='center')
    time.sleep(3)

# ============================================================================
# DOUBLE WIDE + HEIGHT TRANSITIONS (14-pixel tall, 2x wider) - WORKING
# ============================================================================

def wide_plain(message):
    """Plain double-wide double-height display using WORKING quadrant mapping."""
    display_text_double_wide_double_height(message, justify='center')
    time.sleep(3)

def wide_flash(message):
    """Flash double-wide double-height text using WORKING quadrant mapping."""
    for _ in range(4):
        display_text_double_wide_double_height(message, justify='center')
        time.sleep(0.4)
        clear()
        time.sleep(0.4)

def wide_dramatic(message):
    """Dramatic entrance for double-wide text using WORKING quadrant mapping."""
    # Quick flash sequence
    for i in range(3):
        display_text_double_wide_double_height(message, justify='center')
        time.sleep(0.2)
        clear()
        time.sleep(0.1)
    
    # Final display
    display_text_double_wide_double_height(message, justify='center')
    time.sleep(3)

def wide_typewriter(message):
    """Typewriter effect for double-wide text."""
    # Since it's so wide, show character by character
    for i in range(1, min(len(message) + 1, 4)):  # Limit to 3 chars
        partial = message[:i]
        display_text_double_wide_double_height(partial, justify='left')
        time.sleep(0.6)
    time.sleep(2)

# ============================================================================
# MIXED SIZE TRANSITIONS using WORKING mapping
# ============================================================================

def size_escalation(message):
    """Show message in escalating sizes using WORKING mapping."""
    # Start small
    display_text_single_height(message, justify='center')
    time.sleep(1.5)
    clear()
    
    # Medium
    display_text_double_height(message[:5], justify='center')
    time.sleep(1.5)
    clear()
    
    # Large (first 3 chars only)
    display_text_double_wide_double_height(message[:3], justify='center')
    time.sleep(2)

def mixed_announcement(message):
    """Mixed size announcement using WORKING mapping."""
    # Split message into title and content
    parts = message.split(' - ', 1) if ' - ' in message else [message[:4], message[4:]]
    title = parts[0]
    content = parts[1] if len(parts) > 1 else ""
    
    # Big title
    display_text_double_height(title, justify='center')
    time.sleep(2)
    clear()
    
    # Smaller content
    if content:
        time.sleep(0.5)
        single_scroll(content)

def emphasis_transition(message):
    """Emphasize different parts of message using WORKING mapping."""
    words = message.split()
    
    for i, word in enumerate(words[:3]):  # Limit to 3 words
        clear()
        
        if i == 0:  # First word big
            display_text_double_height(word, justify='center')
        elif len(word) <= 3:  # Short words extra big
            display_text_double_wide_double_height(word, justify='center')
        else:  # Normal size
            display_text_single_height(word, justify='center')
        
        time.sleep(1.5)
    
    clear()
    time.sleep(0.5)
    # Show full message in single height
    single_scroll(message)

def impact_sequence(message):
    """Maximum impact sequence for short messages."""
    if len(message) <= 3:
        # Very short - maximum impact
        wide_dramatic(message)
    else:
        # Build up sequence
        for i in range(1, min(len(message) + 1, 4)):
            partial = message[:i]
            if len(partial) <= 3:
                display_text_double_wide_double_height(partial, justify='center')
            else:
                display_text_double_height(partial, justify='center')
            time.sleep(0.8)
            if i < min(len(message), 3):
                clear()
                time.sleep(0.2)

# ============================================================================
# TRANSITION LISTS with WORKING functions
# ============================================================================

SINGLE_HEIGHT_TRANSITIONS = [
    single_plain, single_scroll, single_typewriter, single_flash, single_upnext
]

DOUBLE_HEIGHT_TRANSITIONS = [
    double_plain, double_scroll, double_typewriter, double_flash, 
    double_upnext, double_dramatic
]

DOUBLE_WIDE_TRANSITIONS = [
    wide_plain, wide_flash, wide_typewriter, wide_dramatic
]

MIXED_SIZE_TRANSITIONS = [
    size_escalation, mixed_announcement, emphasis_transition, impact_sequence
]

ALL_TRANSITIONS = (SINGLE_HEIGHT_TRANSITIONS + DOUBLE_HEIGHT_TRANSITIONS + 
                  DOUBLE_WIDE_TRANSITIONS + MIXED_SIZE_TRANSITIONS)

# ============================================================================
# SMART TRANSITION SELECTION using WORKING mapping
# ============================================================================

def smart_transition(message):
    """Intelligently select transition based on message characteristics."""
    msg_len = len(message)
    
    if msg_len <= 3:
        # Very short - use double-wide for maximum impact
        random.choice(DOUBLE_WIDE_TRANSITIONS)(message)
    elif msg_len <= 6:
        # Short - good for double height
        random.choice(DOUBLE_HEIGHT_TRANSITIONS)(message)
    elif msg_len <= 12:
        # Medium - mix of sizes
        if random.random() < 0.4:
            random.choice(MIXED_SIZE_TRANSITIONS)(message)
        else:
            random.choice(DOUBLE_HEIGHT_TRANSITIONS)(message)
    else:
        # Long - single height works best
        random.choice(SINGLE_HEIGHT_TRANSITIONS)(message)

def random_single_height(message):
    """Random single-height transition."""
    random.choice(SINGLE_HEIGHT_TRANSITIONS)(message)

def random_double_height(message):
    """Random double-height transition."""
    random.choice(DOUBLE_HEIGHT_TRANSITIONS)(message)

def random_double_wide(message):
    """Random double-wide transition."""
    random.choice(DOUBLE_WIDE_TRANSITIONS)(message)

def random_mixed(message):
    """Random mixed-size transition."""
    random.choice(MIXED_SIZE_TRANSITIONS)(message)

def random_any(message):
    """Random transition from any available."""
    random.choice(ALL_TRANSITIONS)(message)

# ============================================================================
# PLAYLIST BUILDERS using WORKING functions
# ============================================================================

def create_working_demo_playlist():
    """Create a demo playlist showcasing all WORKING text sizes."""
    return [
        # Single height
        {"function": single_plain, "parameter": "SINGLE HEIGHT", "type": "single"},
        {"function": single_scroll, "parameter": "NORMAL TEXT SCROLLING", "type": "single"},
        
        # Double height - WORKING
        {"function": double_plain, "parameter": "DOUBLE", "type": "double"},
        {"function": double_scroll, "parameter": "BIG TEXT", "type": "double"},
        {"function": double_upnext, "parameter": "NEWS", "type": "double"},
        
        # Double wide - WORKING
        {"function": wide_dramatic, "parameter": "WOW", "type": "wide"},
        {"function": wide_flash, "parameter": "BIG", "type": "wide"},
        
        # Mixed - WORKING
        {"function": size_escalation, "parameter": "ESCALATE", "type": "mixed"},
        {"function": mixed_announcement, "parameter": "TITLE - Content goes here", "type": "mixed"},
        {"function": impact_sequence, "parameter": "GO", "type": "mixed"},
    ]

def create_working_biopunk_playlist():
    """Create an enhanced biopunk playlist with WORKING multi-size text."""
    return [
        {"function": wide_dramatic, "parameter": "BIO", "type": "wide"},
        {"function": double_upnext, "parameter": "PUNK", "type": "double"},
        {"function": single_scroll, "parameter": "Digital evolution in progress", "type": "single"},
        {"function": double_flash, "parameter": "HACKER", "type": "double"},
        {"function": mixed_announcement, "parameter": "FUTURE - Biotechnology revolution", "type": "mixed"},
        {"function": size_escalation, "parameter": "EVOLVE", "type": "mixed"},
        {"function": double_scroll, "parameter": "DIGITAL DNA", "type": "double"},
        {"function": impact_sequence, "parameter": "GO", "type": "mixed"},
    ]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def display_text(message, size='single', justify='center'):
    """
    Unified text display function using WORKING mapping.
    
    Args:
        message: Text to display
        size: 'single', 'double', or 'wide'
        justify: 'left', 'center', or 'right'
    """
    if size == 'single':
        display_text_single_height(message, justify)
    elif size == 'double':
        display_text_double_height(message, justify)
    elif size == 'wide':
        display_text_double_wide_double_height(message, justify)
    else:
        print(f"Unknown size: {size}, using single height")
        display_text_single_height(message, justify)

def run_playlist(playlist, loop=False):
    """Run a playlist with WORKING enhanced transitions."""
    print(f"🎬 Running playlist with {len(playlist)} items...")
    
    try:
        while True:
            for item in playlist:
                print(f"Executing: {item['function'].__name__} ({item.get('type', 'unknown')})")
                
                try:
                    if item.get("parameter"):
                        item["function"](item["parameter"])
                    else:
                        item["function"]()
                    
                    time.sleep(0.5)  # Brief pause between items
                    
                except Exception as e:
                    print(f"Error in {item['function'].__name__}: {e}")
                    clear()
                    time.sleep(1)
            
            if not loop:
                break
                
    except KeyboardInterrupt:
        print("\nPlaylist stopped by user")
        clear()

# Export all WORKING functions
__all__ = [
    # Single height transitions
    'single_plain', 'single_scroll', 'single_typewriter', 'single_flash', 'single_upnext',
    
    # Double height transitions (WORKING)  
    'double_plain', 'double_scroll', 'double_typewriter', 'double_flash', 'double_upnext',
    'double_dramatic',
    
    # Double wide transitions (WORKING)
    'wide_plain', 'wide_flash', 'wide_typewriter', 'wide_dramatic',
    
    # Mixed size transitions (WORKING)
    'size_escalation', 'mixed_announcement', 'emphasis_transition', 'impact_sequence',
    
    # Smart selection (WORKING)
    'smart_transition', 'random_single_height', 'random_double_height', 
    'random_double_wide', 'random_mixed', 'random_any',
    
    # Utilities (WORKING)
    'display_text', 'create_working_demo_playlist', 'create_working_biopunk_playlist', 'run_playlist',
    
    # Transition lists
    'SINGLE_HEIGHT_TRANSITIONS', 'DOUBLE_HEIGHT_TRANSITIONS', 'DOUBLE_WIDE_TRANSITIONS',
    'MIXED_SIZE_TRANSITIONS', 'ALL_TRANSITIONS'
]

if __name__ == "__main__":
    print("🎨 Final Enhanced Transitions with WORKING Quadrant Mapping")
    print("=" * 70)
    print("All double-height functions now use the PROVEN WORKING buffer mapping!")
    
    choice = input("\nTest WORKING double-height transitions? (y/n): ").strip().lower()
    if choice == 'y':
        test_transitions = [
            ("Double Plain", lambda: double_plain("TEST")),
            ("Double Flash", lambda: double_flash("FLASH")),
            ("Wide Dramatic", lambda: wide_dramatic("WOW")),
            ("Impact Sequence", lambda: impact_sequence("GO")),
        ]
        
        for name, test_func in test_transitions:
            choice = input(f"Test {name}? (y/n): ").strip().lower()
            if choice == 'y':
                print(f"Testing {name}...")
                test_func()
                input("Press Enter to continue...")
                clear()
    
    choice = input("\nRun WORKING demo playlist? (y/n): ").strip().lower()
    if choice == 'y':
        demo_playlist = create_working_demo_playlist()
        run_playlist(demo_playlist)
    
    choice = input("\nRun WORKING biopunk playlist? (y/n): ").strip().lower()
    if choice == 'y':
        biopunk_playlist = create_working_biopunk_playlist()
        run_playlist(biopunk_playlist)
    
    print("✅ Final enhanced transitions test complete!")
    print("🎉 You now have working single-height, double-height, and double-wide text!")
