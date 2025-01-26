from functools import cache

from adaptix import Retort
from dynaconf import Dynaconf

from .schemas import Config


@cache
def load_settings() -> Config:
    dynaconf: Dynaconf = Dynaconf(
        settings_file=["settings/.secrets.toml", "settings/settings.toml"],
        core_loaders=["TOML"],
        environments=True,
    )
    retort: Retort = Retort()

    return retort.load(dynaconf, Config)
