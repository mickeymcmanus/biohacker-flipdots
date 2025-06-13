#!/usr/bin/env python3
"""
Scavenger Hunt Module

This module manages a Twitter-based scavenger hunt game, tracking puzzles, user progress,
and displaying results on a flipdot display.
"""

import os
import json
import time
import random
from typing import Dict, List, Tuple, Any, Optional, Union, Iterator
from pathlib import Path
from transition import transition
from twitter import twitter

__author__ = 'boselowitz (modernized version)'

# Constants
PUZZLES_DIR = Path(__file__).parent / "puzzles"
DATA_DIR = Path(__file__).parent / "data"
DATA_EXT = ".json"

# Global state (could be moved to class in further refactoring)
current_puzzle_index = 0
individual_stats_text = "You have successfully completed %d out of %d riddles."


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON data from a file with proper error handling.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return {}


def save_json_file(data: Dict[str, Any], file_path: Path) -> bool:
    """
    Save data to a JSON file with proper error handling.
    
    Args:
        data: Data to save
        file_path: Path to save the data
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


def compile_data() -> None:
    """
    Process Twitter mentions to update scavenger hunt progress.
    Updates user records based on hashtags in tweets that match puzzle solutions.
    """
    # Load the current puzzle
    current_puzzle_path = PUZZLES_DIR / "main_puzzle.json"
    current_puzzle = load_json_file(current_puzzle_path)
    if not current_puzzle:
        return

    # Load or initialize user data
    current_puzzle_data_path = DATA_DIR / f"{current_puzzle['name']}{DATA_EXT}"
    current_puzzle_data = load_json_file(current_puzzle_data_path)
    
    # Get latest mentions from Twitter
    mentions = twitter.get_latest_mentions()
    for mention in mentions:
        username = mention["user"]["screen_name"]

        # Initialize user data if this is their first interaction
        if username not in current_puzzle_data:
            current_puzzle_data[username] = {
                "complete": [],
                "complete_count": 0,
                "incomplete": [p["name"] for p in current_puzzle["puzzles"]],
                "incomplete_count": current_puzzle["puzzle_count"]
            }

        print(mention)
        
        # Check all puzzles against the hashtags in the mention
        for puzzle in current_puzzle["puzzles"]:
            name = ""
            key = ""
            
            # Look for matching hashtags
            for hashtag in mention["entities"]["hashtags"]:
                hashtag_text = hashtag["text"]
                
                # Check if hashtag is a valid key for this puzzle
                if hashtag_text in puzzle["keys"]:
                    key = hashtag_text
                
                # Check if hashtag matches the puzzle name
                if puzzle["name"] == hashtag_text:
                    name = hashtag_text

            # If user solved a puzzle (found both name and key)
            if key and name:
                print(f"{username} solved puzzle {name} with key {key}")

                # Check if already completed
                if puzzle["name"] not in current_puzzle_data[username]["complete"]:
                    # Update user's progress
                    current_puzzle_data[username]["complete"].append(puzzle["name"])
                    current_puzzle_data[username]["complete_count"] = len(current_puzzle_data[username]["complete"])
                    
                    # Remove from incomplete list
                    if puzzle["name"] in current_puzzle_data[username]["incomplete"]:
                        current_puzzle_data[username]["incomplete"].remove(puzzle["name"])
                    
                    current_puzzle_data[username]["incomplete_count"] = len(current_puzzle_data[username]["incomplete"])
                    
                    # Save user data
                    save_json_file(current_puzzle_data, current_puzzle_data_path)

                    # Remove used key and save puzzle
                    if key in puzzle["keys"]:
                        puzzle["keys"].remove(key)
                    
                    save_json_file(current_puzzle, current_puzzle_path)
                    
                    # Send success tweet
                    success_message = random.choice(current_puzzle["successful_responses"])
                    stats = individual_stats_text % (
                        current_puzzle_data[username]["complete_count"],
                        current_puzzle["puzzle_count"]
                    )
                    twitter.send_tweet(f"@{username} {success_message} {stats}")
                    return
                else:
                    # User already completed this puzzle
                    twitter.send_tweet(f"@{username} you already completed this riddle.")
                    return

        # Failed to complete any puzzle
        fail_message = random.choice(current_puzzle["fail_responses"])
        stats = individual_stats_text % (
            current_puzzle_data[username]["complete_count"],
            current_puzzle["puzzle_count"]
        )
        twitter.send_tweet(f"@{username} {fail_message} {stats}")


def display_riddle(name: Optional[str] = None) -> None:
    """
    Display a riddle on the flipdot display.
    
    Args:
        name: Optional specific riddle name to display
    """
    global current_puzzle_index
    
    # Load the current puzzle
    current_puzzle_path = PUZZLES_DIR / "main_puzzle.json"
    current_puzzle = load_json_file(current_puzzle_path)
    if not current_puzzle or "puzzles" not in current_puzzle:
        print("No valid puzzle found")
        return

    # Display the current riddle
    transition.righttoleft(current_puzzle["puzzles"][current_puzzle_index]["display_text"])
    
    # Cycle to the next riddle
    current_puzzle_index += 1
    current_puzzle_index %= current_puzzle["puzzle_count"]


def display_leader_board() -> None:
    """Display the scavenger hunt leaderboard on the flipdot display."""
    # First update data from latest tweets
    compile_data()

    # Load the current puzzle
    current_puzzle_path = PUZZLES_DIR / "main_puzzle.json"
    current_puzzle = load_json_file(current_puzzle_path)
    if not current_puzzle:
        return

    # Load user data
    current_puzzle_data_path = DATA_DIR / f"{current_puzzle['name']}{DATA_EXT}"
    current_puzzle_data = load_json_file(current_puzzle_data_path)
    
    # Sort users by complete count (highest first)
    leader_board = sorted(
        current_puzzle_data.items(),
        key=lambda x: x[1]["complete_count"],
        reverse=True
    )

    if leader_board:
        # Display leaderboard header
        transition.righttoleft("NAMII Scavenger Hunt Leader Board")
        
        # Display top 5 users
        for i, (username, data) in enumerate(leader_board[:5]):
            transition.righttoleft(
                f"#{i+1} {username} with ({data['complete_count']}/{current_puzzle['puzzle_count']})"
            )


if __name__ == "__main__":
    # Example usage when run directly
    print("Scavenger Hunt Module")
    print("Use this module by importing it and calling its functions.")
