from dataclasses import dataclass

import typer
from loguru import logger
from qbittorrentapi import Client

from commands import errors


@dataclass
class Common:
    client: any
    log_level: str

app = typer.Typer()
app.add_typer(errors.app, name="errors")

@app.callback()
def common(ctx: typer.Context,
        username: str = typer.Option(default="", envvar='QB_USERNAME', help='Username'),
        password: str = typer.Option(default="", envvar='QB_PASSWORD', help='Password'),
        host: str = typer.Option(..., envvar='QB_HOST', help='Host'),
        log_level: str = typer.Option(default='INFO', envvar='LOG_LEVEL', help='Log Level')):
    """Hai"""
    client = Client(host=host, username=username, password=password)
    ctx.obj = Common(client, log_level)

if __name__ == "__main__":
    app()
