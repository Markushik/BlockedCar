from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from dishka import AsyncContainer, provide, Provider, Scope
from dishka.integrations.aiogram import setup_dishka

from blockedcar.main.configuration.schemas import BotConfig, NatsConfig
from blockedcar.presentation.telegram.dialogs.main_menu.dialog import main_menu
from blockedcar.presentation.telegram.handlers.user import setup

class BotProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_bot(self, config: BotConfig) -> AsyncIterable[Bot]:
        async with Bot(token=config.token) as bot:
            yield bot


class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    def create_dispatcher(
        self, container: AsyncContainer, storage: BaseStorage
    ) -> Dispatcher:
        dispatcher = Dispatcher(storage=storage)

        dispatcher.include_routers(main_menu())
        dispatcher.include_routers(setup())

        setup_dishka(container=container, router=dispatcher)
        setup_dialogs(dispatcher)

        return dispatcher

    @provide
    def create_storage(self, config: NatsConfig) -> BaseStorage:
        return MemoryStorage()
