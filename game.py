import pygame
import sys
import json
import os

pygame.init()

# Constants
WINDOWED_RES = (1280, 720)
FPS = 60
SAVE_FILE = "game_data.json"

# Themes
THEMES = {
    "dark": {
        "bg": (10, 20, 40),
        "text": (255, 255, 120),
        "highlight": (255, 200, 0),
        "button_bg": (30, 60, 90),
        "shadow": (0, 0, 0),
        "input_bg": (50, 70, 90)
    },
    "light": {
        "bg": (200, 255, 255),
        "text": (30, 30, 30),
        "highlight": (0, 180, 150),
        "button_bg": (170, 255, 255),
        "shadow": (150, 150, 150),
        "input_bg": (255, 255, 255)
    }
}

# Fonts (کارتونی و شیک)
try:
    FONT_BIG = pygame.font.Font("comic.ttf", 64)
    FONT_MED = pygame.font.Font("comic.ttf", 40)
    FONT_SMALL = pygame.font.Font("comic.ttf", 24)
except:
    FONT_BIG = pygame.font.SysFont("comicsansms", 64)
    FONT_MED = pygame.font.SysFont("comicsansms", 40)
    FONT_SMALL = pygame.font.SysFont("comicsansms", 24)
    FONT_SMALL = pygame.font.SysFont("comicsansms", 18)


# Utility functions
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "current_level": 0,
            "current_part": 0,
            "theme": "dark",
            "fullscreen": False
        }

def save_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


LEVEL_FILE = "Lvl.json"

def load_or_create_levels():
    if os.path.exists(LEVEL_FILE):
        # اگر فایل وجود داشت، آن را بخوان و برگردان
        with open(LEVEL_FILE, "r", encoding="utf-8") as f:
            levels = json.load(f)
        return levels
    else:
        # اگر فایل نبود، سطوح را بساز و ذخیره کن
        levels = []
        for l in range(15):  # 15 سطح
            parts = []
            base = (l + 1) * 10
            for p in range(10):  # 10 قسمت در هر سطح
                first = base + p * 10
                second = first + 10
                answer = second + 10
                parts.append({
                    "sequence": [first, second, None],
                    "answer": answer,
                    "attempts": 0,
                    "solved": False
                })
            levels.append(parts)
        with open(LEVEL_FILE, "w", encoding="utf-8") as f:
            json.dump(levels, f, indent=2, ensure_ascii=False)
        return levels


levels = load_or_create_levels()


# کلاس دکمه‌ها
class Button:
    def __init__(self, text, x, y, w, h, theme, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.theme = theme
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = self.theme["highlight"] if self.hovered else self.theme["button_bg"]
        pygame.draw.rect(screen, color, self.rect, border_radius=12)

        # سایه متن
        shadow_txt = FONT_MED.render(self.text, True, self.theme["shadow"])
        screen.blit(shadow_txt, shadow_txt.get_rect(center=(self.rect.centerx+2, self.rect.centery+2)))

        txt = FONT_MED.render(self.text, True, self.theme["text"])
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event, pos):
        self.hovered = self.rect.collidepoint(pos)
        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN:
            if self.action:
                self.action()

class Game:
    def __init__(self):
        self.data = load_data()
        self.levels = load_or_create_levels()
        self.clock = pygame.time.Clock()
        self.running = True
        self.theme_name = self.data["theme"]
        self.theme = THEMES[self.theme_name]
        self.fullscreen = self.data["fullscreen"]
        self.screen = self.init_display()

        self.buttons = []
        self.build_menu()

        self.state = "menu"
        self.input_value = ""
        self.message = ""
        self.attempts_left = 5

    def reset_progress(self):
        self.data["current_level"] = 0
        self.data["current_part"] = 0
        save_data(self.data)

        for level in self.levels:
            for part in level:
                part["solved"] = False
                part["attempts"] = 0

        with open(LEVEL_FILE, "w", encoding="utf-8") as f:
            json.dump(self.levels, f, ensure_ascii=False, indent=2)

        self.levels = load_or_create_levels()
        self.message = "Game has been reset."
        self.state = "menu"

    def init_display(self):
        if self.fullscreen:
            info = pygame.display.Info()
            try:
                return pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.SCALED)
            except pygame.error:
                return pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        else:
            return pygame.display.set_mode(WINDOWED_RES)


    def switch_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.theme = THEMES[self.theme_name]
        self.build_menu()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.screen = self.init_display()
        self.build_menu()


    def build_menu(self):
        width, height = self.screen.get_size()
        button_width, button_height = 300, 60
        center_x = width // 2 - button_width // 2
        start_y = height // 4

        self.buttons = [
    Button("Start Game", center_x, start_y + 0 * (button_height + 20), button_width, button_height, self.theme, self.start_game),
    Button("Reset Game", center_x, start_y + 1 * (button_height + 20), button_width, button_height, self.theme, self.reset_progress),
    Button("About Game", center_x, start_y + 2 * (button_height + 20), button_width, button_height, self.theme, self.about_game),
    Button(f"Team ({self.theme_name.capitalize()})", center_x, start_y + 3 * (button_height + 20), button_width, button_height, self.theme, self.switch_theme),
    Button("Fullscreen", center_x, start_y + 4 * (button_height + 20), button_width, button_height, self.theme, self.toggle_fullscreen),
    Button("Exit", center_x, start_y + 5 * (button_height + 20), button_width, button_height, self.theme, self.quit_game),
]



    def start_game(self):
        self.state = "game"
        self.input_value = ""
        self.message = ""
        self.attempts_left = 5
        # بارگذاری محل فعلی بازی
        self.current_level = self.data.get("current_level", 0)
        self.current_part = self.data.get("current_part", 0)

    def about_game(self):
        self.state = "about"

    def quit_game(self):
        self.data["theme"] = self.theme_name
        self.data["fullscreen"] = self.fullscreen
        save_data(self.data)
        pygame.quit()
        sys.exit()

    def draw_menu(self):
        self.screen.fill(self.theme["bg"])
        width, height = self.screen.get_size()
        title = FONT_BIG.render("NPA (Number Puzzle Amjadi)", True, self.theme["text"])
        title_rect = title.get_rect(center=(width // 2, height // 6))
        self.screen.blit(title, title_rect)
        for btn in self.buttons:
            btn.draw(self.screen)


    def draw_about(self):
        self.screen.fill(self.theme["bg"])

        lines = [
            ("Builder", True),
            ("Developer: Alireza Amjadi (alirezaamjadi)", False),
            ("Year: 2025", False),
            ("Version: NA-1", False),
            ("Built with Python and VS Code", False),
            ("Developed using Python and Visual Studio Code.", False),
            ("", False),

            ("How to Play:", True),
            ("- 10 puzzles per level.", False),
            ("- Guess the missing number.", False),
            ("- 5 attempts per puzzle.", False),
            ("- Solve to progress.", False),
            ("- Fail: level resets.", False),
            ("- ESC to return.", False),
            ("- Use number keys + ENTER.", False),
            ("", False),

            ("Menu Options:", True),
            ("- Start Game: Begin.", False),
            ("- Reset Game: Clear progress.", False),
            ("- About Game: Info.", False),
            ("- Theme: Toggle mode.", False),
            ("- Fullscreen: Toggle.", False),
            ("- Exit: Quit.", False),
            ("", False),

            ("Click or ESC to return.", False)
        ]

        red = (255, 100, 100)
        line_height = 26
        start_y = 100

        for i, (line, is_header) in enumerate(lines):
            color_text = red if is_header else self.theme["text"]
            color_shadow = self.theme["shadow"]

            shadow = FONT_SMALL.render(line, True, color_shadow)
            txt = FONT_SMALL.render(line, True, color_text)
            self.screen.blit(shadow, (80 + 2, start_y + i * line_height + 2))
            self.screen.blit(txt, (80, start_y + i * line_height))




    def draw_game(self):
        self.screen.fill(self.theme["bg"])

        level_text = FONT_MED.render(f"Level: {self.current_level+1}/15", True, self.theme["highlight"])
        part_text = FONT_MED.render(f"Part: {self.current_part+1}/10", True, self.theme["highlight"])
        self.screen.blit(level_text, (30, 20))
        self.screen.blit(part_text, (30, 70))

        part = self.levels[self.current_level][self.current_part]
        seq = part["sequence"]

        # نمایش دنباله با جای خالی (علامت سوال)
        seq_str = "  .  ".join(str(x) if x is not None else "?" for x in seq)
        seq_text = FONT_BIG.render(seq_str, True, self.theme["text"])
        shadow = FONT_BIG.render(seq_str, True, self.theme["shadow"])
        seq_rect = seq_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 60))
        self.screen.blit(shadow, seq_rect.move(3,3))
        self.screen.blit(seq_text, seq_rect)

        # نمایش ورودی کاربر
        input_display = FONT_MED.render(f"Your Guess: {self.input_value}", True, self.theme["highlight"])
        self.screen.blit(input_display, (self.screen.get_width()//2 - 200, self.screen.get_height()//2 + 40))

        # نمایش پیام‌ها
        msg_text = FONT_MED.render(self.message, True, self.theme["highlight"])
        self.screen.blit(msg_text, (self.screen.get_width()//2 - 200, self.screen.get_height()//2 + 90))

        # نمایش تلاش‌های باقی مانده
        attempts_text = FONT_MED.render(f"Attempts Left: {self.attempts_left}", True, self.theme["highlight"])
        self.screen.blit(attempts_text, (self.screen.get_width() - 300, 20))

    def handle_game_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_value = self.input_value[:-1]
            elif event.key == pygame.K_RETURN:
                self.check_answer()
            elif event.unicode.isdigit():
                self.input_value += event.unicode

    def check_answer(self):
        part = self.levels[self.current_level][self.current_part]
        try:
            guess = int(self.input_value)
        except ValueError:
            self.message = "Please enter a valid number!"
            self.input_value = ""
            return

        if guess == part["answer"]:
            self.message = "Correct! Moving to next part."
            part["solved"] = True
            part["attempts"] = 0
            self.next_part()
        else:
            self.attempts_left -= 1
            part["attempts"] += 1
            if self.attempts_left == 0:
                self.message = "You lost! Restarting level..."
                # ریست پارت‌ها و تلاش‌ها
                self.reset_level()
            else:
                self.message = f"Wrong! Try again. Attempts left: {self.attempts_left}"
        self.input_value = ""

    def next_part(self):
        self.current_part += 1
        if self.current_part >= 10:
            self.current_part = 0
            self.current_level += 1
            if self.current_level >= 15:
                self.message = "Congratulations! You completed all levels!"
                self.state = "menu"
                self.current_level = 0
        self.attempts_left = 5
        self.data["current_level"] = self.current_level
        self.data["current_part"] = self.current_part
        save_data(self.data)

    def reset_level(self):
        # ریست کردن تمام پارت‌ها در این سطح
        for part in self.levels[self.current_level]:
            part["solved"] = False
            part["attempts"] = 0
        self.attempts_left = 5
        self.input_value = ""
        self.message = ""
        self.current_part = 0
        self.data["current_part"] = 0
        save_data(self.data)

    def run(self):
        while self.running:
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (2, 4, 5):
                        # اسکرول موس را نادیده بگیر
                        pass
                    else:
                        if self.state == "menu":
                            for btn in self.buttons:
                                btn.handle_event(event, pos)
                        elif self.state == "about":
                            self.state = "menu"

                elif event.type == pygame.KEYDOWN:
                    if self.state == "game":
                        if event.key == pygame.K_ESCAPE:
                            # ذخیره و برگشت به منو
                            self.data["current_level"] = self.current_level
                            self.data["current_part"] = self.current_part
                            save_data(self.data)
                            self.state = "menu"
                            self.message = ""
                            self.input_value = ""
                        else:
                            self.handle_game_input(event)

            # آپدیت وضعیت hover دکمه‌ها در منو
            if self.state == "menu":
                for btn in self.buttons:
                    btn.hovered = btn.rect.collidepoint(pos)

            # رسم صفحه مناسب
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "about":
                self.draw_about()
            elif self.state == "game":
                self.draw_game()

            pygame.display.flip()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.run()
