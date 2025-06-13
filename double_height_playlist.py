#!/usr/bin/env python3
"""
Double Height Playlist Example

Shows how to use single-height and double-height text in your playlist.
"""

import time
from transition.transition import (
    righttoleft, righttoleft_double,
    upnext, upnext_double, 
    magichat, magichat_double,
    typewriter, typewriter_double,
    plain, plain_double
)

# Updated playlist with height options
MAIN_PLAYLIST = [
    # Regular single-height (7 pixels high) - like your original
    {"function": righttoleft, "parameter": "bioPunk", "name": "bioPunk (single)"},
    
    # Double-height (14 pixels high) - uses full display height
    {"function": righttoleft_double, "parameter": "bioPunk", "name": "bioPunk (double)"},
    
    # Mix of heights for variety
    {"function": upnext, "parameter": "Single Height", "name": "Announcement (single)"},
    {"function": upnext_double, "parameter": "DOUBLE", "name": "Announcement (double)"},
    
    {"function": typewriter, "parameter": "biology", "name": "Typewriter (single)"},
    {"function": typewriter_double, "parameter": "BIOTECH", "name": "Typewriter (double)"},
    
    {"function": magichat, "parameter": "synthetic life forms evolving", "name": "Magic Hat (single)"},
    {"function": magichat_double, "parameter": "GENETIC CODE", "name": "Magic Hat (double)"},
]

# Or use the height parameter directly:
FLEXIBLE_PLAYLIST = [
    # Same function, different heights
    {"function": righttoleft, "parameter": "bioPunk", "height": "single"},
    {"function": righttoleft, "parameter": "bioPunk", "height": "double"},
    
    {"function": plain, "parameter": "Standard text scrolling", "height": "single"},
    {"function": plain, "parameter": "BIG TEXT", "height": "double"},
]

def run_playlist(playlist_name="main"):
    """Run the specified playlist."""
    
    if playlist_name == "main":
        playlist = MAIN_PLAYLIST
    else:
        playlist = FLEXIBLE_PLAYLIST
    
    print(f"Starting {playlist_name} playlist with single and double height text...")
    
    try:
        while True:
            for sequence in playlist:
                print(f"Playing: {sequence.get('name', sequence.get('parameter', 'Unknown'))}")
                
                # Handle height parameter if specified
                if 'height' in sequence:
                    # Call function with height parameter
                    if sequence["parameter"] is not None:
                        sequence["function"](sequence["parameter"], height=sequence["height"])
                    else:
                        sequence["function"](height=sequence["height"])
                else:
                    # Call function normally
                    if sequence["parameter"] is not None:
                        sequence["function"](sequence["parameter"])
                    else:
                        sequence["function"]()
                
                time.sleep(1)  # Pause between items
                
    except KeyboardInterrupt:
        print("\nPlaylist interrupted")
        from core.core import clear
        clear()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        run_playlist(sys.argv[1])
    else:
        run_playlist("main")
