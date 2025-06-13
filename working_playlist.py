#!/usr/bin/env python3
"""
Working Playlist - Updated version of your mainplaylist-biopunk.py
"""

import time
from complete_working_core import working_core
from working_transitions import righttoleft, upnext, magichat, dissolve, randomgeneral

# Updated playlist using working transitions
MAIN_PLAYLIST = [
    {"function": righttoleft, "parameter": "bioPunk"},
    {"function": upnext, "parameter": "bioPunk Systems"},
    {"function": dissolve, "parameter": "biology"},
    {"function": magichat, "parameter": "biotech revolution"},
    {"function": randomgeneral, "parameter": "synthetic life forms"},
]

DEFAULT_PLAYLIST = MAIN_PLAYLIST

def run_playlist():
    """Run the working playlist."""
    print("Starting bioPunk playlist with working transitions...")
    
    try:
        while True:
            for sequence in DEFAULT_PLAYLIST:
                print(f"Playing: {sequence.get('parameter', 'No parameter')}")
                
                if sequence["parameter"] is not None:
                    sequence["function"](sequence["parameter"])
                else:
                    sequence["function"]()
                
                time.sleep(1)  # Pause between items
                
    except KeyboardInterrupt:
        print("\nPlaylist interrupted")
        working_core.clear()

if __name__ == "__main__":
    run_playlist()
