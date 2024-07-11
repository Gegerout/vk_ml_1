class DocumentProcessor:
    def __init__(self, db):
        self.db = db

    def process(self, doc):
        existing_doc = self.db.get_document(doc.Url)
        if existing_doc:
            updated = False
            if doc.FetchTime > existing_doc.FetchTime:
                existing_doc.Text = doc.Text
                existing_doc.FetchTime = doc.FetchTime
                updated = True
            if doc.FetchTime < existing_doc.FirstFetchTime:
                existing_doc.FirstFetchTime = doc.FetchTime
                updated = True
            if doc.FetchTime < existing_doc.FetchTime:
                existing_doc.PubDate = doc.PubDate
                updated = True

            if updated:
                self.db.save_document(existing_doc)
                return existing_doc
            else:
                return None
        else:
            doc.FirstFetchTime = doc.FetchTime
            self.db.save_document(doc)
            return doc
