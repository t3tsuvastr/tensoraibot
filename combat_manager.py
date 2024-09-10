import time
import pyautogui
import random
from enemy_detection import EnemyDetector
from combat_logic import Combat
from loot_manager import LootManager

class CombatManager:
    def __init__(self, enemy_detector, combat, loot_manager):
        self.enemy_detector = enemy_detector
        self.combat = combat
        self.loot_manager = loot_manager
        self.enemy_found = False
        self.last_escape_time = time.time() - 2  # Инициализация времени для 'Esc'
        self.last_d_time = time.time() - 4  # Инициализация времени для 'D'

    def manage_combat(self):
        while True:
            if self.enemy_detector.detect_enemy():
                if not self.enemy_found:
                    print("Враг обнаружен! Переключение на атаку...")
                    self.enemy_found = True

                # Включаем проверку на возможность атаки перед атакой
                if self.combat.can_attack():
                    self.combat.attack_enemy()
                else:
                    print("Враг вне зоны досягаемости. Прерывание атаки...")
                    current_time = time.time()
                    if current_time - self.last_escape_time >= 2:
                        pyautogui.press('esc')  # Прерывание текущей цели
                        self.last_escape_time = current_time
                    self.enemy_found = False

            else:
                if self.enemy_found:
                    print("Враг не обнаружен. Переключение на поиск...")
                    self.enemy_found = False

                # Логика нажатия TAB для поиска врагов
                for i in range(7):  # Цикл увеличен до 7 повторений
                    print(f"Проверка {i + 1}: Нажатие TAB...")
                    pyautogui.press('tab')
                    tab_interval = random.uniform(0.5, 1.1)
                    print(f"Ожидание {tab_interval:.2f} секунд перед следующим нажатием TAB...")
                    time.sleep(tab_interval)
                    
                    if self.enemy_detector.detect_enemy():
                        print("Враг обнаружен после TAB. Переключение на атаку...")
                        self.enemy_found = True
                        break

                    print(f"Проверка {i + 1}: Нажатие D...")
                    pyautogui.keyDown('d')
                    d_press_duration = random.uniform(0.1, 0.3)  # Удержание от 0.1 до 0.3 секунд
                    time.sleep(d_press_duration)
                    pyautogui.keyUp('d')
                    print(f"Отпускание D после {d_press_duration:.2f} секунд...")

                    # Ожидание перед следующим циклом от 0.5 до 1.1 секунд
                    d_interval = random.uniform(0.5, 1.1)
                    print(f"Ожидание {d_interval:.2f} секунд перед следующим нажатием D...")
                    time.sleep(d_interval)
                    self.last_d_time = time.time()  # Обновляем время последнего нажатия D

                # Если после семи проверок враг не найден, начинаем лутание
                if not self.enemy_found:
                    print("Врагов не обнаружено после семи проверок. Начинаем лутание...")
                    self.loot_manager.loot()

if __name__ == "__main__":
    reference_enemy_image_path = "path_to_enemy_image.png"
    reference_loot_image_path = "path_to_loot_image.png"
    
    enemy_detector = EnemyDetector(reference_enemy_image_path)
    combat = Combat(enemy_detector)
    loot_manager = LootManager(reference_loot_image_path)
    
    combat_manager = CombatManager(enemy_detector, combat, loot_manager)
    combat_manager.manage_combat()
