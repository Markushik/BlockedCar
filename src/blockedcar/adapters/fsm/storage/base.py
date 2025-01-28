from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, Literal, Optional, Protocol, Union

from aiogram.fsm.state import State

StateType = Optional[Union[str, State]]

DEFAULT_DESTINY = "default"


@dataclass(frozen=True)
class StorageKey:
    bot_id: int
    chat_id: int
    user_id: int
    thread_id: Optional[int] = None
    businnes_connection_id: Optional[str] = None
    destiny: str = DEFAULT_DESTINY


class KeyBuilder(Protocol):
    def build(
        self,
        key: StorageKey,
        part: Optional[Literal["data", "state", "lock"]] = None,
    ) -> str:
        pass


class DefaultKeyBuilder(KeyBuilder):
    def __init__(
        self,
        *,
        prefix: str = "fsm",
        separator: str = "_",
        with_bot_id: bool = False,
        with_business_connection_id: bool = False,
        with_destiny: bool = False,
    ) -> None:
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_business_connection_id = with_business_connection_id
        self.with_destiny = with_destiny

        def build(
            self,
            key: StorageKey,
            part: Optional[Literal["data", "state", "lock"]] = None,
        ) -> str:
            return self.separator.join(
                str(part)
                for part in (
                    self.prefix,
                    str(key.bot_id) if self.with_bot_id else None,
                    str(key.chat_id),
                    str(key.user_id),
                    str(key.thread_id) if key.thread_id else None,
                    str(key.businnes_connection_id)
                    if self.with_businnes_connection_id
                    else None,
                    key.destiny if self.with_destiny else None,
                    part,
                )
                if part is not None
            )


class BaseStorage(Protocol):
    async def set_state(self, key: KeyBuilder, state: StateType = None) -> None: ...

    async def get_state(self, key: KeyBuilder) -> Optional[str]: ...

    async def set_data(self, key: KeyBuilder, data: Dict[str, Any]) -> None: ...

    async def get_data(self, key: KeyBuilder) -> None: ...

    async def close(self) -> None: ...


class BaseEventIsolation(Protocol):
    async def lock(self, key: KeyBuilder) -> AsyncGenerator[None, None]:
        yield None

    async def close(self) -> None: ...
