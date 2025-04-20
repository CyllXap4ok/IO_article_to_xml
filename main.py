import os
import tkinter as tk

from tkinter import filedialog
from progress_window import ProgressWindow
from typing import Callable

from data_utils.extractor.data_extractor import DataExtractor
from data_utils.extractor.extraction_strategy import ArticleExtractionStrategy, ReviewExtractionStrategy
from data_utils.saver.data_saver import DataSaver
from data_utils.enum_const import FileType
from data_utils.article import ArticleData


class InfoExtractorApp:
    article_data = ArticleData()

    def __init__(self, root):
        self.root = root
        self.root.title('InfoExtractorApp')
        self.root.minsize(400, 250)

        self.labels = []
        self.filepaths: dict[FileType, list[str]] = {}

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
                self.extract_data(progress_callback=progress_window.update_progress),
                DataSaver().save_data(
                    saving_path=filedialog.asksaveasfilename(
                        title='Сохранить файл',
                        defaultextension='',
                        filetypes=[('All files', '*')]
                    ),
                    article_data=self.article_data
                ),
                self.article_data.clear()
            )
        ).pack(anchor=tk.NE, padx=5, pady=5)

        # Кнопка для создания выпуска
        tk.Button(
            root,
            text='Сформировать выпуск',
            command=lambda: ()
        ).pack(pady=10, side=tk.BOTTOM)

    def extract_data(self, progress_callback: Callable):
        data_extractor = DataExtractor()
        total_elements = sum(map(len, self.filepaths.values()))

        for file_type, paths in self.filepaths.items():
            """ Устанавливаем стратегию в зависимости от типа файлов """
            match file_type:
                case (FileType.Article): data_extractor.set_strategy(ArticleExtractionStrategy())
                case (FileType.Review): data_extractor.set_strategy(ReviewExtractionStrategy())

            for path in paths:
                """ Извлекаем информацию и обновляем прогресс """
                data_extractor.extract_data(path, self.article_data)
                progress_callback(100 / total_elements)

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
            self.filepaths[file_type] = file_paths
            self.labels[index].config(text=', '.join([os.path.basename(path) for path in file_paths]), fg='black')

    def select_file(self, file_type: FileType, extensions: list[str], index: int):
        file_path = filedialog.askopenfilename(filetypes=[('Word Documents', extensions)])

        if file_path:
            self.filepaths[file_type] = [file_path]
            self.labels[index].config(text=os.path.basename(file_path), fg='black')


if __name__ == "__main__":
    root = tk.Tk()
    app = InfoExtractorApp(root)
    root.mainloop()