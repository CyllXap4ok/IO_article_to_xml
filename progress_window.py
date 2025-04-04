import time
import tkinter as tk
from tkinter import ttk
from typing import Callable


class ProgressWindow:
    __current_progress = 0

    def __init__(self, root):
        self.__root = root
        self.__window = None
        self.__progress_label = None
        self.__progressbar = None


    def open(self):
        if self.__window is None:
            self.__window = tk.Toplevel(self.__root)
            self.__window.title("Извлечение...")
            self.__window.resizable(False, False)

            self.__progress_label = tk.Label(self.__window, text="0%")
            self.__progress_label.pack()

            self.__progressbar = ttk.Progressbar(self.__window, length=300, mode='determinate')
            self.__progressbar.pack()

            self.__center_on_parent(self.__root)
            self.__window.grab_set()
            self.__window.focus_force()


    def close(self):
        self.__window.destroy()
        self.__window = None
        self.__current_progress = 0


    def update_progress(self, percent, on_finish: Callable[[], None] = 'close'):
        self.__current_progress += percent
        self.__progressbar['value'] = self.__current_progress
        self.__progress_label.config(text=f"{int(self.__current_progress)}%")
        self.__window.update_idletasks()
        time.sleep(0.1)
        if on_finish == 'close': on_finish = self.close
        if self.__current_progress >= 100: on_finish()


    def __center_on_parent(self, parent):
        self.__window.update_idletasks()
        # Получаем реальные размеры окна прогресса
        width = self.__window.winfo_reqwidth()
        height = self.__window.winfo_reqheight()

        # Получаем позицию и размер родительского окна
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Вычисляем позицию для центрирования
        x = parent_x + abs((parent_width - width)) // 2
        y = parent_y + abs((parent_height - height)) // 2

        # Устанавливаем позицию без изменения размеров
        self.__window.geometry(f"+{x}+{y}")