#!/usr/bin/env python3
"""
Adventure Game

A text-based adventure game where the player must defeat the evil Dragon named Kibbles
and rescue Princess Catherine.

Original by Andrew D. Sapolnick, David Lear, Suved Adkar (C)2010
Modernized version, 2025

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from enum import Enum, auto
from typing import List, Optional


class Location(Enum):
    """Enum representing game locations."""
    TOWN = auto()
    FOREST = auto()
    MINE = auto()
    LAIR = auto()
    DEAD = auto()  # End state


class GameState(Enum):
    """Enum representing game states."""
    RUNNING = auto()
    WIN = auto()
    LOSE = auto()


class AdventureGame:
    """Main game class for the adventure game."""
    
    def __init__(self):
        """Initialize the game state."""
        self.items: List[str] = []
        self.location = Location.TOWN
        self.state = GameState.RUNNING
        
        # Welcome message
        self.display_welcome()
    
    def display_welcome(self) -> None:
        """Display the welcome message for the game."""
        print(
            "Welcome to the Adventure Game, here you will embark on a dangerous journey to "
            "defeat the evil Dragon named Kibbles, and rescue Princess Catherine. Your story "
            "begins in the small town of Jersey."
        )
        print("\nCommands:")
        self.display_commands()
    
    def display_commands(self) -> None:
        """Display the available commands."""
        print("- north, south, east, west: Navigate in that direction")
        print("- use [item] [target]: Use an item on a target")
        print("- inventory: Look at the items in your possession")
        print("- look: Look around your current location")
        print("- search [target]: Search for people or items")
        print("- commands: Show these instructions again")
        print("\nGood luck on your quest!")
    
    def run(self) -> None:
        """Main game loop."""
        while self.state == GameState.RUNNING:
            if self.location == Location.TOWN:
                self.handle_town()
            elif self.location == Location.FOREST:
                self.handle_forest()
            elif self.location == Location.MINE:
                self.handle_mine()
            elif self.location == Location.LAIR:
                self.handle_lair()
            elif self.location == Location.DEAD:
                break
        
        # End game messages
        if self.state == GameState.WIN:
            print("\nCongratulations! You beat the Adventure game! Thank you for playing!")
        elif self.state == GameState.LOSE:
            print("\nThank you for playing. Try again and see if you can rescue Princess Catherine!")
        
        input("\nPress enter to exit the program")
    
    def handle_town(self) -> None:
        """Handle player actions in the town."""
        direction = input("\nWhat would you like to do?\n").lower().strip()
        
        if direction == "west":
            has_blacksmith_materials = all(item in self.items for item in ["iron ore", "wood", "3 Gold Pieces"])
            
            if has_blacksmith_materials:
                print("The blacksmith greets you, and you tell him that you have the items and money he requires. "
                      "You also give him the saw to make up for some of the difference. He then forges you a "
                      "battleaxe and wishes you luck on the rest of your quest.")
                
                # Remove used items
                for item in ["saw", "3 Gold Pieces", "iron ore", "wood"]:
                    self.items.remove(item)
                
                # Add battleaxe
                self.items.append("battleaxe")
            else:
                print("You are at the blacksmith shop, many different kinds of weapons decorate the walls. "
                      "The blacksmith is a tall, hairy man who smiles as you enter the door. You tell him "
                      "that you need a weapon to kill Kibbles the Evil Dragon. He laughs and says 'Mah boy! "
                      "Killing Kibbles is what all true warriors strive for! But you can't do it with any of "
                      "my weapons, you need Atari, the magic sword that lies in the cave east of the forest. "
                      "Many have tried to get it, but all have failed as it is guarded by the evil wizard Gwonam! "
                      "If you're looking to fight Gwonam, I can make you an axe, but you need to bring me iron ore, "
                      "wood, and some gold for my troubles.' You then decide to head into the forest to seek out "
                      "the materials for the blacksmith.")
        
        elif direction == "north":
            print("You walk up to the gates of the king's castle. The guards stop and ask you to state your business. "
                  "You tell them that you want to rescue Princess Catherine. They laugh and tell you that you should "
                  "probably obtain a weapon first. You head back to the center of town.")
        
        elif direction == "east":
            print("You head into the residential district of town. A few huts line the streets, but there isn't "
                  "much else of note here. You decide to head back to the center of town.")
        
        elif direction == "south":
            print("You head deep into the forest.")
            self.location = Location.FOREST
        
        elif direction == "commands":
            self.display_commands()
        
        elif direction == "inventory":
            if self.items:
                print(f"Your inventory: {', '.join(self.items)}")
            else:
                print("Your inventory is empty.")
        
        elif direction == "look":
            print("You're located in the small town of Jersey. Here you see a blacksmith shop to the west, "
                  "the king's castle to the north, houses to the east, and the town's exit to the forest to your south.")
        
        elif direction.startswith("use"):
            print("You have nothing to use here.")
        
        elif direction.startswith("search"):
            print("There's nothing of importance to search here.")
        
        else:
            print("Please enter a valid command.")
    
    def handle_forest(self) -> None:
        """Handle player actions in the forest."""
        direction = input("\nWhat would you like to do?\n").lower().strip()
        
        if direction == "west":
            print("You head into the mine.")
            self.location = Location.MINE
        
        elif direction == "south":
            print("The mountains look too treacherous to try and pass through. "
                  "It might not hurt to try and look for that man though.")
        
        elif direction == "east":
            if "battleaxe" in self.items:
                print("You head into Gwonam's Lair.")
                self.location = Location.LAIR
            else:
                print("It's not a good idea to go to Gwonam's lair unprotected.")
        
        elif direction == "north":
            print("You head back to Jersey.")
            self.location = Location.TOWN
        
        elif direction == "look":
            print("You are at the center of a vast forest, surrounded by many tall trees. You could definitely "
                  "obtain some wood from some of them, but you would need the proper tools. To your west lies a mine, "
                  "to your south a group of impassable mountains, but you can hear a person in the distance. "
                  "To your east lies the evil Gwonam's lair, and to the north lies Jersey.")
        
        elif direction.startswith("use"):
            # Extract the item name from the command
            parts = direction.split(maxsplit=1)
            if len(parts) < 2:
                print("Use what?")
                return
                
            item_command = parts[1].lower()
            
            if "pickaxe" in item_command and "pickaxe" in self.items:
                if "iron ore" in self.items and ("man" in item_command or "person" in item_command):
                    print("The man looks at the pickaxe with sorrow and tells you that this was his brother's pickaxe. "
                          "He offers you his saw for it and you accept.")
                    self.items.append("saw")
                    self.items.remove("pickaxe")
                else:
                    print("Nothing happens.")
            
            elif "saw" in item_command:
                if "saw" in self.items and "tree" in item_command:
                    print("You use the saw to cut some wood off of a nearby tree.")
                    self.items.append("wood")
                else:
                    print("You can't use that.")
            else:
                print("You can't use that here.")
        
        elif direction == "inventory":
            if self.items:
                print(f"Your inventory: {', '.join(self.items)}")
            else:
                print("Your inventory is empty.")
        
        elif direction.startswith("search"):
            search_target = direction[7:].strip() if len(direction) > 7 else ""
            
            if search_target == "person" or search_target == "man":
                print("You find the man. He appears to be a lumberjack and is carrying a large saw. "
                      "You tell him about your quest and the items you are looking for. "
                      "He directs you to the mine for the iron ore and tells you that he's always wanted "
                      "to be a miner like his brother. He tells you that his brother is in the mines right now "
                      "if you should need any help.")
            else:
                print("You can't search for that.")
        
        elif direction == "commands":
            self.display_commands()
        
        else:
            print("Please enter a valid command.")
    
    def handle_mine(self) -> None:
        """Handle player actions in the mine."""
        direction = input("\nWhat would you like to do?\n").lower().strip()
        
        if direction == "west":
            print("The cavern is too dark to travel down. You head back to the center of the mine.")
        
        elif direction == "east":
            print("You head back to the forest.")
            self.location = Location.FOREST
        
        elif direction == "south":
            print("You are at a deposit of rich iron. This is perfect for the blacksmith. "
                  "The only problem is you don't have a way to mine it.")
        
        elif direction == "north":
            print("You are in a small cavern with a dead body on the floor. You are not sure how he died. "
                  "You see a pickaxe underneath him and a bag around his waist.")
        
        elif direction == "look":
            print("You find yourself in the center of a large mine. To your east lies the exit back to the forest, "
                  "to your north lies a cavern with a dead body, to your south lies an iron deposit, "
                  "and to your west lies a very dark cavern.")
        
        elif direction.startswith("search"):
            search_target = direction[7:].strip() if len(direction) > 7 else ""
            
            if "body" in search_target:
                if "pickaxe" not in self.items:
                    print("You take the pickaxe and the bag which contained 3 Gold Pieces.")
                    self.items.append("pickaxe")
                    self.items.append("3 Gold Pieces")
                else:
                    print("You've already searched the body.")
            else:
                print("You cannot search that.")
        
        elif direction.startswith("use"):
            parts = direction.split(maxsplit=1)
            if len(parts) < 2:
                print("Use what?")
                return
                
            item_command = parts[1].lower()
            
            if "pickaxe" in item_command and "pickaxe" in self.items and "iron" in item_command:
                print("You use the pickaxe to mine the iron ore.")
                self.items.append("iron ore")
            else:
                print("You cannot use that.")
        
        elif direction == "inventory":
            if self.items:
                print(f"Your inventory: {', '.join(self.items)}")
            else:
                print("Your inventory is empty.")
        
        elif direction == "commands":
            self.display_commands()
        
        else:
            print("Please enter a valid command.")
    
    def handle_lair(self) -> None:
        """Handle player actions in Gwonam's lair."""
        direction = input("\nWhat would you like to do?\n").lower().strip()
        
        if direction == "west":
            print("You head back into the forest.")
            self.location = Location.FOREST
        
        elif direction == "south":
            if "Atari" not in self.items:
                print("You see Gwonam's scary looking 'Faces of Evil' paintings hanging on the wall. "
                      "You head down the corridor and come face to face with the evil wizard. "
                      "He screams 'Zreep!' and tries to attack you with a magic spell!")
                
                action = input("What will you do? ").lower().strip()
                
                if "axe" in action or "battleaxe" in action:
                    print("You manage to dodge the spell. You lunge forward and cut off Gwonam's head. "
                          "He screams 'Squadalllllllllahhhhhhhhhhh' as he dies as if it's some sort of spell, "
                          "but who cares, you did it! Atari the magic sword hangs on the wall. "
                          "It's finally yours now. Time to fight Kibbles!")
                    self.items.append("Atari")
                else:
                    print("You get hit with the spell. You can hear Gwonam laughing as you feel immense pain "
                          "and everything begins to fade to black. You realize that this is it, and you do not "
                          "feel bad about losing your own life, only that you could not save Princess Catherine. "
                          "Here is where your Adventure ends.")
                    self.state = GameState.LOSE
                    self.location = Location.DEAD
            else:
                print("You've already defeated Gwonam and claimed Atari.")
        
        elif direction == "east":
            if "key" in self.items:
                print("You run down the long hallway and reach Princess Catherine's cell.")
                cell_locked = True
                
                while cell_locked:
                    action = input("What would you like to do? ").lower().strip()
                    
                    if "key" in action or "unlock" in action:
                        cell_locked = False
                        print("You unlock the cell door and rescue the Princess! She hugs you and thanks you for saving her. "
                              "You escort her back to Jersey and become a legendary hero!")
                        self.state = GameState.WIN
                        self.location = Location.DEAD
                    else:
                        print("The cell is locked. Try using the key.")
            else:
                print("You head down a long hallway and reach a jail cell holding Princess Catherine. "
                      "She screams to you for help, but the door is locked. She tells you the key is in the room "
                      "and guarded by Kibbles the Evil Dragon. You promise her that you will save her "
                      "and head back to the center of the lair.")
        
        elif direction == "north":
            if "Atari" in self.items:
                print("You run down the hallway and reach a giant room. You finally come face to face with "
                      "the Evil Kibbles the Dragon. He towers over you and begins to roar when you enter the room. "
                      "He charges at you and breathes fire in your direction.")
                
                action = input("What will you do? ").lower().strip()
                
                if "atari" in action or "sword" in action:
                    print("You unsheathe Atari. It begins to glow and surrounds you with a protective shield. "
                          "The fire bounces off the shield and you swing it at Kibbles' neck, decapitating him. "
                          "You did it! You pick up the key on the table that Kibbles was guarding. "
                          "Now all that's left is to save the Princess!")
                    self.items.append("key")
                else:
                    print("You get hit by the fire. It scorches your body and you feel excruciating pain all over. "
                          "A deep sense of regret fills you as you realize that you were unable to save Princess Catherine. "
                          "Kibbles picks you up and begins to devour you whole. Your adventure ends here.")
                    self.state = GameState.LOSE
                    self.location = Location.DEAD
            else:
                print("You do not have Atari yet. It would be suicide to try and fight Kibbles.")
        
        elif direction == "look":
            print("You are at the center of the evil Gwonam's lair. To the north lies Kibbles the evil dragon, "
                  "to the south lies Gwonam's room, to the east lies the jail, and to the west is the exit back to the forest.")
        
        elif direction.startswith("use"):
            print("I would worry about using that now. Let's just try and rescue the Princess.")
        
        elif direction == "commands":
            self.display_commands()
        
        elif direction == "inventory":
            if self.items:
                print(f"Your inventory: {', '.join(self.items)}")
            else:
                print("Your inventory is empty.")
        
        elif direction.startswith("search"):
            print("Let's not search that now. We have to save the Princess!")
        
        else:
            print("Please enter a valid command.")


def main():
    """Main function to start the game."""
    game = AdventureGame()
    game.run()


if __name__ == "__main__":
    main()
