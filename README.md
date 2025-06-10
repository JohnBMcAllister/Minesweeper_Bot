# 🧠 Minesweeper Bot

This project is a bot that plays the classic Minesweeper game using two different automation methods: **PyAutoGUI** and **Selenium**.

Inspired by [Code Bullet's Minesweeper AI video](https://youtu.be/ehAStJmx_Fo?si=HjeTiyKblvdYijsl), this project explores two levels of bot intelligence, from pure chance to basic logic-based inference.

Minesweeper Website: https://minesweeper.online/game/4702341783

---

## 🤖 Bot Levels

### 🔹 Level 1: Random Bot
- Randomly clicks on unopened tiles.
- If it hits a mine, it restarts the game.
- If it wins, the game ends.
- No logic or inference — purely luck-based.

### 🔹 Level 2: Rule-Based Bot
- Implements two basic Minesweeper inference rules:
  1. **Flagging Bombs**: If the number of unopened tiles around a number equals the number, all those tiles are bombs.
  2. **Clearing Safe Tiles**: If the number of flags around a number equals the number, the rest of the unopened tiles around it are safe and can be clicked.
- If neither rule can be applied, it chooses a random tile to continue.

---
