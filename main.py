from hp_detection import HealthDetector
from healing_logic import Healer
from enemy_detection import EnemyDetector
from combat_logic import Combat
from combat_manager import CombatManager
from loot_manager import LootManager
import threading
import time

def monitor_health(healer):
    while True:
        healer.heal()
        time.sleep(6)  # Интервал проверки здоровья каждые 6 секунд

def manage_combat(combat_manager):
    while True:
        combat_manager.manage_combat()
        time.sleep(1)  # Интервал между проверками противников

def main():
    # Путь к эталонным изображениям
    health_reference_image_path = "path_to_full_health_image.png"
    enemy_reference_image_path = "path_to_enemy_frame_image.png"
    loot_reference_image_paths = [
        "screen_loot/reference_image1.png", 
        "screen_loot/reference_image2.png"
    ]

    # Инициализация объектов для детекции здоровья, врагов и лута
    health_detector = HealthDetector(health_reference_image_path)
    enemy_detector = EnemyDetector(enemy_reference_image_path)
    loot_manager = LootManager(loot_reference_image_paths)

    # Инициализация объектов для лечения и боя
    healer = Healer(health_detector)
    combat = Combat(enemy_detector)
    combat_manager = CombatManager(enemy_detector, combat, loot_manager)

    # Запуск мониторинга здоровья в отдельном потоке
    health_thread = threading.Thread(target=monitor_health, args=(healer,))
    health_thread.start()

    # Запуск управления боем и лутанием
    combat_thread = threading.Thread(target=manage_combat, args=(combat_manager,))
    combat_thread.start()

    # Ждём завершения потоков (в данном случае они работают бесконечно, так что это будет работать постоянно)
    health_thread.join()
    combat_thread.join()

if __name__ == "__main__":
    main()
