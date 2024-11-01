import logging

from aiokafka import AIOKafkaProducer
import asyncio

from src.config import Settings

event_loop = asyncio.get_event_loop()


class AIOWebProducer:
    def __init__(self):
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=Settings.KAFKA_BOOTSTRAP_SERVERS,
            loop=event_loop,
        )
        self.__produce_topic = Settings.PICTURE_TOPIC

    async def start(self) -> None:
        await self.__producer.start()

    async def stop(self) -> None:
        await self.__producer.stop()

    async def send(self, value: bytes) -> None:
        await self.start()
        try:
            await self.__producer.send(
                topic=self.__produce_topic,
                value=value,
            )
        finally:
            await self.stop()


def get_producer() -> AIOWebProducer:
    return AIOWebProducer()
