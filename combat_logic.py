import pyautogui
import ctypes
import cv2
import numpy as np
import mss
import random
import time

# Получаем разрешение экрана
screen_width, screen_height = pyautogui.size()

# Получаем актуальный DPI scaling
def get_scaling_factor():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width_actual = user32.GetSystemMetrics(0)
    scaling_factor = screen_width_actual / screen_width
    return scaling_factor

# Определяем масштаб в процентах
scaling_factor = get_scaling_factor()

def to_relative(x, y):
    return (x / screen_width, y / screen_height)

def to_absolute(rel_x, rel_y):
    abs_x = int(rel_x * screen_width * scaling_factor)
    abs_y = int(rel_y * screen_height * scaling_factor)
    print(f"Преобразование относительных координат ({rel_x}, {rel_y}) в абсолютные ({abs_x}, {abs_y})")
    return abs_x, abs_y

class Combat:
    def __init__(self, enemy_detector):
        self.enemy_detector = enemy_detector
        self.can_attack_image = cv2.imread("screen_spels/can_attack.png", cv2.IMREAD_GRAYSCALE)
        self.cannot_attack_image = cv2.imread("screen_spels/cannot_attack.png", cv2.IMREAD_GRAYSCALE)
        self.attack_bar_position = (
            to_relative(608, 965), 
            to_relative(1313, 1020)
        )
        self.last_escape_time = time.time() - 2  # Время последнего нажатия Esc

    def capture_attack_bar(self):
        (rel_x1, rel_y1), (rel_x2, rel_y2) = self.attack_bar_position
        x1, y1 = to_absolute(rel_x1, rel_y1)
        x2, y2 = to_absolute(rel_x2, rel_y2)
        
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
            screenshot = np.array(sct.grab(monitor))
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            return gray_screenshot

    def can_attack(self):
        screenshot = self.capture_attack_bar()
        res_can = cv2.matchTemplate(screenshot, self.can_attack_image, cv2.TM_CCOEFF_NORMED)
        res_cannot = cv2.matchTemplate(screenshot, self.cannot_attack_image, cv2.TM_CCOEFF_NORMED)
        
        _, max_val_can, _, _ = cv2.minMaxLoc(res_can)
        _, max_val_cannot, _, _ = cv2.minMaxLoc(res_cannot)

        can_similarity = max_val_can * 100
        cannot_similarity = max_val_cannot * 100

        print(f"Процент схожести с can_attack: {can_similarity:.2f}%, cannot_attack: {cannot_similarity:.2f}%")

        return can_similarity > cannot_similarity

    def attack_enemy(self):
        if self.can_attack():
            print("Враг в зоне досягаемости. Начинаем атаку...")
            key_to_press = str(random.randint(1, 8))
            print(f"Нажата клавиша: {key_to_press}")
            pyautogui.press(key_to_press)
            time.sleep(2)  # Интервал между атаками
        else:
            current_time = time.time()
            # Проверяем, прошло ли достаточно времени с момента последнего нажатия Esc
            if current_time - self.last_escape_time >= 2:  # 2 секунды задержки
                # Нажимаем 'D' перед 'Esc'
                print("Нажатие D перед Esc...")
                pyautogui.keyDown('d')
                d_press_duration = random.uniform(0.1, 0.3)  # Удержание от 0.1 до 0.3 секунд
                time.sleep(d_press_duration)
                pyautogui.keyUp('d')
                print(f"Отпускание D после {d_press_duration:.2f} секунд...")

                # Нажимаем 'Esc' после 'D'
                print("Враг вне зоны досягаемости. Прерывание атаки...")
                pyautogui.press('esc')  # Прерывание текущей цели
                self.last_escape_time = current_time  # Обновляем время последнего нажатия Esc

                d_interval = random.uniform(3, 4)
                print(f"Ожидание {d_interval:.2f} секунд перед следующим нажатием D...")
                time.sleep(d_interval)
            else:
                print("Слишком рано для повторного нажатия Esc.")
