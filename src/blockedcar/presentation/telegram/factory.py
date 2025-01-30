from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from dishka import AsyncContainer, provide, Provider, Scope
from dishka.integrations.aiogram import setup_dishka

from nats.js import JetStreamContext

from blockedcar.adapters.fsm.storage.nats import (
    DefaultKeyBuilder,
    NatsBucketManager,
    NatsStorage,
)

from blockedcar.main.configuration.schemas import BotConfig
from blockedcar.presentation.telegram.dialogs import get_dialogs
from blockedcar.presentation.telegram.handlers import get_handlers


class BotProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_bot(self, config: BotConfig) -> AsyncIterable[Bot]:
        async with Bot(token=config.token) as bot:
            yield bot


class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_storage(self, jetstream: JetStreamContext) -> BaseStorage:
        bucket_manager = NatsBucketManager(jetstream)
        await bucket_manager.create_buckets()
        return NatsStorage(
            bucket_manager, key_builder=DefaultKeyBuilder(with_destiny=True)
        )

    @provide
    def create_dispatcher(
        self, container: AsyncContainer, storage: BaseStorage
    ) -> Dispatcher:
        dispatcher = Dispatcher(storage=storage)

        dispatcher.include_routers(*get_handlers(), *get_dialogs())

        setup_dishka(container=container, router=dispatcher)
        setup_dialogs(dispatcher)

        return dispatcher
