#!/usr/bin/env python3
"""
Test Playlist for Double Height Features

This playlist demonstrates all the double-height text capabilities
and can be used to verify everything is working correctly.
"""

import time
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import both old and new transition systems
try:
    # Try importing from your existing structure  
    from transition import transition
    print("✅ Found existing transition module")
except ImportError:
    print("⚠️  Could not import existing transition module")
    transition = None

try:
    # Import the enhanced transitions from transitions subfolder
    from transition.enhanced_transitions import *
    print("✅ Found enhanced transitions module")
except ImportError:
    try:
        # Fallback: try without subfolder
        from enhanced_transitions import *
        print("✅ Found enhanced transitions module (alternate path)")
    except ImportError:
        print("❌ Could not import enhanced_transitions - check file placement")
        print("Expected location: transition/enhanced_transitions.py")
        sys.exit(1)

try:
    from core.core import working_core, clear
    print("✅ Found core module")
except ImportError:
    try:
        from core import working_core, clear
        print("✅ Found core module (alternate path)")
    except ImportError:
        print("❌ Could not import core module")
        sys.exit(1)

# Test playlist with progressive complexity
DOUBLE_HEIGHT_TEST_PLAYLIST = [
    # Basic double height tests
    {"name": "Double Height Static", "function": double_height_plain, "parameter": "HELLO"},
    {"name": "Double Height Numbers", "function": double_height_plain, "parameter": "2024"}, 
    {"name": "Double Height Short", "function": double_height_plain, "parameter": "HI"},
    
    # Animation tests
    {"name": "Double Height Typewriter", "function": double_height_typewriter, "parameter": "TYPE"},
    {"name": "Double Height Pop", "function": double_height_pop, "parameter": "POP"},
    {"name": "Double Height Scroll", "function": double_height_scroll, "parameter": "SCROLL TEXT"},
    
    # Advanced effects
    {"name": "Double Height Wave", "function": double_height_wave, "parameter": "WAVE"},
    {"name": "Double Height Magic", "function": double_height_magic_reveal, "parameter": "MAGIC"},
    {"name": "Double Height Up Next", "function": double_height_upnext, "parameter": "NEWS"},
    
    # Mixed mode tests
    {"name": "Mixed Announcement", "function": mixed_announcement, "parameter": "TITLE - This is the longer content"},
    {"name": "Size Transition", "function": size_transition, "parameter": "SHRINK"},
    {"name": "Emphasis Effect", "function": emphasis_transition, "parameter": "BIG small BIG"},
    
    # Smart selection
    {"name": "Smart Short", "function": smart_transition, "parameter": "AUTO"},
    {"name": "Smart Medium", "function": smart_transition, "parameter": "AUTOMATIC MODE"},
    {"name": "Smart Long", "function": smart_transition, "parameter": "This message is long enough to trigger single height"},
]

# Comparison playlist (old vs new)
COMPARISON_PLAYLIST = [
    {"name": "OLD: Right to Left", "function": righttoleft, "parameter": "old style"},
    {"name": "NEW: Double Scroll", "function": double_height_scroll, "parameter": "NEW"},
    
    {"name": "OLD: Pop Effect", "function": pop, "parameter": "old pop"},
    {"name": "NEW: Double Pop", "function": double_height_pop, "parameter": "NEW"},
    
    {"name": "OLD: Typewriter", "function": typewriter, "parameter": "old type"},
    {"name": "NEW: Double Type", "function": double_height_typewriter, "parameter": "NEW"},
]

# Quick demo playlist (shorter for rapid testing)
QUICK_DEMO_PLAYLIST = [
    {"name": "Demo: Static", "function": double_height_plain, "parameter": "DEMO"},
    {"name": "Demo: Scroll", "function": double_height_scroll, "parameter": "WORKS"},
    {"name": "Demo: Mixed", "function": mixed_announcement, "parameter": "BIG - and small text"},
]

def run_playlist(playlist, name="Test Playlist", pause_between=2.0, show_names=True):
    """
    Run a playlist with error handling and progress display.
    
    Args:
        playlist: List of playlist items
        name: Name of the playlist for display
        pause_between: Seconds to pause between items
        show_names: Whether to print item names
    """
    print(f"\n🎬 Starting {name}")
    print("=" * 50)
    
    for i, item in enumerate(playlist, 1):
        item_name = item.get("name", f"Item {i}")
        
        if show_names:
            print(f"\n[{i}/{len(playlist)}] {item_name}")
            print("-" * 30)
        
        try:
            # Execute the transition
            if item.get("parameter"):
                item["function"](item["parameter"])
            else:
                item["function"]()
            
            print(f"✅ {item_name} completed")
            
            # Pause between items
            if i < len(playlist):  # Don't pause after last item
                time.sleep(pause_between)
                
        except Exception as e:
            print(f"❌ {item_name} failed: {e}")
            try:
                clear()  # Try to clear display on error
            except:
                pass
            time.sleep(1)  # Brief pause before continuing
    
    print(f"\n🏁 {name} completed!")
    clear()

def interactive_test():
    """Interactive test mode - let user choose what to test."""
    playlists = {
        "1": ("Quick Demo (3 items)", QUICK_DEMO_PLAYLIST),
        "2": ("Full Double Height Test (13 items)", DOUBLE_HEIGHT_TEST_PLAYLIST), 
        "3": ("Old vs New Comparison (6 items)", COMPARISON_PLAYLIST),
        "4": ("All Tests (22 items)", DOUBLE_HEIGHT_TEST_PLAYLIST + COMPARISON_PLAYLIST),
    }
    
    print("\n🎯 Double Height Text Test Menu")
    print("=" * 40)
    for key, (desc, _) in playlists.items():
        print(f"{key}. {desc}")
    print("q. Quit")
    
    while True:
        choice = input("\nSelect test to run (1-4 or q): ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            break
        elif choice in playlists:
            desc, playlist = playlists[choice]
            run_playlist(playlist, desc, pause_between=1.5)
            
            cont = input("\nRun another test? (y/n): ").strip().lower()
            if cont != 'y':
                break
        else:
            print("Invalid choice. Please enter 1-4 or q.")

def single_test(transition_name):
    """Test a single transition by name."""
    transitions = {
        "plain": ("Double Height Plain", double_height_plain, "TEST"),
        "scroll": ("Double Height Scroll", double_height_scroll, "SCROLLING"), 
        "type": ("Double Height Typewriter", double_height_typewriter, "TYPE"),
        "pop": ("Double Height Pop", double_height_pop, "POP"),
        "wave": ("Double Height Wave", double_height_wave, "WAVE"),
        "magic": ("Double Height Magic", double_height_magic_reveal, "MAGIC"),
        "mixed": ("Mixed Mode", mixed_announcement, "BIG - small text"),
        "smart": ("Smart Selection", smart_transition, "AUTO"),
    }
    
    if transition_name.lower() in transitions:
        desc, func, param = transitions[transition_name.lower()]
        print(f"\n🎯 Testing: {desc}")
        try:
            func(param)
            print(f"✅ {desc} completed successfully")
        except Exception as e:
            print(f"❌ {desc} failed: {e}")
        finally:
            clear()
    else:
        print(f"Unknown transition: {transition_name}")
        print("Available: " + ", ".join(transitions.keys()))

if __name__ == "__main__":
    print("🎮 Double Height Text Test System")
    print("=" * 50)
    
    # Check if command line argument provided
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            run_playlist(QUICK_DEMO_PLAYLIST, "Quick Demo", pause_between=1.0)
        elif command == "full":
            run_playlist(DOUBLE_HEIGHT_TEST_PLAYLIST, "Full Test", pause_between=2.0)
        elif command == "compare":
            run_playlist(COMPARISON_PLAYLIST, "Comparison Test", pause_between=2.0)
        elif command in ["plain", "scroll", "type", "pop", "wave", "magic", "mixed", "smart"]:
            single_test(command)
        else:
            print(f"Unknown command: {command}")
            print("Usage: python test_playlist.py [quick|full|compare|plain|scroll|type|pop|wave|magic|mixed|smart]")
    else:
        # Interactive mode
        interactive_test()
    
    print("\nTest session ended.")
