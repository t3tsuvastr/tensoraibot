import tkinter as tk
from tkinter import ttk
import os
import subprocess
import signal

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WoW Bot Manager")
        self.root.geometry("400x300")
        self.processes = []  # Список для хранения запущенных процессов

        self.create_tabs()

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)

        self.main_frame = tk.Frame(self.notebook)
        self.windows_frame = tk.Frame(self.notebook)
        self.profile_frame = tk.Frame(self.notebook)

        self.notebook.add(self.main_frame, text="Главная")
        self.notebook.add(self.windows_frame, text="Окна")
        self.notebook.add(self.profile_frame, text="Профиль")

        self.notebook.pack(expand=True, fill="both")

        self.create_main_tab()
        self.create_windows_tab()
        self.create_profile_tab()

    def create_main_tab(self):
        tk.Button(self.main_frame, text="Старт гринда ресурсов", command=self.start_grind).pack(pady=10)
        tk.Button(self.main_frame, text="Старт прокачки лвл", command=self.start_leveling).pack(pady=10)
        tk.Button(self.main_frame, text="Старт прокачки репутации", command=self.start_reputation).pack(pady=10)
        tk.Button(self.main_frame, text="Старт гринда боешек", command=self.start_grind_boesh).pack(pady=10)
        tk.Button(self.main_frame, text="Старт гринда маунтов", command=self.start_mount_farm).pack(pady=10)
        tk.Button(self.main_frame, text="Стоп", command=self.stop_all_processes, fg="red").pack(pady=10)  # Кнопка Стоп

    def create_windows_tab(self):
        tk.Label(self.windows_frame, text="Настройки окон").pack(pady=10)
        tk.Button(self.windows_frame, text="Добавить аккаунт", command=self.add_account).pack(pady=10)

    def create_profile_tab(self):
        tk.Label(self.profile_frame, text="Настройки профиля").pack(pady=10)
        tk.Button(self.profile_frame, text="Выйти из аккаунта", command=self.logout).pack(pady=10)

    def start_grind(self):
        self.run_script("scripts/grind_resources.py")

    def start_leveling(self):
        self.run_script("scripts/leveling.py")

    def start_reputation(self):
        self.run_script("scripts/reputation.py")

    def start_grind_boesh(self):
        self.run_script("main.py")

    def start_mount_farm(self):
        self.run_script("scripts/mount_farm.py")

    def add_account(self):
        pass

    def logout(self):
        pass

    def run_script(self, script_path):
        process = subprocess.Popen(["python", script_path])
        self.processes.append(process)  # Сохраняем процесс в список

    def stop_all_processes(self):
        for process in self.processes:
            process.terminate()  # Отправляем сигнал на завершение процесса
            try:
                process.wait(timeout=5)  # Ожидаем завершения процесса
            except subprocess.TimeoutExpired:
                process.kill()  # Принудительно убиваем процесс, если он не завершился
        self.processes.clear()  # Очищаем список процессов

if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()
