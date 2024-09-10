import cv2
import numpy as np
import mss
import pyautogui
import os
import time
import ctypes  # Для работы с Windows API

# Получаем разрешение экрана
screen_width, screen_height = pyautogui.size()

# Получаем актуальный DPI scaling
def get_scaling_factor():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # Разрешаем приложению работать с DPI
    screen_width_actual = user32.GetSystemMetrics(0)
    screen_height_actual = user32.GetSystemMetrics(1)
    scaling_factor = screen_width_actual / screen_width
    return scaling_factor

# Определяем масштаб в процентах
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

# Преобразование относительных размеров в реальные размеры экрана с учетом DPI масштабирования
def to_absolute_size(rel_w, rel_h):
    abs_w = int(rel_w * screen_width * scaling_factor)
    abs_h = int(rel_h * screen_height * scaling_factor)
    print(f"Преобразование относительных размеров ({rel_w}, {rel_h}) в абсолютные ({abs_w}, {abs_h})")
    return abs_w, abs_h

class HealthDetector:
    def __init__(self, reference_image_path):
        self.health_bar_position = (
            to_relative(1368, 696),  # Преобразование координат x и y
            to_relative(6, 12)     # Преобразование ширины и высоты
        )
        self.reference_image = cv2.imread(reference_image_path)

    def capture_health_bar(self):
        # Получаем относительные координаты области здоровья и преобразуем их обратно в абсолютные
        (rel_x, rel_y), (rel_w, rel_h) = self.health_bar_position
        x, y = to_absolute(rel_x, rel_y)
        w, h = to_absolute_size(rel_w, rel_h)

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            screenshot = np.array(sct.grab(monitor))
            return screenshot[:, :, :3]  # Убираем альфа-канал

    def save_health_screenshot(self):
        # Захват области здоровья
        health_bar = self.capture_health_bar()

        # Проверка, что скриншот получен
        if health_bar is None or health_bar.size == 0:
            print("Ошибка: не удалось захватить область здоровья.")
            return

        # Создание папки health_screenshots, если она не существует
        os.makedirs('health_screenshots', exist_ok=True)

        # Сохранение скриншота в папку с уникальным именем
        screenshot_path = os.path.join('health_screenshots', f'health_screenshot_{int(time.time())}.png')
        cv2.imwrite(screenshot_path, health_bar)
        print(f"Скриншот области здоровья сохранен в {screenshot_path}")

# Пример использования
if __name__ == "__main__":
    health_detector = HealthDetector("path_to_full_health_image.png")

    # Бесконечный цикл для захвата скриншотов каждую секунду
    while True:
        health_detector.save_health_screenshot()
        time.sleep(1)  # Задержка в 1 секунду между скриншотами
