class DocumentProcessor:
    def __init__(self, db):
        self.db = db

    def process(self, doc):
        existing_doc = self.db.get_document(doc.Url)
        if existing_doc:
            if doc.FetchTime > existing_doc.FetchTime:
                existing_doc.Text = doc.Text
                existing_doc.FetchTime = doc.FetchTime
            if doc.FetchTime < existing_doc.FirstFetchTime:
                existing_doc.FirstFetchTime = doc.FetchTime
            if doc.FetchTime < existing_doc.FetchTime:
                existing_doc.PubDate = doc.PubDate

            self.db.save_document(existing_doc)
            return existing_doc
        else:
            doc.FirstFetchTime = doc.FetchTime
            self.db.save_document(doc)
            return doc
