from data.article import ArticleData
from data.saver.saving_strategy import DataSavingStrategy


class DataSaver:

    _saving_strategy: DataSavingStrategy

    def set_strategy(self, saving_strategy: DataSavingStrategy):
        self._saving_strategy = saving_strategy

    def save_data(self, saving_path: str, data: ArticleData):
        self._saving_strategy.save_data(saving_path, data)
