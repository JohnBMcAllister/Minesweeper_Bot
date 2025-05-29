import pyautogui
import time

while True:
    x, y = pyautogui.position()
    rgb = pyautogui.screenshot().getpixel((x, y))
    print(f"Current mouse position: ({x}, {y}), RGB: {rgb}")
    time.sleep(1)  # Adjust the sleep time as needed