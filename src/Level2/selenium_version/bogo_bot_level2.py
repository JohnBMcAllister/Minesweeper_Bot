import random
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import keyboard

load_dotenv()

options = Options()
options.binary_location = os.getenv("FIREFOX_BINARY")
options.headless = True
service = Service(executable_path=os.getenv("GECKODRIVER_PATH"))
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://minesweeper.online/game/4655406265")

# Environment variables
width = 9
height = 9
games_played = 0

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'cell'))
)

def print_board(board):
    print("Current Board:")
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()

def update_board(board, tiles):
    for tile in tiles:
        x = int(tile.get_attribute('data-x'))
        y = int(tile.get_attribute('data-y'))
        cls = tile.get_attribute('class')
        if 'hdd_closed' in cls:
            if 'hdd_flag' in cls:
                board[y][x] = '-1'
            else:
                board[y][x] = '-'
        elif 'hdd_opened' in cls:
            for n in range(0, 8):
                if f'hdd_type{n}' in cls:
                    board[y][x] = str(n)
                    break
                else:
                    board[y][x] = '?'

def get_random_tile(tiles):
    unopened = [tile for tile in tiles if 'hdd_closed' in tile.get_attribute('class') and 'hdd_flag' not in tile.get_attribute('class')]
    if unopened:
        return random.choice(unopened)
    return None

def get_neighbors(y, x):
    neighbors = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                neighbors.append((ny, nx))
    return neighbors

def apply_rules(board):
    actions = set()
    for y in range(height):
        for x in range(width):
            if board[y][x].isdigit() and board[y][x] != '0':
                value = int(board[y][x])
                neighbors = get_neighbors(y, x)
                unopened = [(ny, nx) for ny, nx in neighbors if board[ny][nx] == '-']
                flagged = [(ny, nx) for ny, nx in neighbors if board[ny][nx] == '-1']
                # Rule 1
                if len(unopened) > 0 and value == len(unopened) + len(flagged) and len(flagged) < value:
                    for ny, nx in unopened:
                        actions.add(('flag', ny, nx))
                # Rule 2
                if len(unopened) > 0 and value == len(flagged) and len(flagged) > 0:
                    for ny, nx in unopened:
                        actions.add(('click', ny, nx))
    return list(actions)

def get_game_state():
    face = driver.find_element(By.CLASS_NAME, 'top-area-face')
    cls = face.get_attribute('class')
    if 'hdd_top-area-face-win' in cls:
        return 'win'
    elif 'hdd_top-area-face-lose' in cls:
        return 'lose'
    return 'playing'

while True:
    games_played += 1
    start_time = time.time()
    print(f"Starting game {games_played}")

    face = driver.find_element(By.CLASS_NAME, 'top-area-face')
    face.click()  # Start a new game
    time.sleep(1)  # Wait for the game to initialize
    board = [["-" for _ in range(width)] for _ in range(height)]
    tiles = driver.find_elements(By.CLASS_NAME, 'cell')
    first_tile = get_random_tile(tiles)
    if first_tile:
        first_tile.click()
        tiles = driver.find_elements(By.CLASS_NAME, 'cell')
        update_board(board, tiles)
        print_board(board)

    while True:
        tiles = driver.find_elements(By.CLASS_NAME, 'cell')
        update_board(board, tiles)
        print_board(board)
        actions = apply_rules(board)
        if actions:
            for action, y, x in actions:
                if action == 'flag':
                    cell = driver.find_element(By.XPATH, f"//div[@data-y='{y}'][@data-x='{x}']")
                    ActionChains(driver).context_click(cell).perform()
                    tiles = driver.find_elements(By.CLASS_NAME, 'cell')
                    update_board(board, tiles)
                    print_board(board)
                elif action == 'click':
                    cell = driver.find_element(By.XPATH, f"//div[@data-y='{y}'][@data-x='{x}']")
                    cell.click()
                    tiles = driver.find_elements(By.CLASS_NAME, 'cell')
                    update_board(board, tiles)
                    print_board(board)
        else:
            tile = get_random_tile(tiles)
            if tile:
                tile.click()
                tiles = driver.find_elements(By.CLASS_NAME, 'cell')
                update_board(board, tiles)
                print_board(board)

        state = get_game_state()
        if state != 'playing':
            print(f"Game ended: {state}")
            elapsed = time.time() - start_time
            break

    if state == 'win':
        print("Congratulations! it took", elapsed, "seconds and you played", games_played, "games.")
        break

input("Press Enter to close")
