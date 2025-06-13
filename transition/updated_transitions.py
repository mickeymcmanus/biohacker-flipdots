#!/usr/bin/env python3
"""
Updated Transition Module for Reconfigurable Flipdot Display

This module provides text transition effects that work with any display configuration.
"""

import time
import random
from typing import Optional
from core.reconfigurable_flipdot import ReconfigurableFlipdotDisplay, TextHeight, Justify

# Global display instance - will be set by the main script
display: Optional[ReconfigurableFlipdotDisplay] = None

def set_display(flipdot_display: ReconfigurableFlipdotDisplay):
    """Set the global display instance for all transitions."""
    global display
    display = flipdot_display

def ensure_display():
    """Ensure we have a display instance."""
    global display
    if display is None:
        from core.reconfigurable_flipdot import create_display
        display = create_display()

####################
# BASE TRANSITIONS #
####################

def upnext(message: str):
    """Animated 'UP NEXT' transition followed by the message."""
    ensure_display()
    
    # Flash "UP NEXT" multiple times
    for j in range(3):
        for i in range(5):
            # Show "UP NEXT" normally
            display.display_text("UP NEXT", TextHeight.SINGLE, Justify.CENTER, scroll=False)
            time.sleep(0.25)
            
            # Show "UP NEXT" inverted (we'll simulate this with clearing)
            display.clear()
            time.sleep(0.2)
            
            display.display_text("UP NEXT", TextHeight.SINGLE, Justify.CENTER, scroll=False)
            time.sleep(0.1)
            
            display.clear()
            time.sleep(0.2)
        
        # Show the actual message
        if j == 2:
            # Final message with center justification and scrolling
            display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=True, scroll_speed=0.15)
        else:
            # Intermediate message displays
            display.display_text(message, TextHeight.AUTO, scroll=True, scroll_speed=0.15)
    
    # End with a pacman-style animation (placeholder for now)
    display.display_text("< < < < <", TextHeight.SINGLE, scroll=True, scroll_speed=0.1)

def righttoleft(message: str):
    """Simple right-to-left scrolling text."""
    ensure_display()
    display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=True, scroll_speed=0.2)

def pop(message: str):
    """Flashing pop effect."""
    ensure_display()
    display.clear()
    
    for i in range(7):
        display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=False)
        time.sleep(0.25)
        display.clear()
        time.sleep(0.25)
    
    display.clear()
    time.sleep(1)

def dissolve(message: str):
    """Dissolve effect - show message then fade out."""
    ensure_display()
    
    # Show the message
    display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=False)
    time.sleep(2)
    
    # Simulate dissolve with random clearing
    text_bytes = display.get_text_bytes(message)
    for _ in range(10):
        # This is a simplified version - you could implement actual pixel-level dissolve
        display.clear()
        time.sleep(0.1)
        display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=False)
        time.sleep(0.1)
    
    display.clear()

def magichat(message: str):
    """Multi-screen text display with bottom-up reveal."""
    ensure_display()
    
    # Split long messages into screens that fit the display
    screens = split_message_to_screens(message)
    
    for screen_text in screens:
        # Simulate bottom-up fill (simplified)
        display.clear()
        time.sleep(0.2)
        display.display_text(screen_text, TextHeight.AUTO, Justify.CENTER, scroll=False)
        time.sleep(1)
        
        # Simulate scroll up effect
        display.clear()

def adventurelook(message: str):
    """Adventure game style text display."""
    ensure_display()
    
    screens = split_message_to_screens(message)
    
    for i, screen_text in enumerate(screens):
        display.clear()
        time.sleep(0.2)
        display.display_text(screen_text, TextHeight.AUTO, Justify.CENTER, scroll=False)
        
        if i == len(screens) - 1:
            time.sleep(5)  # Longer pause for last screen
        else:
            time.sleep(1)
            display.clear()
            time.sleep(0.5)

def plain(message: str):
    """Simple scrolling text display."""
    ensure_display()
    display.display_text(message, TextHeight.AUTO, scroll=True)

def typewriter(message: str):
    """Typewriter effect - reveal characters one by one."""
    ensure_display()
    
    for i in range(1, len(message) + 1):
        partial_message = message[:i]
        display.display_text(partial_message, TextHeight.AUTO, Justify.LEFT, scroll=False)
        time.sleep(0.1)
    
    time.sleep(2)

def wave(message: str):
    """Wave effect - text moves up and down."""
    ensure_display()
    
    # This is a simplified version - could be enhanced with actual wave motion
    for _ in range(5):
        display.display_text(message, TextHeight.SINGLE, Justify.CENTER, scroll=False)
        time.sleep(0.3)
        display.display_text(message, TextHeight.DOUBLE, Justify.CENTER, scroll=False)
        time.sleep(0.3)

def bounce(message: str):
    """Bouncing text effect."""
    ensure_display()
    
    for _ in range(6):
        display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=False)
        time.sleep(0.2)
        display.clear()
        time.sleep(0.1)
        display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=False)
        time.sleep(0.2)

#################################
# UTILITY FUNCTIONS             #
#################################

def split_message_to_screens(message: str, max_chars_per_screen: int = None) -> list:
    """
    Split a long message into multiple screens.
    
    Args:
        message: The message to split
        max_chars_per_screen: Maximum characters per screen (auto-calculated if None)
        
    Returns:
        List of message chunks
    """
    ensure_display()
    
    if max_chars_per_screen is None:
        # Estimate based on display width and character width
        # Assuming average 5 pixels per character + 1 pixel spacing
        max_chars_per_screen = display.config.total_width // 6
    
    if len(message) <= max_chars_per_screen:
        return [message]
    
    screens = []
    words = message.split()
    current_screen = ""
    
    for word in words:
        test_screen = current_screen + (" " if current_screen else "") + word
        if len(test_screen) <= max_chars_per_screen:
            current_screen = test_screen
        else:
            if current_screen:
                screens.append(current_screen)
            current_screen = word
    
    if current_screen:
        screens.append(current_screen)
    
    return screens

#################################
# TRANSITION LIST MANAGEMENT    #
#################################

# Available transitions organized by type
TRANSITION_LIST = [plain, upnext, magichat, adventurelook, typewriter, wave, bounce]
GENERAL_TRANSITION_LIST = [plain, magichat, adventurelook, typewriter, wave]
ANNOUNCEMENT_TRANSITION_LIST = [upnext, pop, bounce]
SPECIAL_TRANSITION_LIST = [dissolve, typewriter, wave, bounce]

def random_pick(pick_list: list):
    """Randomly select a transition from the given list."""
    return random.choice(pick_list)

def random(message: str):
    """Apply a random transition from all available transitions."""
    random_pick(TRANSITION_LIST)(message)

def randomgeneral(message: str):
    """Apply a random general transition."""
    random_pick(GENERAL_TRANSITION_LIST)(message)

def randomannouncement(message: str):
    """Apply a random announcement-style transition."""
    random_pick(ANNOUNCEMENT_TRANSITION_LIST)(message)

def randomspecial(message: str):
    """Apply a random special effect transition."""
    random_pick(SPECIAL_TRANSITION_LIST)(message)

#################################
# ADVANCED TRANSITIONS          #
#################################

def matrix_effect(message: str):
    """Matrix-style digital rain effect before showing message."""
    ensure_display()
    
    # Simulate matrix effect with random characters
    matrix_chars = "01"
    
    for _ in range(20):
        random_text = ''.join(random.choice(matrix_chars) for _ in range(display.config.total_width // 6))
        display.display_text(random_text, TextHeight.SINGLE, Justify.LEFT, scroll=False)
        time.sleep(0.1)
    
    display.clear()
    time.sleep(0.5)
    display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=True)

def slide_in_left(message: str):
    """Slide text in from the left side."""
    ensure_display()
    
    text_bytes = display.get_text_bytes(message)
    width = display.config.total_width
    
    # Animate sliding in from left
    for i in range(width + 1):
        padded = b'\x00' * (width - i) + text_bytes[:i]
        if len(padded) > width:
            padded = padded[:width]
        elif len(padded) < width:
            padded += b'\x00' * (width - len(padded))
            
        display.serial.write(b'\x81\x82')  # RESET + ROW1
        display.serial.write(padded)
        time.sleep(0.05)
    
    time.sleep(2)

def slide_in_right(message: str):
    """Slide text in from the right side."""
    ensure_display()
    
    text_bytes = display.get_text_bytes(message)
    width = display.config.total_width
    
    # Animate sliding in from right
    for i in range(width + 1):
        padded = text_bytes[:i] + b'\x00' * (width - i)
        if len(padded) > width:
            padded = padded[-width:]
        elif len(padded) < width:
            padded = b'\x00' * (width - len(padded)) + padded
            
        display.serial.write(b'\x81\x82')  # RESET + ROW1
        display.serial.write(padded)
        time.sleep(0.05)
    
    time.sleep(2)

def center_zoom(message: str):
    """Zoom effect from center outward."""
    ensure_display()
    
    # Start with a single character in center and expand
    for i in range(1, len(message) + 1):
        partial = message[:i]
        display.display_text(partial, TextHeight.AUTO, Justify.CENTER, scroll=False)
        time.sleep(0.15)
    
    time.sleep(2)

def spiral_text(message: str):
    """Display text with a spiral reveal effect."""
    ensure_display()
    
    # This is a simplified spiral - just rotate through different justifications
    justifications = [Justify.LEFT, Justify.CENTER, Justify.RIGHT, Justify.CENTER]
    
    for i, justify in enumerate(justifications * 3):
        display.display_text(message, TextHeight.AUTO, justify, scroll=False)
        time.sleep(0.3)
    
    # Final centered display
    display.display_text(message, TextHeight.AUTO, Justify.CENTER, scroll=False)
    time.sleep(2)

#################################
# COMPATIBILITY LAYER           #
#################################

# For backward compatibility with existing scripts
def amdissolve(message: str):
    """AMD-style dissolve effect (alias for dissolve)."""
    dissolve(message)

# Add the new transitions to the lists
TRANSITION_LIST.extend([matrix_effect, slide_in_left, slide_in_right, center_zoom, spiral_text])
SPECIAL_TRANSITION_LIST.extend([matrix_effect, slide_in_left, slide_in_right, center_zoom, spiral_text])

# Export all transition functions for easy access
__all__ = [
    'upnext', 'righttoleft', 'pop', 'dissolve', 'magichat', 'adventurelook',
    'plain', 'typewriter', 'wave', 'bounce', 'matrix_effect', 'slide_in_left',
    'slide_in_right', 'center_zoom', 'spiral_text', 'amdissolve',
    'random', 'randomgeneral', 'randomannouncement', 'randomspecial',
    'set_display', 'TRANSITION_LIST', 'GENERAL_TRANSITION_LIST', 
    'ANNOUNCEMENT_TRANSITION_LIST', 'SPECIAL_TRANSITION_LIST'
]