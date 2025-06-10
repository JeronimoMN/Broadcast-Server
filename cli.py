import asyncio
import click
import threading
from src.Models.server import main as server_main

@click.group()
def cli():
    pass

@cli.command(name='broadcast-server')
@click.option("--start", is_flag=True, help="Start a new session")
@click.option("--stop", is_flag=True, help="Stop a new session")
def broadcast_server(start, stop):
    if start:
        asyncio.run(server_main())
        print('Starting new session...')

    if stop:
        click.echo('Stopping new session...')

if __name__ == '__main__':
    cli()