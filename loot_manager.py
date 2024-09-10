import time
import pyautogui
import random
import cv2
import numpy as np
import mss
import ctypes  # Для работы с Windows API
from typing import List

# Получаем разрешение экрана
screen_width, screen_height = pyautogui.size()

# Получаем актуальный DPI scaling
def get_scaling_factor():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width_actual = user32.GetSystemMetrics(0)
    screen_height_actual = user32.GetSystemMetrics(1)
    scaling_factor = screen_width_actual / screen_width
    return scaling_factor

scaling_factor = get_scaling_factor()

# Функция для преобразования абсолютных координат в относительные
def to_relative(x, y):
    return (x / screen_width, y / screen_height)

# Преобразование относительных координат в реальные координаты экрана с учетом DPI масштабирования
def to_absolute(rel_x, rel_y):
    abs_x = int(rel_x * screen_width * scaling_factor)
    abs_y = int(rel_y * screen_height * scaling_factor)
    print(f"Преобразование относительных координат ({rel_x}, {rel_y}) в абсолютные ({abs_x}, {abs_y})")
    return abs_x, abs_y

class LootManager:
    def __init__(self, reference_image_paths: List[str]):
        self.reference_images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in reference_image_paths]

    def loot_corpses(self):
        """Лутание трупов, нажимая '2' на нампаде в течение 3 секунд с задержкой 0.2-0.4 секунды между нажатиями."""
        start_time = time.time()
        while time.time() - start_time < 3:  # Лутание в течение 3 секунд
            pyautogui.press('num2')  # Нажатие на '2' на нампаде
            delay = random.uniform(0.2, 0.4)  # Рандомная задержка между нажатиями
            print(f"Нажатие '2' на нампаде. Ожидание {delay:.2f} секунд перед следующим нажатием.")
            time.sleep(delay)

    def turn_right(self):
        """Поворот вправо, удерживая 'd' на случайное время от 0.1 до 0.3 секунд."""
        press_duration = random.uniform(0.1, 0.3)
        print(f"Нажатие 'd' на {press_duration:.2f} секунд для поворота вправо.")
        pyautogui.keyDown('d')
        time.sleep(press_duration)
        pyautogui.keyUp('d')

    def loot(self):
        for _ in range(7):  # Повторяем процесс до 7 раз
            self.loot_corpses()
            self.turn_right()
        print("Лутание завершено. Возвращаемся к фарму крипов.")

if __name__ == "__main__":
    reference_image_paths = [
        "screen_loot/reference_image1.png", 
        "screen_loot/reference_image2.png"
    ]  # Список путей к эталонным изображениям
    loot_manager = LootManager(reference_image_paths)
    loot_manager.loot()
