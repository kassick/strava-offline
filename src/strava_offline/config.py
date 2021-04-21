from dataclasses import dataclass
from functools import reduce
from functools import wraps
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Type
from typing import TypeVar

import appdirs  # type: ignore [import]
import click
from click_option_group import OptionGroup  # type: ignore [import]

data_dir = Path(appdirs.user_data_dir(appname=__package__))
config_dir = Path(appdirs.user_config_dir(appname=__package__))

ConfigT = TypeVar('ConfigT', bound='BaseConfig')


class PathType(click.Path):
    def convert(self, value, param, ctx):
        rv = super().convert(value, param, ctx)
        return Path(rv) if rv is not None else None


def compose_decorators(*decorators):
    return lambda f: reduce(lambda x, g: g(x), reversed(decorators), f)


def wrap_kwargs_into_config(config_class: Type[ConfigT]):
    def decorator(f: Callable[[ConfigT], None]) -> Callable[..., None]:
        @wraps(f)
        def wrapper(**kwargs):
            return f(config_class(**kwargs))
        return wrapper
    return decorator


@dataclass
class BaseConfig:
    @classmethod
    def options(cls):
        assert not hasattr(super(), 'options')
        return wrap_kwargs_into_config(cls)


@dataclass
class StravaApiConfig(BaseConfig):
    strava_client_id: str = '54316'
    strava_client_secret: str = '3cfc2260d03472baca90d49fc4bc1d9714711771'
    strava_token_filename: Path = config_dir / 'token.json'
    http_host: str = '127.0.0.1'
    http_port: int = 12345

    @classmethod
    def options(cls):
        group = OptionGroup("Strava API")
        return compose_decorators(
            group.option(
                '--client-id', 'strava_client_id', type=str,
                envvar='STRAVA_CLIENT_ID', show_envvar=True,
                default=cls.strava_client_id,
                help="Strava OAuth 2 client id"),
            group.option(
                '--client-secret', 'strava_client_secret', type=str,
                envvar='STRAVA_CLIENT_SECRET', show_envvar=True,
                default=cls.strava_client_secret,
                help="Strava OAuth 2 client secret"),
            group.option(
                '--token-file', 'strava_token_filename', type=PathType(dir_okay=False),
                default=cls.strava_token_filename, show_default=True,
                help="Strava OAuth 2 token store"),
            group.option(
                '--http-host', type=str,
                default=cls.http_host, show_default=True,
                help="OAuth 2 HTTP server host"),
            group.option(
                '--http-port', type=int,
                default=cls.http_port, show_default=True,
                help="OAuth 2 HTTP server port"),
            super().options()
        )


@dataclass
class StravaWebConfig(BaseConfig):
    strava_cookie_strava4_session: str = ""

    @classmethod
    def options(cls):
        group = OptionGroup("Strava web")
        return compose_decorators(
            group.option(
                '--strava4-session', 'strava_cookie_strava4_session', type=str,
                envvar='STRAVA_COOKIE_STRAVA4_SESSION', show_envvar=True,
                required=True,
                help="'_strava4_session' cookie value"),
            super().options()
        )


@dataclass
class DatabaseConfig(BaseConfig):
    strava_sqlite_database: Path = data_dir / 'strava.sqlite'

    @classmethod
    def options(cls):
        group = OptionGroup("Database")
        return compose_decorators(
            group.option(
                '--database', 'strava_sqlite_database', type=PathType(dir_okay=False),
                default=cls.strava_sqlite_database, show_default=True,
                help="Sqlite database file"),
            super().options()
        )


@dataclass
class SyncConfig(DatabaseConfig):
    full: bool = False

    @classmethod
    def options(cls):
        group = OptionGroup("Sync options")
        return compose_decorators(
            group.option(
                '--full / --no-full', default=cls.full, show_default=True,
                help="Perform full sync instead of incremental"),
            super().options()
        )


@dataclass
class GpxConfig(DatabaseConfig):
    dir_activities: Path = Path("strava_data", "activities")
    dir_activities_backup: Optional[Path] = None

    @classmethod
    def options(cls):
        group = OptionGroup("GPX storage")
        return compose_decorators(
            group.option(
                '--dir-activities', type=PathType(file_okay=False),
                default=cls.dir_activities, show_default=True,
                help="Directory to store gpx files indexed by activity id"),
            group.option(
                '--dir-activities-backup', type=PathType(file_okay=False),
                help="Optional path to activities in Strava backup (no need to redownload these)"),
            super().options()
        )
