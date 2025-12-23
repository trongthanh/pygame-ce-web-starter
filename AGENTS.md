# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# Serve the directory (required for PyScript)
python -m http.server 8000

# Then open in browser at http://localhost:8000
```

PyScript requires a local web server to work - it cannot run from `file://` URLs.

## Architecture

This is a Pygame-CE game running in the browser via PyScript and Pyodide.

### Core Components

- **index.html**: HTML entry point that loads PyScript core library and renders the canvas element. Uses `<script type="py-game">` to load Python game code.
- **main.py**: Bootstrap module that sets up Pygame, runs the async game loop, and connects HTML buttons to game functions via `pyscript.when` decorators.
- **breakout.py**: Complete Breakout game implementation with paddle, ball, blocks, and collision detection.

### PyScript Integration Pattern

The game uses PyScript's `py-game` script type which automatically creates a Pygame display bound to the canvas element in the HTML.

Key integration points:
- `from pyscript import when` - decorator for HTML event handlers
- `from pyscript.web import page` - for accessing DOM elements
- `asyncio.run(main_loop())` - async game loop using `await asyncio.sleep(1/60)` for 60 FPS

### Game Module Interface

Game modules (like `breakout.py`) should export these functions:
- `update()` - called each frame for game logic
- `draw()` - called each frame to render the game
- `reset_game()` - resets game state
- `set_pause(paused)` - pauses/resumes the game

The `screen` surface is created via `pygame.display.set_mode()` and PyScript binds it to the HTML canvas.

### Switching Game Modules

In `main.py`, change line 12 to import a different game:
```python
game = breakout  # Change to other module
```

And add the import at the top.

### Type Checking

The project uses Pyright with custom stubs in `typings/` for PyScript types. Run with:
```bash
pyright .
```

PyScript types are not complete - some functions may be marked as `Any`.
