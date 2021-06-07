# Sodoku Gameboard

This is the sodoku graphical game using `pygame` library with `backtracking algorithm`.
The module also included a graphical solver to mimic the algorithm flows.

## Installation
Create virtual environment
```bash
# Install virtualenv if we do not have it yet
pip install virtualenv
# Create new virtual env
python -m venv venv
```
Activate your `venv`
```bash
# For Windows
source venv/Scripts/activate 
# For Linux
source venv/bin/activate
```
Install dependency package
```bash
pip install -r requirements.txt
```
## Usage
```bash
python main.py
```
Feel free to change the `INIT_STAGE` if you want to try other puzzple.
```python
class Board:
    # The backtracking approach is to generate all possible numbers (1-9)
    # into the empty cells.
    # Try every row, column one by one until the correct solution is found.
    INIT_STAGE = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]
```
In case you want to change the `style`, `size` or `fps`, feel free to update the Engine Configuration.
```python
class GameEngine:
    BOARD_NAME = "Sodoku Gameboard"
    BOARD_SIZE = 630
    BOARD_COLORS = {
        "BLACK": (0, 0, 0),
        "WHITE": (255, 255, 255),
        "DARK_GREY": (128, 128, 128),
        "LIGHT_GREY": (224, 224, 224),
        "RED": (255, 51, 51),
        "ORANGE": (255, 178, 153),
        "GREEN": (0, 204, 102),
        "BLUE": (0, 128, 255),
    }
    FPS = 60
```
## Outstanding Works
Currently, there are some more things I want to put into, you can find it in the `main.py` script. Feel free to work with it once you have understood the module.
```python
if __name__ == '__main__':
    # TODO: Improve logging mechanism
    # TODO: Add pytest package
    # TODO: Improve Game Interface to show more information
    # Ultility: Button Guideline, Time Counter, Stage Generator, Hint
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)