from data.article import ArticleData
from data.extractor.extraction_strategy import DataExtractionStrategy


class DataExtractor:

    data_extraction_strategy: DataExtractionStrategy

    def set_strategy(self, data_extraction_strategy: DataExtractionStrategy):
        self.data_extraction_strategy = data_extraction_strategy

    def extract_data(self, path: str, data_holder: ArticleData):
        self.data_extraction_strategy.extract_data(path, data_holder)