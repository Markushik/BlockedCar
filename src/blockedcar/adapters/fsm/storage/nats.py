from .base import BaseStorage, DefaultKeyBuilder, KeyBuilder


class NatsStorage(BaseStorage):
    def __init__(
        self,
        nc,
        key_builder: KeyBuilder,
        state_ttl,
        data_ttl,
        json_loads,
        json_dumps,
    ):
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.nc = nc
        self.key_builder = key_builder
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl
        self.json_loads = json_loads
        self.json_dumps = json_dumps

        async def set_state(self, key: KeyBuilder, state: StateType = None) -> None: ...
