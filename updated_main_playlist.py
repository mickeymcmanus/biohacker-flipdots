#!/usr/bin/env python3
"""
Updated Main Playlist for Reconfigurable Flipdot Display

This script demonstrates the new reconfigurable system with your 2×6 module setup.
"""

import time
import sys
import os
from typing import List, Dict, Any, Callable

# Import the new modules
from core.reconfigurable_flipdot import create_display, DISPLAY_CONFIGS, TextHeight
from transition.updated_transitions import (
    set_display as set_transition_display, 
    righttoleft, upnext, dissolve, magichat, plain, typewriter, 
    matrix_effect, slide_in_left, randomgeneral
)
from video.updated_video import (
    set_display as set_video_display,
    display_video, quick_play, create_test_pattern, get_video_info
)

__author__ = 'boselowitz (updated version)'

class PlaylistItem:
    """Represents an item in the display playlist."""
    
    def __init__(self, function: Callable, parameter: Any = None, 
                 name: str = "", duration: float = 0):
        self.function = function
        self.parameter = parameter
        self.name = name or f"{function.__name__}"
        self.duration = duration
    
    def execute(self):
        """Execute this playlist item."""
        print(f"Playing: {self.name}")
        start_time = time.time()
        
        try:
            if self.parameter is not None:
                self.function(self.parameter)
            else:
                self.function()
        except Exception as e:
            print(f"Error executing {self.name}: {e}")
        
        elapsed = time.time() - start_time
        print(f"Completed {self.name} in {elapsed:.2f}s")

class FlipdotPlaylist:
    """Manages and executes a playlist for the flipdot display."""
    
    def __init__(self, config_name: str = "current", port: str = "/dev/tty.usbserial-A3000lDq"):
        """
        Initialize the playlist system.
        
        Args:
            config_name: Display configuration to use
            port: Serial port for the display
        """
        print(f"Initializing Flipdot Playlist System")
        print(f"Configuration: {config_name}")
        
        # Create the display
        self.display = create_display(config_name, port=port)
        print(self.display.get_config_info())
        
        # Set up the modules to use this display
        set_transition_display(self.display)
        set_video_display(self.display)
        
        self.playlist: List[PlaylistItem] = []
        self.current_index = 0
        self.loop_playlist = True
    
    def add_text(self, message: str, transition_func: Callable = righttoleft, 
                name: str = "") -> None:
        """Add a text item to the playlist."""
        item = PlaylistItem(
            function=transition_func,
            parameter=message,
            name=name or f"Text: {message[:20]}..."
        )
        self.playlist.append(item)
    
    def add_video(self, video_name: str, auto_convert: bool = True, 
                 fps: float = 12.0, name: str = "") -> None:
        """Add a video item to the playlist."""
        def play_video():
            quick_play(video_name, auto_convert=auto_convert, fps=fps)
        
        item = PlaylistItem(
            function=play_video,
            name=name or f"Video: {video_name}"
        )
        self.playlist.append(item)
    
    def add_custom(self, function: Callable, parameter: Any = None, 
                  name: str = "") -> None:
        """Add a custom function to the playlist."""
        item = PlaylistItem(
            function=function,
            parameter=parameter,
            name=name or f"Custom: {function.__name__}"
        )
        self.playlist.append(item)
    
    def run_test_sequence(self) -> None:
        """Run a test sequence to verify display functionality."""
        print("\n=== Running Test Sequence ===")
        
        # Test pattern
        print("1. Test Pattern")
        create_test_pattern()
        
        # Simple text
        print("2. Simple Text")
        self.display.display_text("HELLO WORLD", TextHeight.AUTO, scroll=True)
        time.sleep(2)
        
        # Different transitions
        test_messages = [
            ("Basic scroll", plain),
            ("Typewriter", typewriter),
            ("Matrix effect", matrix_effect),
            ("Slide from left", slide_in_left),
        ]
        
        for msg, transition in test_messages:
            print(f"3. Testing: {msg}")
            transition("TEST MESSAGE")
            time.sleep(1)
        
        self.display.clear()
        print("Test sequence completed!")
    
    def play(self, start_index: int = 0) -> None:
        """
        Play the playlist.
        
        Args:
            start_index: Index to start playing from
        """
        if not self.playlist:
            print("Playlist is empty!")
            return
        
        self.current_index = start_index
        print(f"\n=== Starting Playlist ({len(self.playlist)} items) ===")
        
        try:
            while True:
                item = self.playlist[self.current_index]
                item.execute()
                
                self.current_index = (self.current_index + 1) % len(self.playlist)
                
                if not self.loop_playlist and self.current_index == 0:
                    break
                
                # Small delay between items
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nPlaylist interrupted by user")
        except Exception as e:
            print(f"Playlist error: {e}")
        finally:
            self.display.clear()
            print("Playlist stopped")
    
    def show_playlist(self) -> None:
        """Display the current playlist."""
        print(f"\n=== Current Playlist ({len(self.playlist)} items) ===")
        for i, item in enumerate(self.playlist):
            marker = ">" if i == self.current_index else " "
            print(f"{marker} {i+1:2d}. {item.name}")
    
    def clear_playlist(self) -> None:
        """Clear the current playlist."""
        self.playlist.clear()
        self.current_index = 0
        print("Playlist cleared")

def create_biopunk_playlist() -> FlipdotPlaylist:
    """Create the bioPunk themed playlist (updated version of your original)."""
    playlist = FlipdotPlaylist("current")
    
    # Add text items with different transitions
    playlist.add_text("bioPunk", righttoleft, "BioPunk Title")
    playlist.add_text("biology meets technology", magichat, "Biology Message")
    playlist.add_text("synthetic life forms", typewriter, "Synthetic Life")
    playlist.add_text("genetic algorithms", matrix_effect, "Genetic Algorithms")
    
    # Add video (will auto-convert if needed)
    playlist.add_video("barber-pole-10s.mov", name="Barber Pole Animation")
    
    # Add some special effects
    playlist.add_custom(
        lambda: playlist.display.display_text("< SYSTEM ONLINE >", TextHeight.SINGLE, scroll=True),
        name="System Status"
    )
    
    return playlist

def create_demo_playlist() -> FlipdotPlaylist:
    """Create a demo playlist showcasing different features."""
    playlist = FlipdotPlaylist("current")
    
    # Welcome sequence
    playlist.add_text("FLIPDOT DISPLAY SYSTEM", upnext, "Welcome")
    playlist.add_text("Reconfigurable Controller", slide_in_left, "Subtitle")
    
    # Feature demonstrations
    playlist.add_text("Text can scroll smoothly", plain, "Scroll Demo")
    playlist.add_text("Or appear with effects", matrix_effect, "Effects Demo")
    playlist.add_text("Multiple display sizes supported", typewriter, "Size Demo")
    
    # If you have test videos
    video_info = get_video_info("test-pattern.mov")
    if video_info['video_exists']:
        playlist.add_video("test-pattern.mov", name="Test Pattern Video")
    
    # Random content
    playlist.add_custom(
        lambda: randomgeneral("Random transition effects"),
        name="Random Effects"
    )
    
    return playlist

def main():
    """Main function - customize this for your needs."""
    print("Flipdot Display Playlist System")
    print("==============================")
    
    # Show available configurations
    print("\nAvailable display configurations:")
    for name, config in DISPLAY_CONFIGS.items():
        print(f"  {name}: {config.name} ({config.total_width}×{config.total_height})")
    
    # You can change this to test different configurations
    config_name = "current"  # Your 2×6 setup
    
    try:
        if len(sys.argv) > 1:
            mode = sys.argv[1].lower()
            
            if mode == "test":
                print(f"\nRunning test mode with {config_name} configuration...")
                playlist = FlipdotPlaylist(config_name)
                playlist.run_test_sequence()
                
            elif mode == "demo":
                print(f"\nRunning demo playlist...")
                playlist = create_demo_playlist()
                playlist.show_playlist()
                playlist.play()
                
            elif mode == "biopunk":
                print(f"\nRunning bioPunk playlist...")
                playlist = create_biopunk_playlist()
                playlist.show_playlist()
                playlist.play()
                
            else:
                print(f"Unknown mode: {mode}")
                print("Available modes: test, demo, biopunk")
                
        else:
            # Default behavior - run the bioPunk playlist like your original
            print(f"\nRunning default bioPunk playlist...")
            playlist = create_biopunk_playlist()
            playlist.play()
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
