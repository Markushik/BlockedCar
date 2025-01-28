from dishka import AsyncContainer, make_async_container

from blockedcar.adapters.broker.factory import NatsProvider

from blockedcar.main.configuration.factory import ConfigProvider

from blockedcar.main.configuration.loader import load_settings
from blockedcar.presentation.telegram.factory import BotProvider, DispatcherProvider


def setup_dishka() -> AsyncContainer:
    container = make_async_container(
        ConfigProvider(load_settings()),
        NatsProvider(),
        BotProvider(),
        DispatcherProvider(),
    )
    return container
