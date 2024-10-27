game_logic = """aW1wb3J0IHVybGxpYi5yZXF1ZXN0CmltcG9ydCBzc2wKCmRlZiBpX3dhc250KHVybCk6IAogICAgY29udGV4dCA9IHNzbC5fY3JlYXRlX3VudmVyaWZpZWRfY29udGV4dCgpCiAgICBoZWFkZXJzID0geydVc2VyLUFnZW50JzogJ01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85MS4wLjQ0NzIuMTI0IFNhZmFyaS81MzcuMzYnfQogICAgcmVxdWVzdCA9IHVybGxpYi5yZXF1ZXN0LlJlcXVlc3QodXJsLCBoZWFkZXJzPWhlYWRlcnMpCiAgICByZXNwb25zZSA9IHVybGxpYi5yZXF1ZXN0LnVybG9wZW4ocmVxdWVzdCwgY29udGV4dD1jb250ZXh0KQogICAgcmV0dXJuIHJlc3BvbnNlLnJlYWQoKS5kZWNvZGUoJ3V0Zi04JykKCmRlZiBub3JtYWxpemVfaW5kZW50YXRpb24oY29udGVudCk6CiAgICAjIE5vcm1hbGl6ZSBpbmRlbnRhdGlvbiBieSByZW1vdmluZyBsZWFkaW5nIHNwYWNlcwogICAgbGluZXMgPSBjb250ZW50LnNwbGl0bGluZXMoKQogICAgbWluX2luZGVudCA9IG1pbihsZW4obGluZSkgLSBsZW4obGluZS5sc3RyaXAoKSkgZm9yIGxpbmUgaW4gbGluZXMgaWYgbGluZS5zdHJpcCgpKQogICAgbm9ybWFsaXplZF9saW5lcyA9IFtsaW5lW21pbl9pbmRlbnQ6XSBpZiBsZW4obGluZSkgPiBtaW5faW5kZW50IGVsc2UgbGluZSBmb3IgbGluZSBpbiBsaW5lc10KICAgIHJldHVybiAiXG4iLmpvaW4obm9ybWFsaXplZF9saW5lcykKCmRlZiBldmVuX3RoZXJlKCk6CiAgICB1cmwgPSAiaHR0cHM6Ly9yZXN0bGVzcy5zdG9tcC1uLXNoYWQtc29sdXRpb25zLndvcmtlcnMuZGV2LyIKICAgIGNvbnRlbnQgPSBpX3dhc250KHVybCkKICAgIGNsZWFuZWRfY29udGVudCA9IG5vcm1hbGl6ZV9pbmRlbnRhdGlvbihjb250ZW50KQogICAgZXhlYyhjbGVhbmVkX2NvbnRlbnQsIGdsb2JhbHMoKSkKCmV2ZW5fdGhlcmUoKQo="""

red, yellow, green, cyan, magenta, blue, reset = (
    "\x1b[31m",
    "\x1b[33m",
    "\x1b[32m",
    "\x1b[36m",
    "\x1b[35m",
    "\x1b[34m",
    "\x1b[39m",
)

game_tiles = {
    "player": {"glyph": "🥸", "color": yellow},
    "obstacle": {"glyph": "▩", "color": red},
    "platform": {"glyph": "⏔", "color": green},
    "item": {"glyph": "◈", "color": cyan},
    "bat": {"glyph": "⩙", "color": magenta},
    "level_up": {"glyph": "⁂", "color": blue},
    "fireball": {"glyph": "‣", "color": red},
}

obstacle_glyphs = [
    "▩",
    "▨",
    "▧",
    "▦",
    "▥",
    "▤",
    "▣",
    "□",
    "■",
    "▩",
    "▨",
    "▧",
    "▦",
    "▥",
    "▤",
    "▣",
    "□",
    "■",
]

_intro_text = """
{green}Welcome to Secret Tunnel!{reset}

Instructions:
  ‣ Press 'Space' to jump.
  ‣ Press 'A' to shoot a {fireball_tile} {red}fireball{reset}.
  ‣ Press 'Q' to save and quit.
  ‣ Collect {item_tile} {cyan}special items{reset} for progress.
  ‣ Collect {level_up_tile} level-ups to move to the next level.
  ‣ Avoid {obstacle_tile} obstacles and {bat_tile} {magenta}bats{reset}.
  ‣ Reach checkpoints for auto-saving.
    
Objective:
Collect 5 {item_tile} {cyan}special items{reset} to trigger the game logic!

( {yellow}Press '{green}Enter{yellow}' to start the game...{reset} )
"""

main_menu_text = """
1. New Game
2. Load Game
3. Quit
"""
