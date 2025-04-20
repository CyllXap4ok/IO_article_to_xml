from typing import Callable

from data.article import ArticleData
from data.enum_const import FileType
from data.extractor.data_extractor import DataExtractor
from data.extractor.extraction_strategy import ArticleExtractionStrategy, ReviewExtractionStrategy
from data.saver.data_saver import DataSaver
from data.saver.saving_strategy import SavingStrategies


class MainViewModel:

    _article_data = ArticleData()
    _data_extractor = DataExtractor()
    _data_saver = DataSaver()

    _filepaths: dict[FileType, list[str]] = {}
    _progress_elements = len(SavingStrategies)

    def extract_data(self, progress_callback: Callable):
        self._progress_elements += sum(map(len, self._filepaths.values()))

        for file_type, paths in self._filepaths.items():
            """ Устанавливаем стратегию в зависимости от типа файлов """
            match file_type:
                case (FileType.Article):
                    self._data_extractor.set_strategy(ArticleExtractionStrategy())
                case (FileType.Review):
                    self._data_extractor.set_strategy(ReviewExtractionStrategy())

            for path in paths:
                """ Извлекаем информацию и обновляем прогресс """
                self._data_extractor.extract_data(path, self._article_data)
                progress_callback(100 / self._progress_elements)

    def save_data(self, saving_path: str, progress_callback: Callable):

        for strategy in SavingStrategies:
            self._data_saver.set_strategy(strategy.value)
            self._data_saver.save_data(saving_path, self._article_data)
            progress_callback(100 / self._progress_elements)

        self._progress_elements = len(SavingStrategies)
        self._article_data.clear()

    def set_file_paths(self, file_type: FileType, paths: list[str]):
        self._filepaths[file_type] = paths

    def clear_file_paths(self):
        self._filepaths.clear()