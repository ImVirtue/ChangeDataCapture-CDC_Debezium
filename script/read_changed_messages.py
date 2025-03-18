from confluent_kafka import KafkaError, Consumer
import json

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

consumer.subscribe(['cdc.public.transactions'])

try:
        while True:
            msg = consumer.poll(1.0)
            # print(type(msg))
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
            else:
                data = json.loads(msg.value().decode('utf-8'))
                change_type = data['payload']['op']
                data_before = data['payload']['before']
                data_after = data['payload']['after']
                if change_type == 'u':
                    change_type = 'Update'
                elif change_type == 'c':
                    change_type = 'Create'
                else:
                    change_type = 'Delete'
                print(f"Change Type: {change_type}")
                print(f"Data before changing: {data_before}")
                print(f"Data after changing: {data_after}")

except Exception as e:
    print(e)
