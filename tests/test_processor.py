import unittest
from src.TDocument import TDocument
from src.processor import DocumentProcessor


class TestDocumentProcessor(unittest.TestCase):
    def test_processing(self):
        processor = DocumentProcessor()

        # Test input documents
        doc1 = TDocument("http://example.com", 1622470420, 1, "Text1")
        doc2 = TDocument("http://example.com", 1622470420, 2, "Text2")
        doc3 = TDocument("http://example.com", 1622470420, 3, "Text3")

        # Process the documents
        result1 = processor.process(doc1)
        result2 = processor.process(doc2)
        result3 = processor.process(doc3)

        # Check the results
        self.assertEqual(result1.Text, "Text1")
        self.assertEqual(result1.FetchTime, 1)
        self.assertEqual(result1.PubDate, 1622470420)
        self.assertEqual(result1.FirstFetchTime, 1)

        self.assertEqual(result2.Text, "Text2")
        self.assertEqual(result2.FetchTime, 2)
        self.assertEqual(result2.PubDate, 1622470420)
        self.assertEqual(result2.FirstFetchTime, 1)

        self.assertEqual(result3.Text, "Text3")
        self.assertEqual(result3.FetchTime, 3)
        self.assertEqual(result3.PubDate, 1622470420)
        self.assertEqual(result3.FirstFetchTime, 1)

    def test_mixed_order(self):
        processor = DocumentProcessor()

        # Documents received out of order
        doc1 = TDocument("http://example.com", 1622470420, 3, "Text3")
        doc2 = TDocument("http://example.com", 1622470420, 1, "Text1")
        doc3 = TDocument("http://example.com", 1622470420, 2, "Text2")

        result1 = processor.process(doc1)
        result2 = processor.process(doc2)
        result3 = processor.process(doc3)

        self.assertEqual(result1.Text, "Text3")
        self.assertEqual(result1.FetchTime, 3)
        self.assertEqual(result1.PubDate, 1622470420)
        self.assertEqual(result1.FirstFetchTime, 3)

        self.assertEqual(result2.Text, "Text3")
        self.assertEqual(result2.FetchTime, 3)
        self.assertEqual(result2.PubDate, 1622470420)
        self.assertEqual(result2.FirstFetchTime, 1)

        self.assertEqual(result3.Text, "Text3")
        self.assertEqual(result3.FetchTime, 3)
        self.assertEqual(result3.PubDate, 1622470420)
        self.assertEqual(result3.FirstFetchTime, 1)

    def test_duplicates(self):
        processor = DocumentProcessor()

        # Duplicate documents
        doc1 = TDocument("http://example.com", 1622470420, 1, "Text1")
        doc2 = TDocument("http://example.com", 1622470420, 1, "Text1 Duplicate")
        doc3 = TDocument("http://example.com", 1622470420, 2, "Text2")

        result1 = processor.process(doc1)
        result2 = processor.process(doc2)
        result3 = processor.process(doc3)

        self.assertEqual(result1.Text, "Text1")
        self.assertEqual(result1.FetchTime, 1)
        self.assertEqual(result1.PubDate, 1622470420)
        self.assertEqual(result1.FirstFetchTime, 1)

        self.assertEqual(result2.Text, "Text1")
        self.assertEqual(result2.FetchTime, 1)
        self.assertEqual(result2.PubDate, 1622470420)
        self.assertEqual(result2.FirstFetchTime, 1)

        self.assertEqual(result3.Text, "Text2")
        self.assertEqual(result3.FetchTime, 2)
        self.assertEqual(result3.PubDate, 1622470420)
        self.assertEqual(result3.FirstFetchTime, 1)


if __name__ == "__main__":
    unittest.main()
