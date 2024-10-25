# user_service - kahfa_consumer.py

# from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
# import asyncio
# import json

from aiokafka import AIOKafkaConsumer
### ============================================================================================================= ###

async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()

    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Consumer Received message: {message.value.decode()} on topic {message.topic}")
            
    finally:
        # Ensure that the consumer is properly closed when done.
        await consumer.stop() 
        
### ============================================================================================================= ###
