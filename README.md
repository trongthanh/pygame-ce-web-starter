# Pygame-CE Demo on PyScript

This is a collection of games built with Pygame-CE and running in the browser using PyScript and Pyodide.

## Files

- `index.html` - Main HTML file with PyScript setup and game canvas
- `main.py` - Bootstrap module that sets up Pygame and runs the game loop
- `chrome_dino.py` - Chrome Dino endless runner game
- `breakout.py` - Breakout game implementation with paddle, ball, and blocks
- `drawing.py` - Simple demo showing basic Pygame drawing
- `pyscript.toml` - PyScript configuration file

## How to Run Locally

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

## GitHub Codespaces

You can edit and run this project directly in GitHub Codespaces:

1. Click the **Code** button on the GitHub repository
2. Select **Codespaces** tab
3. Click **Create codespace on main**
4. Once the codespace is ready, click the **Ports** tab
5. Add port `8000` and click **Open in Browser**

The codespace is pre-configured with Python 3 and VS Code extensions for Python development.


## Game Controls

### Chrome Dino (Default Game)
- **Space / Up Arrow**: Jump
- **Down Arrow**: Duck
- **Reset Button**: Restart the game
- **Pause/Resume Button**: Pause or resume the game

### Breakout
- **Left/Right Arrow Keys**: Move the paddle
- **Reset Button**: Restart the game
- **Pause/Resume Button**: Pause or resume the game

## Switching Games

To switch between games, edit `main.py` and change the import on line 5:

```python
import breakout  # Change to chrome_dino or drawing
game = breakout   # Match the import
```

## Game Rules

Each game has its own rules:
- **Chrome Dino**: Jump over obstacles and avoid cacti. Try to get the highest score!
- **Breakout**: Use the paddle to keep the ball in play, break all blocks, and don't let the ball fall off
- **Drawing**: A simple demo showing basic Pygame drawing functions

## Technical Notes

- This uses Pygame-CE which is included by default in PyScript
- The game loop uses `asyncio.sleep()` to allow the browser to remain responsive
- All graphics are drawn programmatically (no external image assets needed)
- The game runs at 60 FPS for smooth animation

## About PyScript

PyScript allows you to run Python directly in the browser using WebAssembly (Pyodide). This demo showcases how you can create interactive games with Pygame-CE that run entirely in the browser without any server-side Python installation.
