from kafka import KafkaProducer
import json


def send_messages():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    messages = [
        {"Url": "https://example.com", "PubDate": 1622470423, "FetchTime": 3, "Text": "Text3"},
        {"Url": "https://example.com", "PubDate": 1622470421, "FetchTime": 1, "Text": "Text1"},
        {"Url": "https://example.com", "PubDate": 1622470422, "FetchTime": 2, "Text": "Text2"}
    ]

    for msg in messages:
        producer.send('input_topic', json.dumps(msg).encode('utf-8'))

    producer.close()


if __name__ == "__main__":
    send_messages()
