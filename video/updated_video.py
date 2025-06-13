#!/usr/bin/env python3
"""
Updated Video Module for Reconfigurable Flipdot Display

This module handles video frame conversion and playback for any display configuration.
"""

import glob
import os
import time
from subprocess import Popen
from PIL import Image
from typing import Optional, List
from core.reconfigurable_flipdot import ReconfigurableFlipdotDisplay

__author__ = 'boselowitz (updated version)'

# Configuration
FFMPEG = "ffmpeg"
VIDEOS_DIR = os.path.join(os.path.dirname(__file__), "videos")
FRAMES_DIR = os.path.join(os.path.dirname(__file__), "frames")
FRAME_FILE_TYPES = ["*.png", "*.jpg", "*.gif", "*.bmp"]
DEFAULT_FPS = 12.0

# Global display instance
display: Optional[ReconfigurableFlipdotDisplay] = None

def set_display(flipdot_display: ReconfigurableFlipdotDisplay):
    """Set the global display instance for video playback."""
    global display
    display = flipdot_display

def ensure_display():
    """Ensure we have a display instance."""
    global display
    if display is None:
        from core.reconfigurable_flipdot import create_display
        display = create_display()

def convert_video_to_frames(video_name: str, fps: float = DEFAULT_FPS, 
                           target_width: Optional[int] = None, 
                           target_height: Optional[int] = None) -> bool:
    """
    Convert a video file to individual frames sized for the display.
    
    Args:
        video_name: Name of the video file in the videos directory
        fps: Frames per second to extract
        target_width: Target width (uses display width if None)
        target_height: Target height (uses display height if None)
        
    Returns:
        True if successful, False otherwise
    """
    ensure_display()
    
    if target_width is None:
        target_width = display.config.total_width
    if target_height is None:
        target_height = display.config.total_height
    
    frames_path = os.path.join(FRAMES_DIR, video_name)
    
    # Create directories if they don't exist
    if not os.path.exists(FRAMES_DIR):
        os.makedirs(FRAMES_DIR)
    if not os.path.exists(frames_path):
        os.makedirs(frames_path)
    
    full_video_path = os.path.abspath(os.path.join(VIDEOS_DIR, video_name))
    
    if not os.path.exists(full_video_path):
        print(f"Video file not found: {full_video_path}")
        return False
    
    starting_dir = os.getcwd()
    
    try:
        os.chdir(frames_path)
        
        # Build ffmpeg command with scaling
        cmd = [
            FFMPEG,
            "-i", full_video_path,
            "-r", str(fps),
            "-vf", f"scale={target_width}:{target_height}:flags=neighbor",
            "-vcodec", "png",
            "-y",  # Overwrite existing files
            "%05d.png"
        ]
        
        print(f"Converting {video_name} to {target_width}×{target_height} frames at {fps} FPS...")
        p = Popen(cmd)
        p.wait()
        
        if p.returncode == 0:
            print(f"Successfully converted {video_name}")
            return True
        else:
            print(f"Error converting {video_name} (return code: {p.returncode})")
            return False
            
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False
    finally:
        os.chdir(starting_dir)

def display_video(video_name: str, fps: float = DEFAULT_FPS, loop: bool = False, 
                 brightness_threshold: int = 128) -> None:
    """
    Display a video on the flipdot display.
    
    Args:
        video_name: Name of the video (should have frames in frames directory)
        fps: Playback frame rate
        loop: Whether to loop the video
        brightness_threshold: Threshold for converting grayscale to binary
    """
    ensure_display()
    
    frames_path = os.path.join(FRAMES_DIR, video_name)
    
    if not os.path.exists(frames_path):
        print(f"Frames directory not found: {frames_path}")
        print(f"Try running convert_video_to_frames('{video_name}') first")
        return
    
    # Get all image files
    image_files = []
    for file_type in FRAME_FILE_TYPES:
        image_files.extend(glob.glob(os.path.join(frames_path, file_type)))
    
    if not image_files:
        print(f"No frame files found in {frames_path}")
        return
    
    image_files = sorted(image_files)
    frame_delay = 1.0 / fps
    
    print(f"Playing {len(image_files)} frames at {fps} FPS")
    
    try:
        while True:
            for image_file in image_files:
                frame_data = convert_image_to_frame_data(image_file, brightness_threshold)
                if frame_data:
                    display.display_frame(frame_data)
                time.sleep(frame_delay)
            
            if not loop:
                break
                
    except KeyboardInterrupt:
        print("\nVideo playback interrupted")
    
    print("Video playback finished")

def convert_image_to_frame_data(image_path: str, brightness_threshold: int = 128) -> Optional[bytes]:
    """
    Convert an image file to frame data for the flipdot display.
    
    Args:
        image_path: Path to the image file
        brightness_threshold: Threshold for converting to binary (0-255)
        
    Returns:
        Bytes representing the frame, or None if error
    """
    ensure_display()
    
    try:
        # Open and process the image
        image = Image.open(image_path)
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Resize to match display dimensions
        image = image.resize((display.config.total_width, display.config.total_height), Image.NEAREST)
        
        # Get pixel data
        pixels = list(image.getdata())
        
        # Convert to frame data
        frame_data = b''
        
        if display.config.modules_high == 1:
            # Single row of modules - standard conversion
            frame_data = convert_pixels_single_row(pixels, display.config.total_width, 
                                                 display.config.total_height, brightness_threshold)
        else:
            # Multiple rows of modules - split the image
            frame_data = convert_pixels_multi_row(pixels, display.config, brightness_threshold)
        
        return frame_data
        
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def convert_pixels_single_row(pixels: List[int], width: int, height: int, 
                            threshold: int) -> bytes:
    """Convert pixels for a single row of modules."""
    frame_data = b''
    
    for col in range(width):
        col_byte = 0
        for row in range(min(height, 7)):  # Max 7 bits per byte
            pixel_idx = (row * width) + col
            if pixel_idx < len(pixels):
                if pixels[pixel_idx] > threshold:
                    col_byte |= (1 << (6 - row))  # Set bit for bright pixels
        
        frame_data += bytes([col_byte])
    
    return frame_data

def convert_pixels_multi_row(pixels: List[int], config, threshold: int) -> bytes:
    """Convert pixels for multiple rows of modules."""
    frame_data = b''
    
    # Process each column
    for col in range(config.total_width):
        # For displays with multiple module rows, we need to handle each module row separately
        module_row_height = config.module_height
        
        for module_row in range(config.modules_high):
            col_byte = 0
            
            # Process each row within this module
            for bit_row in range(module_row_height):
                actual_row = (module_row * module_row_height) + bit_row
                pixel_idx = (actual_row * config.total_width) + col
                
                if pixel_idx < len(pixels) and pixels[pixel_idx] > threshold:
                    col_byte |= (1 << (module_row_height - 1 - bit_row))
            
            frame_data += bytes([col_byte])
    
    return frame_data

def display_image(image_path: str, duration: float = 2.0, 
                 brightness_threshold: int = 128) -> None:
    """
    Display a single image on the flipdot display.
    
    Args:
        image_path: Path to the image file
        duration: How long to display the image (seconds)
        brightness_threshold: Threshold for converting to binary
    """
    ensure_display()
    
    frame_data = convert_image_to_frame_data(image_path, brightness_threshold)
    if frame_data:
        display.display_frame(frame_data)
        time.sleep(duration)
    else:
        print(f"Failed to display image: {image_path}")

def create_test_pattern() -> None:
    """Create and display a test pattern to verify display configuration."""
    ensure_display()
    
    print(f"Displaying test pattern for {display.config.total_width}×{display.config.total_height} display")
    
    # Create checkerboard pattern
    frame_data = b''
    for col in range(display.config.total_width):
        col_byte = 0
        for row in range(min(display.config.module_height, 7)):
            if (col + row) % 2 == 0:
                col_byte |= (1 << (display.config.module_height - 1 - row))
        frame_data += bytes([col_byte])
    
    display.display_frame(frame_data)
    time.sleep(3)
    
    # Create vertical stripes
    frame_data = b''
    for col in range(display.config.total_width):
        if col % 2 == 0:
            col_byte = 0x7F  # All bits on
        else:
            col_byte = 0x00  # All bits off
        frame_data += bytes([col_byte])
    
    display.display_frame(frame_data)
    time.sleep(3)
    
    # Create horizontal stripes  
    frame_data = b''
    for col in range(display.config.total_width):
        col_byte = 0x55  # Alternating bits: 01010101
        frame_data += bytes([col_byte])
    
    display.display_frame(frame_data)
    time.sleep(3)
    
    display.clear()

def get_video_info(video_name: str) -> dict:
    """
    Get information about a video file.
    
    Args:
        video_name: Name of the video file
        
    Returns:
        Dictionary with video information
    """
    full_video_path = os.path.join(VIDEOS_DIR, video_name)
    frames_path = os.path.join(FRAMES_DIR, video_name)
    
    info = {
        'video_exists': os.path.exists(full_video_path),
        'frames_exist': os.path.exists(frames_path),
        'video_path': full_video_path,
        'frames_path': frames_path,
        'frame_count': 0
    }
    
    if info['frames_exist']:
        image_files = []
        for file_type in FRAME_FILE_TYPES:
            image_files.extend(glob.glob(os.path.join(frames_path, file_type)))
        info['frame_count'] = len(image_files)
    
    return info

# Convenience functions for common operations
def quick_play(video_name: str, auto_convert: bool = True, **kwargs) -> None:
    """
    Quickly play a video, converting frames if necessary.
    
    Args:
        video_name: Name of the video file
        auto_convert: Whether to automatically convert video to frames if needed
        **kwargs: Additional arguments for display_video
    """
    info = get_video_info(video_name)
    
    if not info['video_exists']:
        print(f"Video file not found: {video_name}")
        return
    
    if not info['frames_exist'] or info['frame_count'] == 0:
        if auto_convert:
            print(f"Converting {video_name} to frames...")
            if not convert_video_to_frames(video_name):
                print("Failed to convert video")
                return
        else:
            print(f"No frames found for {video_name}. Use auto_convert=True or run convert_video_to_frames() first.")
            return
    
    display_video(video_name, **kwargs)

# Export main functions
__all__ = [
    'set_display', 'convert_video_to_frames', 'display_video', 'display_image',
    'create_test_pattern', 'get_video_info', 'quick_play'
]
