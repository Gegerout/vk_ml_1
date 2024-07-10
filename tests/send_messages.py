from kafka import KafkaProducer
import json


def send_messages():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    messages = [
        {"Url": "http://example.com", "PubDate": 1622470420, "FetchTime": 3, "Text": "Text3"},
        {"Url": "http://example.com", "PubDate": 1622470420, "FetchTime": 1, "Text": "Text1"},
        {"Url": "http://example.com", "PubDate": 1622470420, "FetchTime": 2, "Text": "Text2"}
    ]

    for msg in messages:
        producer.send('input_topic', json.dumps(msg).encode('utf-8'))

    producer.close()


if __name__ == "__main__":
    send_messages()
