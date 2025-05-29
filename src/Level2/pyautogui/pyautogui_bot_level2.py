import pyautogui
import random
import time
import win32api, win32con
import keyboard

x1, y1 = 719, 210
x2, y2 = 930, 420

target_x, target_y = 831, 173
target_rgb = (158, 158, 0)

movesMade = 0
gamesPlayed = 0
total_time = 0

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

total_time = 0
start_time = time.time()
while True:

    if keyboard.is_pressed('q'):
            print("Stopped by user.")
            stop_flag = True
            break
    
    pixel_rgb = pyautogui.screenshot().getpixel((target_x, target_y))
    if pixel_rgb == target_rgb:
        gamesPlayed += 1
        game_time = time.time() - start_time
        total_time += game_time
        avg_time = total_time / gamesPlayed if gamesPlayed > 0 else 0
        print(f"Game Over! Games played: {gamesPlayed}")
        print(f"Time for last game: {game_time:.2f} seconds")
        print(f"Average time per game: {avg_time:.2f} seconds")
        click(target_x, target_y)
        start_time = time.time()

    rand_x = random.randint(x1, x2)
    rand_y = random.randint(y1, y2)

    click(rand_x, rand_y)
    movesMade += 1

    if movesMade == 5000:
        print("10000 moves made, exiting.")
        break