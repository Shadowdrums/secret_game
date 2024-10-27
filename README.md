# secret_game
a simple game that if you win can run imbedded encoded python script
# Secret Tunnel

Secret Tunnel is a command-line arcade game that challenges you to collect items, avoid obstacles, and progress through levels while using a unique save-and-load system. Collect 5 special items to trigger a secret script encoded within the game!

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Gameplay Instructions](#gameplay-instructions)
- [Controls](#controls)
- [Saving and Loading](#saving-and-loading)
- [Notes](#notes)
  
## Features
- **Player Progression**: Navigate through levels with increasing difficulty as you advance.
- **Dynamic Obstacles**: Encounter randomly generated obstacles and flying bats to dodge.
- **Special Items**: Collect secret items (`*`) to unlock hidden functionality.
- **Save and Load**: Save your progress to pick up where you left off.
- **Encoded Secret Script**: Unlock and execute a hidden script by collecting items.

## Installation
1. **Prerequisites**: Ensure Python 3.x is installed.
2. **Install Required Libraries**:
   ```bash
   pip install blessed colorama
   ```
## Run the Game:
Copy code
```bash
python secret_tunnel.py
```
## Gameplay Instructions
- Start a new game, or load a previous save to continue.
## Objective:
- Collect special items (*) to progress through levels and unlock the hidden script.
- Reach checkpoints to auto-save.
- Avoid obstacles (O) and bats (^).
## Controls
- Space - Jump
- A - Shoot fireball
- Q - Save and quit
- Enter - Start the game
## Saving and Loading
The game automatically saves at each checkpoint.
Save your progress at any time by pressing Q.
Saved data is stored in save_data.csv and can be loaded from the main menu.
## Notes
The hidden script (game_logic) will execute in the background once the player collects 5 special items.
Customize the encoded script section to add your unique functionality.
