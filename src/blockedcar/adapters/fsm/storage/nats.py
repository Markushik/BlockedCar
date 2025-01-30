from typing import Any, Dict, Literal, Optional

import ormsgpack
import zstd
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DEFAULT_DESTINY,
    KeyBuilder,
    StateType,
    StorageKey,
)
from nats.js import JetStreamContext

from nats.js.errors import BadRequestError, KeyNotFoundError
from nats.js.kv import KeyValue


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
                str(key.business_connection_id)
                if self.with_business_connection_id
                else None,
                key.destiny if self.with_destiny else None,
                part,
            )
            if part is not None
        )


class NatsBucketManager:
    def __init__(
        self,
        jetstream: JetStreamContext,
    ):
        self.jetstream = jetstream

        self._state = None
        self._data = None

    @property
    def state(self) -> KeyValue:
        if self._state is None:
            raise RuntimeError("state is not created")
        return self._state

    @property
    def data(self) -> KeyValue:
        if self._data is None:
            raise RuntimeError("data is not created")
        return self._data

    async def create_buckets(self) -> None:
        try:
            self._state = await self.jetstream.create_key_value(bucket="state")
        except BadRequestError:
            self._state = await self.jetstream.key_value(bucket="state")

        try:
            self._data = await self.jetstream.create_key_value(bucket="data")
        except BadRequestError:
            self._data = await self.jetstream.key_value(bucket="data")


class NatsStorage(BaseStorage):
    def __init__(
        self,
        bucket_manager: NatsBucketManager,
        key_builder: KeyBuilder = None,
    ):
        self.bucket_manager = bucket_manager
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.key_builder = key_builder

    async def get_state(self, key: StorageKey):
        nats_key = self.key_builder.build(key, "state")
        try:
            entry = await self.bucket_manager.state.get(nats_key)
        except KeyNotFoundError:
            value = None
        else:
            value = entry.value
        if value is not None:
            return ormsgpack.unpackb(zstd.decompress(value))
        return value

    async def set_state(self, key: StorageKey, state: StateType = None):
        nats_key = self.key_builder.build(key, "state")

        if state is None:
            await self.bucket_manager.state.delete(nats_key)
        else:
            if isinstance(state, State):
                state = state.state
            await self.bucket_manager.state.put(
                nats_key, zstd.compress(ormsgpack.packb(state))
            )

    async def set_data(self, key: KeyBuilder, data: dict):
        nats_key = self.key_builder.build(key, "data")
        if not data:
            await self.bucket_manager.data.delete(nats_key)
        await self.bucket_manager.data.put(
            nats_key, zstd.compress(ormsgpack.packb(data))
        )

    async def close(): ...

    async def get_data(self, key: StorageKey):
        nats_key = self.key_builder.build(key, "data")

        try:
            entry = await self.bucket_manager.data.get(nats_key)
        except KeyNotFoundError:
            value = None
        else:
            value = entry.value
        if value is None:
            return {}
        return ormsgpack.unpackb(zstd.decompress(value))
