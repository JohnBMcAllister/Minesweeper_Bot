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

load_dotenv()

options = Options()
options.binary_location = os.getenv("FIREFOX_BINARY")
options.headless = True
service = Service(executable_path=os.getenv("GECKODRIVER_PATH"))
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://minesweeper.online/game/4655406265")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'cell'))
)

def get_unopened_tiles():
    tiles = driv 
    return [tile for tile in tiles if 'hdd_closed' in tile.get_attribute('class') and 'hdd_flag' not in tile.get_attribute('class')]

def get_game_state():
    face = driver.find_element(By.CLASS_NAME, 'top-area-face')
    cls = face.get_attribute('class')
    if 'hdd_top-area-face-win' in cls:
        return 'win'
    elif 'hdd_top-area-face-lose' in cls:
        return 'lose'
    return 'playing'

games_played = 0

while True:
    games_played += 1
    # Reset the board at the start of each game
    face = driver.find_element(By.CLASS_NAME, 'top-area-face')
    face.click()

    start_time = time.time()

    unopened = get_unopened_tiles()  # Get all unopened tiles once

    while True:
        state = get_game_state()
        if state != 'playing':
            elapsed = time.time() - start_time
            print(f"Game {games_played} ended: {state} in {elapsed:.2f} seconds")
            break

        if not unopened:
            elapsed = time.time() - start_time
            print(f"Game {games_played} ended: no unopened tiles in {elapsed:.2f} seconds")
            break

        tile = random.choice(unopened)
        unopened.remove(tile)  # Remove the tile so we don't click it again
        tile.click()

    # If win, stop. If lose, loop and try again.
    if state == 'win':
        print("Bot won the game!")
        break



