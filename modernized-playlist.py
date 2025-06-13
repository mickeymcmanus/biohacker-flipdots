#!/usr/bin/env python3
"""
Main Playlist for Frontier Tower Display

This script runs a continuous playlist of animations, videos, and transitions
on the flipdot display.
"""

import time
from typing import Dict, Any, List, Optional, Callable
from video import video
from twitter import twitter
from transition import transition
from games.scavengerhunt import scavengerhunt

__author__ = 'boselowitz (modernized version)'

# Constants
DEFAULT_DELAY = 0.75

# Define playlist types with proper type hints
PlaylistItem = Dict[str, Any]
Playlist = List[PlaylistItem]

# Main playlist with different display elements
MAIN_PLAYLIST: Playlist = [
   # {"function": transition.adventurelook, "parameter": "What?"},#broken length
     {"function": transition.plain, "parameter": "Bio Punk"},
    {"function": video.display_video, "parameter": "barber-pole-10s.mov"},
    {"function": transition.righttoleft, "parameter": "Floor 8...   Biotech"},
    
    # Commented items kept for reference and easy re-enabling
    # {"function": transition.pop, "parameter": "Biotech"},
    # {"function": transition.upnext, "parameter": "Welcome"},
    # {"function": transition.amdissolve, "parameter": "FIRESIDE CHAT"}, # bottom row broken
    #{"function": transition.dissolve, "parameter": "THE FUTURE"}, # bottom row broken
    # {"function": transition.righttoleft, "parameter": "WELCOME TO RAPID"},
    # {"function": transition.magichat, "parameter": "COME JOIN US"},
    # {"function": video.display_video, "parameter": "printer-welcome"},
    # {"function": video.display_video, "parameter": "block-game"},
    # {"function": twitter.display_direct_messages, "parameter": None},
    # {"function": video.display_video, "parameter": "printer-namii"},
    # {"function": transition.righttoleft, "parameter": "WIN A IPAD MINI -- NAMII SCAVENGER HUNT -- WINNERS CMU MECHANICAL ENGINEERING DEPARTMENT"},
    # {"function": transition.magichat, "parameter": "FOR EVERY $1.00 SPENT IN MANUFACTURING, ANOTHER $1.48 IS ADDED TO THE ECONOMY"},
    # {"function": twitter.display_direct_messages, "parameter": None},
]

# Alternate quieter playlist
QUIET_PLAYLIST: Playlist = [
    {"function": transition.righttoleft, "parameter": "77 MEMBERS AND COUNTING"},
    {"function": transition.amdissolve, "parameter": "FIRESIDE CHAT"},
    {"function": transition.dissolve, "parameter": "SHAPE THE FUTURE"},
]

# Set the active playlist
DEFAULT_PLAYLIST = MAIN_PLAYLIST


def run_playlist(playlist: Playlist) -> None:
    """
    Run through all items in a playlist once.
    
    Args:
        playlist: List of playlist items to execute
    """
    for sequence in playlist:
        if sequence["parameter"] is not None:
            sequence["function"](sequence["parameter"])
        else:
            sequence["function"]()


def main() -> None:
    """Main function to run the playlist continuously."""
    print("Starting Frontier Tower display playlist...")
    
    try:
        while True:
            run_playlist(DEFAULT_PLAYLIST)
    except KeyboardInterrupt:
        print("\nPlaylist stopped by user.")
    except Exception as e:
        print(f"Error in playlist: {e}")
        # Could add logging here in a more robust version


if __name__ == "__main__":
    main()
