import time
import random
import pyautogui
from hp_detection import HealthDetector

class Healer:
    def __init__(self, health_detector):
        self.health_detector = health_detector

    def heal(self):
        health_percentage = self.health_detector.compare_health()
        print(f"Текущее здоровье: {health_percentage}%")
        
        if 51 <= health_percentage < 80:
            self.cast_rejuvenation()
        elif health_percentage <= 50:
            self.cast_regrowth()

    def cast_rejuvenation(self):
        print("Применение Rejuvenation...")
        pyautogui.press('9')
        time.sleep(1.5 + random.uniform(0.1, 0.3))  # Кулдаун и рандомизация

    def cast_regrowth(self):
        print("Применение Regrowth...")
        pyautogui.press('0')
        time.sleep(1.5 + random.uniform(0.1, 0.3))  # Время каста и рандомизация
