# 🐎 Chess 🐴
## 📒Game Description

Welcome to the **Chess Game!**  
Simply **grab** the piece you want to move and **drag & drop** it to the desired spot.
  
  
## 😃Demo Play
**With Computer**  
 
https://github.com/su1jun/Chess/assets/120762843/064d54aa-478c-4b73-953b-d67f99312bf1

**People Only**  

https://github.com/su1jun/Chess/assets/120762843/511999dd-a4e3-4fb2-b866-7cf802fdbe7e
    
    
## 🧐Multiple Implementations

https://github.com/su1jun/Chess/assets/120762843/a2eb2612-4dfb-4248-8287-61a421c29679

https://github.com/su1jun/Chess/assets/120762843/76b6ac47-79aa-4cc1-b6b9-096950387673

https://github.com/su1jun/Chess/assets/120762843/dc3ca9ca-2344-4721-84be-c90a67c05390

https://github.com/su1jun/Chess/assets/120762843/f2dfde55-d0f1-4c01-a615-56c54c93deba

https://github.com/su1jun/Chess/assets/120762843/d8c3a64e-9b5d-49cc-a9f5-73104c319244
  
  
## 📃Manual

#### Entry Point:
Start the game via `src/main.py`, or use `chess.exe`.    
+ chess.exe is too large to be deleted temporarily
+ If necessary, you can use the source as an exe file with the pyinstaller library.
  

![Chess Entry Point](https://github.com/su1jun/Chess/assets/120762843/81e95128-f8fb-430f-b2f8-71eb9b780f39)  
Choose between playing **1-player (VS computer)** or **2-player (VS a friend)**.
  

![1-player mode](https://github.com/su1jun/Chess/assets/120762843/27f8daca-51b1-4d2e-a5d1-823cc7507670)  
In 1-player mode, select the **computer's level and color**.
  

![2-player mode](https://github.com/su1jun/Chess/assets/120762843/5e893bf4-60df-41d5-81cd-a2e588a13f11)  
In 2-player mode or after finishing the computer's setup, enjoy the **chess game!**
  
#### Keyboard Shortcuts:  

https://github.com/su1jun/Chess/assets/120762843/9620e5b0-b3b6-4466-afdf-166d4a71c696

**↩️ 'q'**: **Undo** the last move  
**🌀 'w'**: **Flip** the screen  
**🔃 'r'**: **Restart** the game  

**✍️ 'a'**: Change **theme**  
**🔊 's'**: Change **sound**

**⏮️ 'backspace'**: Return to **the main title**  
  
  
## 📚License

The project includes the chess AI **Stockfish**, which is Open Source.  
This project is **licensed** under the **GNU General Public License version 3**.  
See the stockfish/Copying.txt or README.md for more details.  
  
  
## 📢QnA
### 1. What is the stockfish?
![stockfish](https://github.com/su1jun/Chess/assets/120762843/395fe0ed-f985-4eda-a321-3c9277eb7ee3)  
**Stockfish** is an **open-source chess engine**.  
As the Stockfish team focuses solely on developing the chess engine,  
integrating it with a suitable GUI program and protocol is essential for gameplay or analysis.   
  
**- Alpha-Beta Pruning Algorithm**:  
Stockfish employs an alpha-beta pruning algorithm to efficiently reduce the number of nodes evaluated  
in the minimax decision tree, optimizing search for the best move.  

**- Evaluation Function**:  
The engine uses a sophisticated evaluation function considering factors like piece value,  
pawn structure, mobility, king safety, and control of the board center, each weighted by its strategic importance.  

**- Deep and Fast Search**:  
Stockfish is renowned for its ability to deeply analyze a vast array of potential moves rapidly,  
making it ideal for both extended and rapid-play chess games.   
    
    
### 2. Do I need a Python program or package?
No, if the exe file works fine, that's all you need.  
However, in cases like a Mac environment or unknown errors, Python and the pygame library are required.  
The program was developed in `Python v3.11`, `Pygame v2.5.2`.  
If your environment is set up,  
you can run the Chess program by executing the command `python src/main.py` in the Chess folder directory  

### 3. I can't execute the exe file...
Firstly, it should be a Windows environment.  

The file `Chess.exe` and the package `build/main/main.pkg` are large files over 100MB,  
so you need Git Large File Storage (LFS) to download them.  
You will need to download LFS and use the clone command for a proper download.  
For more details, visit:  
- [Git LFS - Official Site / Download](https://git-lfs.com/)  
- [Git LFS - Reference](https://fakecan.tistory.com/90)  

### 4. What is the console window that pops up when running the game?  
It's a process window for the artificial intelligence. It doesn't cause any harm to your computer.  

### 5. Can I beat the computer?
Yes, but it's more likely at lower levels.  
  
  
## 📚References & Credits

**AI Reference**: <https://stockfishchess.org/>  
**Chess Images, Sound Effects**: <https://www.chess.com/>  
**Sound Voices**: <https://ttsmp3.com/>  
**Other Sounds**: <https://pixabay.com/sound-effects>  
**Other Images**: <https://www.flaticon.com/>, su1jun  

© 2023 su1jun. Creative Commons Attribution.

