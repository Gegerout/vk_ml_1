from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from src.TDocument import TDocument

Base = declarative_base()


# Определение модели базы данных для хранения документов
class DocumentModel(Base):
    __tablename__ = 'documents'
    Url = Column(String, primary_key=True)
    PubDate = Column(Integer)
    FetchTime = Column(Integer)
    Text = Column(String)
    FirstFetchTime = Column(Integer)


class Database:
    def __init__(self, db_path='data/documents.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # Сохранение документа в базу данных
    def save_document(self, doc):
        session = self.Session()
        existing_doc = session.query(DocumentModel).filter_by(Url=doc.Url).first()
        if existing_doc:
            # Обновление полей существующего документа
            existing_doc.PubDate = doc.PubDate
            existing_doc.FetchTime = doc.FetchTime
            existing_doc.Text = doc.Text
            existing_doc.FirstFetchTime = doc.FirstFetchTime
        else:
            # Создание нового документа
            new_doc = DocumentModel(
                Url=doc.Url,
                PubDate=doc.PubDate,
                FetchTime=doc.FetchTime,
                Text=doc.Text,
                FirstFetchTime=doc.FirstFetchTime
            )
            session.add(new_doc)
        session.commit()
        session.close()

    # Получение документа из базы данных по URL
    def get_document(self, url):
        session = self.Session()
        doc = session.query(DocumentModel).filter_by(Url=url).first()
        session.close()
        if doc:
            # Преобразование модели базы данных в объект TDocument
            return TDocument(
                Url=doc.Url,
                PubDate=doc.PubDate,
                FetchTime=doc.FetchTime,
                Text=doc.Text,
                FirstFetchTime=doc.FirstFetchTime
            )
        return None

    def close(self):
        pass
