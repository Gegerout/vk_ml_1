class DocumentProcessor:
    def __init__(self, db):
        self.db = db  # Инициализация с базой данных

    def process(self, doc):
        existing_doc = self.db.get_document(doc.Url)  # Получение существующего документа из базы данных по URL
        if existing_doc:
            updated = False

            # Проверка и обновление текста и времени получения, если FetchTime больше
            if doc.FetchTime > existing_doc.FetchTime:
                existing_doc.Text = doc.Text
                existing_doc.FetchTime = doc.FetchTime
                updated = True

            # Обновление FirstFetchTime, если FetchTime меньше
            if doc.FetchTime < existing_doc.FirstFetchTime:
                existing_doc.FirstFetchTime = doc.FetchTime
                updated = True

            # Обновление PubDate, если FetchTime меньше
            if doc.FetchTime < existing_doc.FetchTime:
                existing_doc.PubDate = doc.PubDate
                updated = True

            # Сохранение обновленного документа в базу данных, если были изменения
            if updated:
                self.db.save_document(existing_doc)
                return existing_doc
            else:
                return None
        else:
            # Если документа нет в базе, установить FirstFetchTime и сохранить новый документ
            doc.FirstFetchTime = doc.FetchTime
            self.db.save_document(doc)
            return doc
