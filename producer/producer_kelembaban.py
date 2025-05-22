from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

gudang_ids = ['G1', 'G2', 'G3']

while True:
    data = {
        "gudang_id": random.choice(gudang_ids),
        "kelembaban": random.randint(65, 80)
    }
    producer.send('sensor-kelembaban-gudang', value=data)
    print(f"Kirim: {data}")
    time.sleep(1)
