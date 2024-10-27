from dataclasses import dataclass
import toml

@dataclass
class GameSettings:
    width: int
    height: int
    map_offset: int
    player_pos: list
    obstacles: list
    platforms: list
    secret_items: list
    bats: list
    level_up_items: list
    game_over: bool
    score: int
    points: int
    item_count: int
    level: int
    jumping: bool
    fireball_active: bool
    jump_height: int
    jump_progress: int
    gravity_delay: float
    checkpoint_interval: int
    next_obstacle_time: float
    next_bat_time: float
    last_checkpoint: int
    save_file: str
    player_name: str
    fireball_position: list

    @staticmethod
    def from_toml(toml_filename):
        settings = toml.load(toml_filename)
        return GameSettings(
            width=settings["width"],
            height=settings["height"],
            map_offset=settings["map_offset"],
            player_pos=settings["player_pos"],
            obstacles=settings["obstacles"],
            platforms=settings["platforms"],
            secret_items=settings["secret_items"],
            bats=settings["bats"],
            level_up_items=settings["level_up_items"],
            game_over=settings["game_over"],
            score=settings["score"],
            points=settings["points"],
            item_count=settings["item_count"],
            level=settings["level"],
            jumping=settings["jumping"],
            fireball_active=settings["fireball_active"],
            jump_height=settings["jump_height"],
            jump_progress=settings["jump_progress"],
            gravity_delay=settings["gravity_delay"],
            checkpoint_interval=settings["checkpoint_interval"],
            next_obstacle_time=settings["next_obstacle_time"],
            next_bat_time=settings["next_bat_time"],
            last_checkpoint=settings["last_checkpoint"],
            save_file=settings["save_file"],
            player_name=settings["player_name"],
            fireball_position=settings["fireball_position"]
        )

