import tkinter as tk
from tkinter import filedialog
from typing import Callable
from pathlib import Path

from progress_window import ProgressWindow
from data.enum_const import FileType
from view_model.main_view_model import MainViewModel


class InfoExtractorApp:
    view_model = MainViewModel()

    def __init__(self, root):
        self.root = root
        self.root.title('InfoExtractorApp')
        self.root.minsize(400, 250)
        self.labels = []

        # Окно прогресса | открывается при вызове open()
        progress_window = ProgressWindow(root)

        # Создаем надписи и кнопки
        self.file_selector_button(
            name='Article',
            button_command=lambda: (
                self.select_file(
                    file_type=FileType.Article,
                    extensions=['.docx'],
                    index = 0
                )
            )
        )
        self.file_selector_button(
            name='Essential information',
            button_command=lambda: (
                self.select_file(
                    file_type=FileType.EssentialInfo,
                    extensions=['.docx'],
                    index=1
                )
            )
        )
        self.file_selector_button(
            name='Reviews',
            button_command=lambda: (
                self.select_files(
                    file_type=FileType.Review,
                    extensions=['.docx'],
                    index=2
                )
            )
        )

        # Кнопка для извлечения информации
        tk.Button(
            root,
            text='Извлечь информацию',
            command=lambda: (
                progress_window.open(),
                self.view_model.extract_data(progress_window.update_progress),
                self.view_model.save_data(self.select_saving_path(), progress_window.update_progress)
            )
        ).pack(anchor=tk.NE, padx=5, pady=5)

        # Кнопка для создания выпуска
        tk.Button(
            root,
            text='Сформировать выпуск',
            command=lambda: ()
        ).pack(pady=10, side=tk.BOTTOM)

    def file_selector_button(self, name: str, button_command: Callable[[], None]):
        frame = tk.Frame(self.root)
        frame.pack(pady=5, padx=5, fill='x')

        label = tk.Label(frame, text=name,  fg="gray")
        label.pack(side=tk.LEFT)
        self.labels.append(label)

        button = tk.Button(frame, text='Выбрать файл', command=button_command)
        button.pack(side=tk.RIGHT)

    def select_files(self, file_type: FileType, extensions: list[str], index: int):
        file_paths = list(filedialog.askopenfilenames(filetypes=[('Word Documents', extensions)]))

        if file_paths:
            self.view_model.set_file_paths(file_type, file_paths)
            self.labels[index].config(text=', '.join([Path(path).name for path in file_paths]), fg='black')

    def select_file(self, file_type: FileType, extensions: list[str], index: int):
        path = filedialog.askopenfilename(filetypes=[('Word Documents', extensions)])

        if path:
            self.view_model.set_file_paths(file_type, [path])
            self.labels[index].config(text=Path(path).name, fg='black')

    def select_saving_path(self) -> str:
        article_path = self.view_model.get_article_path()
        article_name = Path(article_path).stem

        saving_path = filedialog.asksaveasfilename(
            title='Сохранить файл',
            initialdir=Path(article_path).parent,
            initialfile=article_name + '_EL.xml',
            defaultextension='',
            filetypes=[('XML', '.xml')]
        )

        return str(Path(saving_path).with_suffix(''))

if __name__ == "__main__":
    root = tk.Tk()
    app = InfoExtractorApp(root)
    root.mainloop()