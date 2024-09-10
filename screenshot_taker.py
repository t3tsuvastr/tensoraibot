import cv2
import numpy as np
import mss
import os
import time

class SkillBarDetector:
    def __init__(self):
        self.skill_bar_position = (1368, 696, 1370, 705)  # Новые координаты области панели способностей
        self.screenshot_dir = "skill_bar_screenshots"  # Директория для сохранения скриншотов
        self.max_screenshots = 5  # Максимальное количество сохраняемых скриншотов

        # Создаем директорию для скриншотов, если она не существует
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def capture_skill_bar(self) -> np.ndarray:
        x1, y1, x2, y2 = self.skill_bar_position
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
            screenshot = np.array(sct.grab(monitor))
            return screenshot[:, :, :3]

    def save_screenshot(self, screenshot, index):
        filename = os.path.join(self.screenshot_dir, f"skill_bar_{index}.png")
        cv2.imwrite(filename, screenshot)
        print(f"Скриншот сохранен: {filename}")

    def cycle_screenshots(self):
        screenshot_index = 0
        while True:
            skill_bar = self.capture_skill_bar()
            self.save_screenshot(skill_bar, screenshot_index)
            screenshot_index = (screenshot_index + 1) % self.max_screenshots
            time.sleep(5)  # Ожидание 5 секунд перед следующим скриншотом

# Пример использования
if __name__ == "__main__":
    skill_bar_detector = SkillBarDetector()
    skill_bar_detector.cycle_screenshots()
