from kafka import KafkaConsumer


def read_output():
    consumer = KafkaConsumer(
        'output_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='output_reader'
    )

    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")


if __name__ == "__main__":
    read_output()
