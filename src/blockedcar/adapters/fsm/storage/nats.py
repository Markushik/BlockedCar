from typing import Any, Dict, Optional

import ormsgpack
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, KeyBuilder, StateType, StorageKey
from nats.js import JetStreamContext
from nats.js.errors import BadRequestError
from nats.js.kv import KeyValue

from .base import DefaultKeyBuilder


class NatsBucketManager:
    def __init__(
        self,
        jetstream,
    ):
        self.jetstream = jetstream

        self._data_key_value: Optional[KeyValue] = None
        self._state_key_lock: Optional[KeyValue] = None
        self._lock_key_value: Optional[KeyValue] = None

    @property
    def data_key_value(self) -> KeyValue:
        if self._data_key_value is None:
            raise RuntimeError("'data_kv' is not created")
        return self._data_key_value

    @property
    def lock_key_value(self) -> KeyValue:
        if self._lock_key_value is None:
            raise RuntimeError("'lock_kv' is not created")
        return self._lock_key_value

    @property
    def state_key_value(self) -> KeyValue:
        if self._state_key_value is None:
            raise RuntimeError("'state_kv' is not created")
        return self._state_key_value

    async def create_key_value(self):
        try:
            self._data_key_value = await self.jetstream.create_key_value(bucket="data")
        except BadRequestError:
            self._data_key_value = self.jetstream.key_value(bucket="data")

        try:
            self._state_key_value = await self.jetstream.create_key_value(
                bucket="state"
            )
        except BadRequestError:
            self._state_key_value = self.jetstream.key_value(bucket="state")

        try:
            self._lock_key_value = await self.jetstream.create_key_value(bucket="lock")
        except BadRequestError:
            self._lock_key_value = self.jetstream.key_value(bucket="lock")

    async def create_object_store(): ...


class NatsStorage(BaseStorage):
    def __init__(
        self,
        jetstream: JetStreamContext,
        bucket_manager: NatsBucketManager,
        key_builder: KeyBuilder = None,
    ) -> None:
        if key_builder is None:
            key_builder = DefaultKeyBuilder()

        self.jetstream = jetstream
        self.key_builder = key_builder
        self.bucket_manager = bucket_manager

        async def set_state(self, key: StorageKey, state: StateType = None) -> None:
            nats_key = self.key_builder.build(key, "state")

            if state is None:
                await self.bucket_manager.state_key_value.delete(nats_key)
            else:
                if isinstance(state, State):
                    state = state.state
                await self.adapter.state_kv.put(nats_key, ormsgpack.packb(state))

        async def get_state(self, key: StorageKey) -> Optional[str]:
            pass

        async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
            pass

        async def get_data(self, key: StorageKey) -> Dict[str, Any]: ...

        async def close(self) -> None: ...
