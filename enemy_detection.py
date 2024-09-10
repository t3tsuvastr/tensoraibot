import pyautogui
import ctypes
import cv2
import numpy as np
import mss

# Получаем разрешение экрана
screen_width, screen_height = pyautogui.size()

def get_scaling_factor():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width_actual = user32.GetSystemMetrics(0)
    screen_height_actual = user32.GetSystemMetrics(1)
    scaling_factor = screen_width_actual / screen_width
    return scaling_factor

scaling_factor = get_scaling_factor()

def to_relative(x, y):
    return (x / screen_width, y / screen_height)

def to_absolute(rel_x, rel_y):
    abs_x = int(rel_x * screen_width * scaling_factor)
    abs_y = int(rel_y * screen_height * scaling_factor)
    print(f"Преобразование относительных координат ({rel_x}, {rel_y}) в абсолютные ({abs_x}, {abs_y})")
    return abs_x, abs_y

def to_absolute_size(rel_w, rel_h):
    abs_w = int(rel_w * screen_width * scaling_factor)
    abs_h = int(rel_h * screen_height * scaling_factor)
    print(f"Преобразование относительных размеров ({rel_w}, {rel_h}) в абсолютные ({abs_w}, {abs_h})")
    return abs_w, abs_h

class EnemyDetector:
    def __init__(self, reference_image_path):
        self.enemy_frame_position = (
            to_relative(1368, 696),  # Преобразование координат x и y
            to_relative(6, 12)       # Преобразование ширины и высоты
        )
        self.reference_image = cv2.imread(reference_image_path)

    def capture_enemy_frame(self):
        # Получаем относительные координаты области врага и преобразуем их обратно в абсолютные
        (rel_x, rel_y), (rel_w, rel_h) = self.enemy_frame_position
        x, y = to_absolute(rel_x, rel_y)
        w, h = to_absolute_size(rel_w, rel_h)  # Используем отдельную функцию для размеров

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            screenshot = np.array(sct.grab(monitor))
            return screenshot[:, :, :3]

    def detect_enemy(self):
        enemy_frame = self.capture_enemy_frame()
        if enemy_frame is None or self.reference_image is None:
            print("Ошибка: не удалось захватить изображение или эталонное изображение отсутствует.")
            return False

        # Изменяем размер эталонного изображения, чтобы оно совпадало с текущим размером
        if enemy_frame.shape != self.reference_image.shape:
            self.reference_image = cv2.resize(self.reference_image, (enemy_frame.shape[1], enemy_frame.shape[0]))

        diff = cv2.absdiff(enemy_frame, self.reference_image)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero_count = np.count_nonzero(diff_gray)
        total_pixels = diff_gray.size

        similarity_percentage = 100 - (non_zero_count / total_pixels * 100)
        print(f"Процент схожести с эталонным изображением врага: {similarity_percentage}%")

        return similarity_percentage > 10  # Порог обнаружения врага, можно настроить
