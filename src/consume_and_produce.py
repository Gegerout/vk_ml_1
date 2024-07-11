from kafka import KafkaConsumer, KafkaProducer
from src.TDocument import TDocument
from src.processor import DocumentProcessor
from src.database import Database
import os


def consume_and_process():
    # Инициализация Kafka consumer для чтения из топика 'input_topic'
    consumer = KafkaConsumer(
        'input_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my_group'
    )

    # Инициализация Kafka producer для записи в топик 'output_topic'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Путь к базе данных
    db_path = os.path.join('..', 'data', 'documents.db')
    db = Database(db_path)
    processor = DocumentProcessor(db)

    # Основной цикл чтения сообщений из Kafka
    for message in consumer:
        message_value = message.value.decode('utf-8')
        doc = TDocument.from_json(message_value)
        if doc is None:
            continue

        # Обработка документа
        processed_doc = processor.process(doc)

        # Если обработка вернула документ, отправить его в топик 'output_topic'
        if processed_doc:
            producer.send('output_topic', processed_doc.to_json().encode('utf-8'))

    consumer.close()
    producer.close()
    db.close()


if __name__ == "__main__":
    consume_and_process()
