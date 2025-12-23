import asyncio
import sys
import pygame

import breakout
import drawing
from pyscript import when
from pyscript.web import page

pygame.init()
pygame.font.init()

# Global reference for the game module
game = breakout

# Global pause state
game_paused = False

# Update DOM elements with game metadata
if hasattr(game, "title"):
    title_elem = page.find("#title")
    print(game.title, title_elem)
    if title_elem:
        title_elem.textContent = game.title

if hasattr(game, "info"):
    info_elem = page.find("#info")
    if info_elem:
        info_elem.innerHTML = game.info


async def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if getattr(game, "update", False) and callable(game.update):
            game.update()
        game.draw()

        pygame.display.flip()

        await asyncio.sleep(1 / 60)


# Button event handlers using pyscript.when
@when("click", "#resetBtn")
def reset_game(event):
    if hasattr(game, "reset_game") and callable(game.reset_game):
        game.reset_game()


@when("click", "#pauseBtn")
def toggle_pause(event):
    global game_paused
    game_paused = not game_paused
    if hasattr(game, "set_pause") and callable(game.set_pause):
        game.set_pause(game_paused)

    # Update button text
    pause_btn = page.find("#pauseBtn")
    if pause_btn:
        pause_btn.textContent = "Resume" if game_paused else "Pause"


# Start the game loop
asyncio.run(main_loop())
