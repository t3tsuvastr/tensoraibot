import pyautogui

# Получаем разрешение экрана
screen_width, screen_height = pyautogui.size()

# Масштаб в процентах, учтем 125%
scaling_factor = 1.25

# Функция для преобразования абсолютных координат в относительные
def to_relative(x, y):
    return (x / screen_width, y / screen_height)

# Преобразование относительных координат в реальные координаты экрана с учетом масштаба
def to_absolute(rel_x, rel_y):
    abs_x = int(rel_x * screen_width * scaling_factor)
    abs_y = int(rel_y * screen_height * scaling_factor)
    print(f"Преобразование относительных координат ({rel_x}, {rel_y}) в абсолютные ({abs_x}, {abs_y})")
    return abs_x, abs_y

# Пример использования
relative_x, relative_y = to_relative(100, 200)  # Преобразуем в относительные координаты
absolute_x, absolute_y = to_absolute(relative_x, relative_y)  # Преобразуем обратно в абсолютные с учетом масштаба

print(f"Relative coordinates: ({relative_x:.2f}, {relative_y:.2f})")
print(f"Absolute coordinates with scaling: ({absolute_x}, {absolute_y})")
