import asyncio
import logging
import os

import click
import tomlkit

main_loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.WARNING)


class Config:
    mongodb_uri: str

    def __init__(self):
        pass

    def read_config(self, filename):

        from pathlib import Path
        config_path = Path(filename)
        if not config_path.exists():
            return

        with open(filename) as f:
            config = tomlkit.load(f)

        self.mongodb_uri = config["database"]["mongodb"]["uri"]


pass_config = click.make_pass_decorator(Config, ensure=True)


def read_config(ctx, param, value):

    cfg = ctx.ensure_object(Config)
    if value is None:
        value = os.path.join(click.get_app_dir("loci", force_posix = True), "config_template.toml")
    cfg.read_config(value)
    return value


@click.group()
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    callback=read_config,
    expose_value=False,
    help="The config file to use instead of the default.",
)
@click.option("silent", "--silent", "-s", default=False, is_flag=True, help="Disables output.")
@click.option("verbose", "--verbose", "-v", default=False, is_flag=True, help="Enables verbose mode.")
@pass_config
def cli(config, silent, verbose):
    """An example application that supports aliases."""
    pass


@cli.command("list")
def find_all():
    """List all memories."""
    #main_loop.run_until_complete()
    pass


@cli.command("sync")
@click.option("--inc/--no-inc", default=True, help="Incremental sync.")
def sync(inc: bool):
    pass
