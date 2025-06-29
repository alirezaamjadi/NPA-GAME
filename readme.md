
# 🎮 Game Code - NPA (Number Puzzle Amjadi)  
**سازنده:** علیرضا امجدی | **Developer:** Alireza Amjadi  

---

## 🕹️ معرفی بازی | Game Introduction  
بازی NPA یک پازل عددی جذاب است که با استفاده از Python و Pygame ساخته شده است.  
NPA is a fun number puzzle game made with Python and Pygame.

---

## 📂 ساختار فایل‌ها | File Structure  

- **game.py**  
  فایل اصلی بازی که منوی بازی، اجرای مراحل، تعامل با کاربر و ذخیره‌سازی اطلاعات بازی را مدیریت می‌کند.  
  The main game file managing menus, gameplay, user interaction, and saving data.

- **Lvl.json**  
  فایل JSON که شامل ساختار سطوح و پازل‌های بازی است.  
  A JSON file containing all levels and puzzles data.

- **game_data.json**  
  فایل ذخیره‌سازی پیشرفت بازی مانند سطح فعلی، بخش فعلی، تنظیمات تم و حالت فول‌اسکرین.  
  Saves player progress, theme choice, fullscreen state, current level and part.

- **Q.create.py**  
  (اگر وجود دارد) اسکریپتی برای ایجاد یا مدیریت سوالات و پازل‌ها.  
  Script for generating or managing puzzles/questions (if exists).

---

## ⚙️ ویژگی‌ها | Features  
- دو تم روشن و تاریک با رنگ‌های زیبا و چشم‌نواز.  
- Two beautiful themes: Light and Dark.  
- ذخیره خودکار پیشرفت بازی و تنظیمات کاربر.  
- Auto-save of player progress and settings.  
- نمایش پیام‌ها، تعداد تلاش‌های باقی‌مانده، و ورودی کاربر در طول بازی.  
- Shows messages, attempts left, and user input during gameplay.  
- سیستم ریست سطح و بازی برای شروع مجدد.  
- Level and game reset system to start fresh.  
- منوی کامل با گزینه‌هایی مثل شروع بازی، ریست بازی، درباره بازی، تغییر تم، حالت فول‌اسکرین، و خروج.  
- Full-featured menu with Start, Reset, About, Theme switch, Fullscreen toggle, Exit.  
- بخش درباره بازی شامل اطلاعات سازنده، آموزش بازی و ساختار فنی با موشن و انیمیشن جذاب.  
- About section with developer info, game instructions, tech structure, with smooth animation.

---

## 📝 آموزش بازی | How To Play  
- هر سطح شامل 10 پازل عددی است.  
- Each level contains 10 number puzzles.  
- باید عدد گمشده دنباله را حدس بزنید.  
- Guess the missing number in the sequence.  
- هر پازل 5 تلاش دارد.  
- Each puzzle gives you 5 attempts.  
- پس از حل، به پازل بعدی می‌روید.  
- After solving, you proceed to the next puzzle.  
- اگر همه تلاش‌ها تمام شود، سطح ریست می‌شود.  
- If attempts run out, the level resets.  
- ESC برای برگشت به منو استفاده می‌شود.  
- Press ESC to return to menu.

---

## 💾 نصب و اجرای بازی | Installation & Running  
برای اجرای بازی به Python و کتابخانه Pygame نیاز دارید:  
You need Python and Pygame library installed:  

```bash
pip install pygame
````

سپس کافی است فایل `game.py` را اجرا کنید:
Run `game.py` to start the game:

```bash
python game.py
```

---

## 📥 دانلود بازی | Download

برای بازی کردن می‌توانید به برنچ `game file` در مخزن GitHub مراجعه کنید و بازی را دانلود کنید.
To play, visit the `game file` branch on GitHub repository and download the game files.

---

## 🎨 تکنولوژی‌ها و ابزارها | Technologies & Tools

* Python 3.x
* Pygame
* VS Code (ساخت و توسعه با Visual Studio Code)
* JSON برای ذخیره‌سازی داده‌ها

---


