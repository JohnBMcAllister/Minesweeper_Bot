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

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'cell'))
)

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

def get_game_state():
    face = driver.find_element(By.CLASS_NAME, 'top-area-face')
    cls = face.get_attribute('class')
    if 'hdd_top-area-face-win' in cls:
        return 'win'
    elif 'hdd_top-area-face-lose' in cls:
        return 'lose'
    return 'playing'

board = [["-" for _ in range(width)] for _ in range(height)]
while True:
    if keyboard.is_pressed('q'):
        tiles = driver.find_elements(By.CLASS_NAME, 'cell')
        update_board(board, tiles)

        print("-------- Board --------")
        for row in board:
            print(row)

        time.sleep(3)
    
    if keyboard.is_pressed('w'):
        break;

driver.quit()
        