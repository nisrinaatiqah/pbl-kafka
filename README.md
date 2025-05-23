# Problem Based Learning : Apache Kafka

Nisrina Atiqah Dwiputri Ridzki
(5027231075)

### Persiapan 
  >docker-compose.yml
  ```
  version: '3.9'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  producer:
    image: python:3.11
    container_name: producer
    volumes:
      - ./producer:/app
    working_dir: /app
    command: python producer_suhu.py && python producer_kelembaban.py
    depends_on:
      - kafka

  spark:
    image: bitnami/spark:3.5.0
    container_name: spark
    ports:
      - "4040:4040"
    volumes:
      - ./spark:/app
    working_dir: /app
    command: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 spark_streaming.py
    depends_on:
      - kafka
  ```

  >producer/producer_suhu.py
  ```
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
        "suhu": random.randint(75, 90)
    }
    producer.send('sensor-suhu-gudang', value=data)
    print(f"Kirim: {data}")
    time.sleep(1)
  ```

  >producer/producer_kelembaban.py
  ```
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
  ```
  Setelah itu
  - Nyalakan docker dekstop
  - Setup Zookeeper, Kafka, Producer, Spark
    ```
    docker-compose up -d
    ```

1. Buat Topik Kafka
   - Masuk ke container kafka
     ```
     docker exec -it kafka bash
     ```
   - Buat topik
     ```
     kafka-topics --create --topic sensor-suhu-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
      kafka-topics --create --topic sensor-kelembaban-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```
     ![WhatsApp Image 2025-05-22 at 12 44 23_623dd305](https://github.com/user-attachments/assets/2a728f64-7fe0-471a-b328-073ba92a29b4)

2. Simulasikan Data Sensor (Producer Kafka)
   - Masuk ke containar producer
     ```
     docker exec -it producer bash
     ```
   - Instalasi python
     ```
     pip install kafka-python
     ```
   - Producer Suhu
     ```
     python producer_suhu.py
     ```
     ![image](https://github.com/user-attachments/assets/dd5d211d-ff94-4494-afde-1dce7acbb997)

   - Producer Kelembaban
     ```
     python producer_kelembaban.py
     ```
     ![image](https://github.com/user-attachments/assets/b1734d70-4fd2-45df-9acd-28691a700fbd)

3. Konsumsi dan Olah Data dengan PySpark
   - Masuk ke container spark
      ```
     docker exec -it spark bash
     ```
   - Instalasi python
     ```
     pip install kafka-python
     ```
   - Spark submit
     ```
     spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 spark_streaming.py
     ```
     ![image](https://github.com/user-attachments/assets/73e7a263-e82e-4d6d-9aec-eb6f20c02335)

