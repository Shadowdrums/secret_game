import time
from .GameSettings import GameSettings
from .GameTile import GameTile
from .static import (
    game_logic,
    game_tiles,
    red,
    yellow,
    green,
    cyan,
    magenta,
    blue,
    reset,
    _intro_text,
    main_menu_text,
    obstacle_glyphs,
)


def load_default_settings():
    return GameSettings.from_toml("settings.toml")


def game_setup():
    game = load_default_settings()

    # Game settings and initializations
    game.width, game.height = 60, 15
    game.map_offset = 0
    game.player_pos = [2, game.height - 3]
    (
        game.obstacles,
        game.platforms,
        game.secret_items,
        game.bats,
        game.level_up_items,
    ) = ([], [], [], [], [])
    game.game_over = False
    game.score, game.points, game.item_count, game.level = 0, 0, 0, 1
    game.jumping, game.fireball_active = False, False
    game.jump_height, game.jump_progress = 3, 0
    game.gravity_delay, game.checkpoint_interval = 0.05, 20
    game.next_obstacle_time, game.next_bat_time = time.time(), time.time()
    game.last_checkpoint = 0
    game.save_file = "save_data.csv"

    game.player_name = ""
    game.fireball_position = None

    return game


(
    player_tile,
    obstacle_tile,
    platform_tile,
    item_tile,
    bat_tile,
    level_up_tile,
    fireball_tile,
) = [GameTile(*ea.values()) for ea in game_tiles.values()]

intro_text = _intro_text.format(
    green=green,
    reset=reset,
    red=red,
    fireball_tile=fireball_tile,
    cyan=cyan,
    item_tile=item_tile,
    level_up_tile=level_up_tile,
    obstacle_tile=obstacle_tile,
    magenta=magenta,
    bat_tile=bat_tile,
    yellow=yellow,
)

game = game_setup()
