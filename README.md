# Pygame-CE Demo on PyScript

This is a Breakout-style game built with Pygame-CE and running in the browser using PyScript and Pyodide.

## Files

- `index.html` - Main HTML file with PyScript setup and game canvas
- `main.py` - Bootstrap module that sets up Pygame and runs the game loop
- `breakout.py` - Breakout game implementation with paddle, ball, and blocks
- `demo.py` - Simple demo showing basic Pygame drawing
- `pyscript.toml` - PyScript configuration file

## How to Run

1. Serve this directory using a local web server (required for PyScript to work):
   ```bash
   # Using Python 3
   python -m http.server 8000

   # Or using Node.js if you have http-server installed
   npx http-server
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Game Controls

- **Left/Right Arrow Keys**: Move the paddle
- **Reset Button**: Restart the game
- **Pause/Resume Button**: Pause or resume the game

## Game Rules

- Use the paddle to keep the ball in play
- Break all the colored blocks to win
- Don't let the ball fall off the bottom of the screen
- The ball's direction changes based on where it hits the paddle

## Technical Notes

- This uses Pygame-CE which is included by default in PyScript
- The game loop uses `asyncio.sleep()` to allow the browser to remain responsive
- All graphics are drawn programmatically (no external image assets needed)
- The game runs at 60 FPS for smooth animation

## About PyScript

PyScript allows you to run Python directly in the browser using WebAssembly (Pyodide). This demo showcases how you can create interactive games with Pygame-CE that run entirely in the browser without any server-side Python installation.