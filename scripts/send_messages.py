from kafka import KafkaProducer
import json


def send_messages():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    messages = [
        {"Url": "https://example3.com", "PubDate": 1622470423, "FetchTime": 1, "Text": "Text3"},
    ]

    for msg in messages:
        producer.send('input_topic', json.dumps(msg).encode('utf-8'))

    producer.close()


if __name__ == "__main__":
    send_messages()
