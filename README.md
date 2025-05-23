# 🚀 Block Blast
[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.0%2B-green)](https://www.pygame.org/)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

> **Block Blast** is an addictive match-and-clear puzzle game built with Pygame.  
> Clear groups of two or more same-color blocks, rack up points, and race against the clock while strategic power-ups and locked blocks keep you on your toes!

## 🎮 Features
- 🔥 **Match & Clear**  
  Click groups of ≥2 adjacent blocks of the same color to clear them.
- 💣 **Exciting Power-Ups**  
  – **Bomb**: Blasts a 3×3 area  
  – **Swap**: Trade any two blocks  
  – **Extra Moves**: +5 moves instantly
- 🔒 **Locked Blocks**  
  Must be unlocked by adjacent clears or power-ups.
- 🌈 **Dynamic Levels**  
  Earn bonus time, unlock new colors, and add rows every level.
- 🌟 **Particle & Gravity Animations**  
  Smooth falling blocks and explosion effects.
- 🏆 **High Score Tracking**  
  Saves your best score to `highscore.txt`.
- 🔊 **Sound FX**  
  (optional) `clear.wav`, `powerup.wav`, `gameover.wav`.

## 🚀 Installation
1. **Clone repository**  
```
   git clone https://github.com/yourusername/block-blast.git
```
```
   cd block-blast
```


2. **Setup virtual environment (recommended)**
 ```  python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```
   pip install pygame
   ```

4. **(Optional) Add sound effects**
   ```Place `clear.wav`, `powerup.wav`, `gameover.wav` in the project root.```

## ▶️ Usage
```
python blockblast.py
```
* **Click** on blocks to match & clear (or swap when using the swap power-up).
* **Press R** after “Game Over” to restart.


## 🎛️ Controls & HUD
| Control         | Action                                 |
| --------------- | -------------------------------------- |
| 🖱️ Mouse Click | Select & clear groups (or swap blocks) |
| R key           | Restart when game is over              |
| HUD             | Score, Level, Moves, Time, High Score  |


## 📝 File Structure
block-blast/
├── blockblast.py      # Main game script
├── highscore.txt      # Auto-generated high score storage
├── clear.wav          # (optional) clear sound
├── powerup.wav        # (optional) power-up sound
├── gameover.wav       # (optional) game-over sound
├── screenshot.png     # Demo screenshot
└── venv/              # Virtual environment (ignored by Git)

## 🤝 Contributing
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add cool feature"`)
4. Push to your branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the **MIT License**.
See [LICENSE](./LICENSE) for details.


> Built with ❤️ using **Pygame**
> Happy blasting! 🚀
