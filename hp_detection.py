import cv2
import numpy as np
import mss
import pyautogui
import ctypes  # Для работы с Windows API
import time

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

# Преобразование относительных размеров в реальные размеры экрана с учетом DPI масштабирования
def to_absolute_size(rel_w, rel_h):
    abs_w = int(rel_w * screen_width * scaling_factor)
    abs_h = int(rel_h * screen_height * scaling_factor)
    print(f"Преобразование относительных размеров ({rel_w}, {rel_h}) в абсолютные ({abs_w}, {abs_h})")
    return abs_w, abs_h

class HealthDetector:
    def __init__(self, reference_image_path):
        # Установленные координаты области здоровья на экране в относительных значениях
        self.health_bar_position = (
            to_relative(491, 694),  # Координаты x и y
            to_relative(64, 22)     # Ширина и высота
        )
        self.reference_image = cv2.imread(reference_image_path)

    def capture_health_bar(self):
        # Получаем относительные координаты области здоровья и преобразуем их обратно в абсолютные
        (rel_x, rel_y), (rel_w, rel_h) = self.health_bar_position
        x, y = to_absolute(rel_x, rel_y)
        w, h = to_absolute_size(rel_w, rel_h)  # Используем отдельную функцию для размеров

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            screenshot = np.array(sct.grab(monitor))
            return screenshot[:, :, :3]  # Убираем альфа-канал

    def compare_health(self):
        health_bar = self.capture_health_bar()
        if health_bar is None or self.reference_image is None:
            print("Ошибка: не удалось захватить изображение или эталонное изображение отсутствует.")
            return 0.0

        # Приведение к одному размеру, если необходимо
        if health_bar.shape != self.reference_image.shape:
            self.reference_image = cv2.resize(self.reference_image, (health_bar.shape[1], health_bar.shape[0]))

        # Сравниваем захваченное изображение с эталонным
        diff = cv2.absdiff(health_bar, self.reference_image)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero_count = np.count_nonzero(diff_gray)
        total_pixels = diff_gray.size

        # Рассчитываем процент оставшегося здоровья
        similarity_percentage = 100 - (non_zero_count / total_pixels * 100)
        print(f"Процент схожести с эталонным изображением: {similarity_percentage}%")

        return similarity_percentage

# Пример использования
if __name__ == "__main__":
    health_detector = HealthDetector("path_to_full_health_image.png")

    # Цикл для мониторинга здоровья
    while True:
        health_percentage = health_detector.compare_health()
        print(f"Текущее здоровье: {health_percentage}%")
        time.sleep(1)  # Задержка в 1 секунду между проверками
