import asyncio
import io
import sys
import pygame

# import chrome_dino
# import drawing
import space_invaders
from pyscript import when
from pyscript.web import page


# Redirect stdout to the python-log textarea
class TextAreaWriter(io.TextIOBase):
    def __init__(self, elem, orig):
        self._elem = elem
        self._orig = orig

    def write(self, text):
        if self._orig:
            self._orig.write(text)
        if text:
            self._elem.value += text
            self._elem.scrollTop = self._elem.scrollHeight
        return len(text)

    def flush(self):
        if self._orig:
            self._orig.flush()


if page["#python-log"]:
    sys.stdout = TextAreaWriter(page["#python-log"], sys.stdout)

pygame.init()
pygame.font.init()

# Global reference for the game module
game = space_invaders

# Global pause state
game_paused = False

# Update DOM elements with game metadata
if hasattr(game, "title"):
    title_elem = page["#title"]
    print(game.title)
    if title_elem:
        title_elem.textContent = game.title

if hasattr(game, "info"):
    info_elem = page["#info"]
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
    pause_btn = page["#pauseBtn"]
    if pause_btn:
        pause_btn.textContent = "Resume" if game_paused else "Pause"


# Hide Splash Screen
splash_elem = page["#splash-overlay"]
splash_elem.remove()

# Start the game loop
asyncio.run(main_loop())
