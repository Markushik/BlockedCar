from typing import AsyncIterable

import nats
from dishka import provide, Provider, Scope
from nats.aio.client import Client
from nats.js import JetStreamContext

from blockedcar.adapters.fsm.storage.nats import NatsBucketManager
from blockedcar.main.configuration.schemas import NatsConfig


class NatsProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_nats(self, config: NatsConfig) -> AsyncIterable[Client]:
        client = await nats.connect()
        yield client
        await client.drain()

    @provide(scope=Scope.APP)
    async def create_jetstream(self, client: Client) -> JetStreamContext:
        jetstream = client.jetstream()
        return jetstream

    @provide(scope=Scope.APP)
    async def create_bucket_manager(
        self, jetstream: JetStreamContext
    ) -> NatsBucketManager:
        return NatsBucketManager(jetstream=jetstream)
