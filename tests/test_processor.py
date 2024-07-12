import unittest
from src.TDocument import TDocument
from src.processor import DocumentProcessor
from unittest.mock import MagicMock


class TestDocumentProcessor(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.processor = DocumentProcessor(self.db_mock)

    def test_process_new_document(self):
        """
            Тест на обработку нового документа.
            Проверяет, что новый документ сохраняется в базу данных с корректным значением FirstFetchTime.
        """
        doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000010,
            Text="First version of the document"
        )

        self.db_mock.get_document.return_value = None
        processed_doc = self.processor.process(doc)

        self.assertIsNotNone(processed_doc)
        self.assertEqual(processed_doc.FirstFetchTime, doc.FetchTime)
        self.db_mock.save_document.assert_called_with(processed_doc)

    def test_process_existing_document_update(self):
        """
            Тест на обновление существующего документа.
            Проверяет, что текст и FetchTime обновляются корректно, если FetchTime нового документа больше.
        """
        initial_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000010,
            Text="First version of the document",
            FirstFetchTime=1620000010
        )

        updated_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000020,
            Text="Updated version of the document"
        )

        self.db_mock.get_document.return_value = initial_doc
        processed_doc = self.processor.process(updated_doc)

        self.assertIsNotNone(processed_doc)
        self.assertEqual(processed_doc.Text, updated_doc.Text)
        self.assertEqual(processed_doc.FetchTime, updated_doc.FetchTime)
        self.assertEqual(processed_doc.FirstFetchTime, initial_doc.FirstFetchTime)
        self.db_mock.save_document.assert_called_with(processed_doc)

    def test_text_and_fetch_time_should_be_from_max_fetch_time(self):
        """
        Тест проверяет, что поля Text и FetchTime должны быть такими,
        какими были у документа с наибольшим FetchTime.
        """
        initial_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000010,
            Text="First version of the document",
            FirstFetchTime=1620000010
        )

        updated_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000020,
            Text="Updated version of the document"
        )

        self.db_mock.get_document.return_value = initial_doc
        processed_doc = self.processor.process(updated_doc)

        self.assertEqual(processed_doc.Text, "Updated version of the document")
        self.assertEqual(processed_doc.FetchTime, 1620000020)

    def test_pub_date_should_be_from_min_fetch_time(self):
        """
        Тест проверяет, что поле PubDate должно быть таким,
        каким оно было у сообщения с наименьшим FetchTime.
        """
        initial_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000005,
            FetchTime=1620000020,
            Text="First version of the document",
            FirstFetchTime=1620000010
        )

        new_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000015,
            Text="Updated version of the document"
        )

        self.db_mock.get_document.return_value = initial_doc
        processed_doc = self.processor.process(new_doc)

        self.assertEqual(processed_doc.PubDate, 1620000000)

    def test_first_fetch_time_should_be_min_fetch_time(self):
        """
        Тест проверяет, что поле FirstFetchTime должно быть равно минимальному значению FetchTime.
        """
        initial_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000020,
            Text="First version of the document",
            FirstFetchTime=1620000010
        )

        new_doc = TDocument(
            Url="https://example.com/doc1",
            PubDate=1620000000,
            FetchTime=1620000005,
            Text="Updated version of the document"
        )

        self.db_mock.get_document.return_value = initial_doc
        processed_doc = self.processor.process(new_doc)

        self.assertEqual(processed_doc.FirstFetchTime, 1620000005)


if __name__ == "__main__":
    unittest.main()
