from kafka import KafkaConsumer, KafkaProducer
from TDocument import TDocument
from processor import DocumentProcessor
from database import Database
import os


def consume_and_process():
    consumer = KafkaConsumer(
        'input_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my_group'
    )

    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Указываем путь к базе данных в папке data
    db_path = os.path.join('..', 'data', 'documents.db')
    db = Database(db_path)
    processor = DocumentProcessor(db)

    for message in consumer:
        message_value = message.value.decode('utf-8')
        doc = TDocument.from_json(message_value)
        if doc is None:
            continue  # Пропускаем неверные сообщения

        processed_doc = processor.process(doc)
        if processed_doc:
            producer.send('output_topic', processed_doc.to_json().encode('utf-8'))

    consumer.close()
    producer.close()
    db.close()


if __name__ == "__main__":
    consume_and_process()
