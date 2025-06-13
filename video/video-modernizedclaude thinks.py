#!/usr/bin/env python3
"""
Video Module for Flipdot Display

This module handles converting and playing video files on the flipdot display.
It supports extracting frames from videos and displaying them at a configurable framerate.
"""

import glob
import os
import time
import subprocess
from typing import List, Callable, Optional, Union, ByteString
from pathlib import Path
from PIL import Image
from core import FlipdotDisplay

__author__ = 'boselowitz (modernized version)'

# Configuration
FFMPEG = "ffmpeg"
VIDEOS_DIR = Path(__file__).parent / "videos"
FRAMES_DIR = Path(__file__).parent / "frames"
FRAME_FILE_TYPES = ["*.png", "*.jpg", "*.gif"]
FPS = 12.0

# Create a display instance
display = FlipdotDisplay()


def threshold_function(pixel_value: int) -> int:
    """
    Threshold function to convert grayscale to binary.
    
    Args:
        pixel_value: Grayscale value between 0-255
        
    Returns:
        Binary value (0 or 255)
    """
    return 255 if pixel_value > 20 else 0


def display_video(video_name: str) -> bool:
    """
    Display a video on the flipdot display.
    
    Args:
        video_name: Name of the video (folder in frames directory)
        
    Returns:
        True if successful, False otherwise
    """
    # Get all image files matching the supported types
    image_files = []
    frames_path = FRAMES_DIR / video_name
    
    for image_type in FRAME_FILE_TYPES:
        image_files.extend(glob.glob(str(frames_path / image_type)))
    
    if not image_files:
        print(f"Could not find frames for video '{video_name}' in {frames_path}")
        return False
    
    # Sort the files to ensure proper sequence
    image_files = sorted(image_files)
    
    # Process and display each frame
    for image_file in image_files:
        try:
            # Open and convert the image to binary (1-bit)
            image = Image.open(image_file)
            image = image.convert("1")  # Convert to binary
            # Alternative: use custom threshold function
            # image = image.point(threshold_function)
            
            # Get image dimensions and pixel data
            width, height = image.size
            image_data = list(image.getdata())
            
            # Convert image data to flipdot format
            fill_value = bytearray()
            for col in range(width):
                col_value = 0
                for row in range(height):
                    pixel = image_data[(row * width) + col]
                    if pixel:  # If pixel is set (white in binary mode)
                        col_value |= display.BITMASK[6 - row]
                fill_value.append(col_value)
            
            # Display the frame
            display.fill(bytes(fill_value))
            
            # Wait for next frame
            time.sleep(1.0 / FPS)
            
        except Exception as e:
            print(f"Error displaying frame {image_file}: {e}")
            continue
    
    return True


def convert_video_to_frames(video_name: str) -> bool:
    """
    Convert a video file to a sequence of frames using ffmpeg.
    
    Args:
        video_name: Name of the video file in the videos directory
        
    Returns:
        True if successful, False otherwise
    """
    # Create output directory if it doesn't exist
    frames_path = FRAMES_DIR / video_name
    frames_path.mkdir(parents=True, exist_ok=True)
    
    # Get full path to the video file
    full_video_path = VIDEOS_DIR / video_name
    
    if not full_video_path.exists():
        print(f"Video file not found: {full_video_path}")
        return False
    
    # Save current directory
    starting_dir = os.getcwd()
    
    try:
        # Change to frames directory
        os.chdir(frames_path)
        
        # Run ffmpeg to extract frames
        cmd = [
            FFMPEG,
            "-r", str(FPS),
            "-i", str(full_video_path),
            "-vcodec", "png",
            "%5d.png"
        ]
        
        # Execute ffmpeg command
        process = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if process.returncode != 0:
            print(f"Error converting video: {process.stderr.decode()}")
            return False
        
        print(f"Successfully converted video '{video_name}' to frames")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg: {e}")
        return False
    
    except Exception as e:
        print(f"Error converting video: {e}")
        return False
    
    finally:
        # Return to original directory
        os.chdir(starting_dir)


def list_available_videos() -> List[str]:
    """
    List all available videos in the frames directory.
    
    Returns:
        List of video names (directory names)
    """
    if not FRAMES_DIR.exists():
        return []
    
    return [d.name for d in FRAMES_DIR.iterdir() if d.is_dir()]


def prepare_and_display_video(video_name: str) -> bool:
    """
    Prepare a video (convert if needed) and display it.
    
    Args:
        video_name: Name of the video file or directory
        
    Returns:
        True if successful, False otherwise
    """
    # Check if frames already exist
    frames_path = FRAMES_DIR / video_name
    
    if not frames_path.exists() or not any(frames_path.glob(pattern) for pattern in FRAME_FILE_TYPES):
        print(f"Frames not found for '{video_name}', converting from video...")
        if not convert_video_to_frames(video_name):
            print(f"Failed to convert video '{video_name}'")
            return False
    
    # Display the video
    return display_video(video_name)


if __name__ == "__main__":
    # Example usage when run directly
    print("Video Module for Flipdot Display")
    print("Available videos:")
    
    videos = list_available_videos()
    for idx, video in enumerate(videos, 1):
        print(f"{idx}. {video}")
    
    if not videos:
        print("No videos found. Use convert_video_to_frames() to prepare videos.")
