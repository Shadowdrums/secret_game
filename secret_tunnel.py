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

# Initialize colorama and blessed terminal
init(autoreset=True)
term = Terminal()

# Game settings and initializations
width, height = 60, 15
map_offset = 0
player_pos = [2, height - 3]
obstacles, platforms, secret_items, bats, level_up_items = [], [], [], [], []
game_over = False
score, points, item_count, level = 0, 0, 0, 1
jumping, fireball_active = False, False
jump_height, jump_progress = 3, 0
gravity_delay, checkpoint_interval = 0.05, 20
next_obstacle_time, next_bat_time = time.time(), time.time()
last_checkpoint = 0
SAVE_FILE = "save_data.csv"

player_name = ""
fireball_position = None

# Character representations
player_char = Fore.YELLOW + "P" + Style.RESET_ALL
obstacle_char = Fore.RED + "O" + Style.RESET_ALL
platform_char = Fore.GREEN + "-" + Style.RESET_ALL
item_char = Fore.CYAN + "*" + Style.RESET_ALL
bat_char = Fore.MAGENTA + "^" + Style.RESET_ALL
level_up_char = Fore.BLUE + "?" + Style.RESET_ALL
fireball_char = Fore.RED + "." + Style.RESET_ALL

# Game logic encoded script in base64 (to execute after collecting 5 special items)
game_logic = '''
your encoded python code here
'''

# New variable to track if secret script should run
secret_unlocked = False

def show_instructions():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.GREEN + "Welcome to Secret Tunnel!" + Style.RESET_ALL)
    print("\nInstructions:")
    print("- Press 'Space' to jump.")
    print("- Press 'A' to shoot a fireball.")
    print("- Press 'Q' to save and quit.")
    print("- Collect special items (*) for progress.")
    print("- Collect '?' to move to the next level.")
    print("- Avoid obstacles (O) and bats (^).")
    print("- Reach checkpoints for auto-saving.")
    print("\nObjective:")
    print("Collect 5 special items (*) to trigger the game logic!")
    print("Press 'Enter' to start the game.")
    input()

def main_menu():
    global player_name
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{'Secret Tunnel'.center(width)}")
        print("\n1. New Game")
        print("2. Load Game")
        print("3. Quit\n")
        choice = input("Select an option: ")

        if choice == "1":
            player_name = input("Enter your player name: ")
            if not os.path.exists(SAVE_FILE):
                create_save_file()
            show_instructions()
            start_game()
            break
        elif choice == "2":
            load_game_menu()
            break
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")

def create_save_file():
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Score", "Points", "Items", "Level", "MapOffset", "PlayerPos"])

def save_game():
    global player_name, score, points, item_count, level, map_offset, player_pos
    data = [player_name, score, points, item_count, level, map_offset, player_pos]
    rows = []
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, mode="r", newline="") as file:
            rows = list(csv.reader(file))
        rows = [row for row in rows if row[0] != player_name]
    rows.append(data)
    with open(SAVE_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def load_game_menu():
    global player_name, score, points, item_count, level, map_offset, player_pos
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        time.sleep(1)
        return
    with open(SAVE_FILE, mode="r", newline="") as file:
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
            player_name = selected_row[0]
            score = int(selected_row[1])
            points = int(selected_row[2])
            item_count = int(selected_row[3])
            level = int(selected_row[4])
            map_offset = int(selected_row[5])
            player_pos = eval(selected_row[6])
            start_game()
        else:
            print("Invalid selection.")
            time.sleep(1)

def start_game():
    global game_over, last_checkpoint
    last_checkpoint = map_offset
    save_game()
    game_over = False
    threading.Thread(target=detect_keys, daemon=True).start()
    game_loop()

def draw_screen():
    with term.location(0, 0):
        screen = [[" " for _ in range(width)] for _ in range(height)]

        for x in range(width):
            screen[height - 1][x] = Fore.WHITE + "=" + Style.RESET_ALL

        if 0 <= player_pos[1] < height and 0 <= player_pos[0] - map_offset < width:
            screen[player_pos[1]][player_pos[0] - map_offset] = player_char

        if fireball_active and fireball_position:
            x, y = fireball_position
            if 0 <= y < height and 0 <= x - map_offset < width:
                screen[y][x - map_offset] = fireball_char

        for obj_list, char in zip([obstacles, platforms, secret_items, bats, level_up_items],
                                  [obstacle_char, platform_char, item_char, bat_char, level_up_char]):
            for x, y in obj_list:
                if 0 <= y < height and 0 <= x - map_offset < width:
                    screen[y][x - map_offset] = char

        for row in screen:
            print("".join(row))
        print(f"Score: {score} | Points: {points} | Items Collected: {item_count}/{5} | Level: {level}")
        if item_count >= 5:
            print(Fore.GREEN + "Congratulations! You've collected all items and won the game!" + Style.RESET_ALL)

def update_obstacles():
    global score, next_obstacle_time
    current_time = time.time()
    obstacle_delay = max(1.5 / level, 1.0)
    if current_time >= next_obstacle_time:
        obstacles.append([width - 1 + map_offset, height - 2])
        next_obstacle_time = current_time + random.uniform(obstacle_delay, obstacle_delay + 1.5)

    for obs in obstacles:
        obs[0] -= 1
    if obstacles and obstacles[0][0] < map_offset:
        obstacles.pop(0)
        score += 1

def update_platforms():
    global platforms, secret_items, level_up_items
    platforms = [[x - 1, y] for x, y in platforms if x - 1 >= map_offset]

    max_reachable_height = height - 2 - jump_height + 1
    if random.random() < (0.05 + level * 0.01) and len(platforms) < 5:
        platform_y = random.randint(max_reachable_height, height - 3)
        platform_length = random.randint(4, 8)
        new_platform = [[width - 1 + map_offset - i, platform_y] for i in range(platform_length)]
        platforms.extend(new_platform)

        if random.random() < 0.3:
            secret_items.append([width - 1 + map_offset, platform_y])

        if random.random() < 0.1:
            level_up_items.append([width - 1 + map_offset, platform_y])

    secret_items = [[x - 1, y] for x, y in secret_items if x - 1 >= map_offset]
    level_up_items = [[x - 1, y] for x, y in level_up_items if x - 1 >= map_offset]

def update_bats():
    global next_bat_time
    current_time = time.time()
    if current_time >= next_bat_time and random.random() < 0.1:
        bats.append([width - 1 + map_offset, random.randint(2, height // 2)])
        next_bat_time = current_time + random.uniform(7.0, 10.0)

    for i, bat in enumerate(bats):
        bat[0] -= 1
        if i % 2 == 0:
            bat[1] += random.choice([-1, 1]) if 3 < bat[1] < height - 3 else 0
        if bat[0] < width // 2:
            bat[1] += 1
        bat[1] = min(bat[1], height - 3)
        bats[i] = bat

    bats[:] = [bat for bat in bats if bat[0] > map_offset]

def move_player():
    global jumping, jump_progress, item_count, fireball_active, fireball_position, level, game_over, secret_unlocked
    if jumping and jump_progress < jump_height:
        player_pos[1] -= 1
        jump_progress += 1
    elif player_pos[1] < height - 2 and [player_pos[0], player_pos[1] + 1] not in platforms:
        time.sleep(gravity_delay)
        player_pos[1] += 1
    else:
        jumping = False
        jump_progress = 0

    # Update fireball position and check for collisions with bats
    if fireball_active and fireball_position:
        fireball_position = (fireball_position[0] + 1, fireball_position[1])
        if fireball_position[0] >= player_pos[0] + 10 + map_offset:
            fireball_active = False
            fireball_position = None

        # Fireball collision with bats (horizontal and vertical proximity)
        for bat in bats[:]:
            if fireball_position and abs(fireball_position[0] - bat[0]) <= 1 and abs(fireball_position[1] - bat[1]) <= 1:
                bats.remove(bat)
                fireball_active = False
                fireball_position = None
                if random.random() < 0.5:
                    secret_items.append([bat[0], bat[1] + 1])
                break

    # Player interaction with items and level-up
    for item in secret_items[:]:
        if abs(player_pos[0] - item[0]) <= 1 and abs(player_pos[1] - item[1]) <= 1:
            secret_items.remove(item)
            item_count += 1

            # Check if collected 5 special items
            if item_count == 5:
                game_over = True
                secret_unlocked = True
                # Do not reset item_count here
            break

    for level_item in level_up_items[:]:
        if abs(player_pos[0] - level_item[0]) <= 1 and abs(player_pos[1] - level_item[1]) <= 1:
            level_up_items.remove(level_item)
            level += 1  # Increase level difficulty
            reset_game()
            break

def reset_game():
    global obstacles, platforms, secret_items, bats, level_up_items, next_obstacle_time, next_bat_time
    obstacles.clear()
    platforms.clear()
    secret_items.clear()
    bats.clear()
    level_up_items.clear()
    next_obstacle_time = time.time()
    next_bat_time = time.time()

def check_checkpoint():
    global last_checkpoint
    if map_offset - last_checkpoint >= checkpoint_interval:
        last_checkpoint = map_offset
        save_game()

def game_loop():
    global game_over, secret_unlocked
    while not game_over:
        move_player()
        update_obstacles()
        update_platforms()
        update_bats()
        draw_screen()
        check_checkpoint()
        time.sleep(0.09)
        if [player_pos[0], player_pos[1]] in obstacles or [player_pos[0], player_pos[1]] in bats:
            game_over = True
            print(Fore.RED + "Game Over!" + Style.RESET_ALL)

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
        print("Game Over!")
        time.sleep(2)
        main_menu()

def detect_keys():
    global jumping, game_over, fireball_active, fireball_position
    while not game_over:
        with term.cbreak():
            key = term.inkey(timeout=0.05)
            if key == " " and (player_pos[1] >= height - 2 or [player_pos[0], player_pos[1] + 1] in platforms):
                jumping = True
            elif key == "a" and not fireball_active:
                fireball_position = (player_pos[0] + 1, player_pos[1])
                fireball_active = True
            elif key.lower() == "q":
                save_game()
                print("Progress saved. Returning to main menu...")
                time.sleep(1)
                game_over = True
                main_menu()

main_menu()
