# game_window.py
import requests
import random
from pgzero.builtins import Actor, animate, keyboard
from pgzero import screen

BASE_URL = 'http://localhost:5000/api/'

WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32
cats = []
coins = []

class Cat:
    def __init__(self, name, x, y):
        self.name = name
        self.sprite = Actor('cat', (x * TILE_SIZE, y * TILE_SIZE))
        self.target_x = x
        self.target_y = y

    def move(self):
        if (self.sprite.x // TILE_SIZE, self.sprite.y // TILE_SIZE) != (self.target_x, self.target_y):
            animate(self.sprite, pos=(self.target_x * TILE_SIZE, self.target_y * TILE_SIZE), duration=0.5)

def get_game_data():
    global cats, coins
    # Fetch the cat positions from the server
    # (For now, we generate mock data for the demo)
    cats = [Cat('Player1', random.randint(0, 19), random.randint(0, 14))]

def draw():
    screen.clear()
    for cat in cats:
        cat.sprite.draw()
        screen.draw.text(cat.name, (cat.sprite.x, cat.sprite.y - 10))

    # Draw the coin at a random position
    for coin in coins:
        screen.blit('coin', (coin['x'] * TILE_SIZE, coin['y'] * TILE_SIZE))

def update():
    for cat in cats:
        cat.move()

    if keyboard.left:
        requests.post(f'{BASE_URL}move', json={'player_name': 'Player1', 'direction': 'left'})
    elif keyboard.right:
        requests.post(f'{BASE_URL}move', json={'player_name': 'Player1', 'direction': 'right'})
    elif keyboard.up:
        requests.post(f'{BASE_URL}move', json={'player_name': 'Player1', 'direction': 'up'})
    elif keyboard.down:
        requests.post(f'{BASE_URL}move', json={'player_name': 'Player1', 'direction': 'down'})

get_game_data()
