#!/usr/bin/env python
import sys

import click as click
from instagrapi import Client


@click.group(name="Instagram Swiss knife")
@click.version_option(version='0.1.0')
def commands():
    """Instagram Swiss knife - Manage your posted media, stories, etc. You will be able to back
    up of your media or to delete the oldest ones."""


@commands.command(name="delete")
@click.option("--size", '-s', help='The amount of oldest photos to be removed')
@click.option('--username', '-u', envvar='IG_USER', prompt="Username",
              help='Your IG username. Default value is taken from IG_USER env var.')
@click.password_option('--password', '-p', envvar='IG_PASSWORD', confirmation_prompt=False,
                       help='Your IG password. Default value is taken from IG_PASSWORD env '
                            'var.')
def delete_command(username, password, size):
    """Delete your oldest posted media, stories, etc."""

    if not username:
        print("Username is mandatory.")
        sys.exit(1)

    if not password:
        print("Password is mandatory.")
        sys.exit(1)

    if not size:
        print("Size (with the amount of media to be removed) is mandatory.")
        sys.exit(1)

    cl = Client()
    cl.login(username, password)

    user_id = cl.user_id_from_username(username)
    medias = cl.user_medias(int(user_id), 0)
    medias.reverse()

    i = 1
    for media in medias[:int(size)]:
        print(f"Trying to delete [{i}]: {media}")
        cl.media_delete(media.pk)
        i += 1


@commands.command(name="backup")
def backup_command(username, password, size):
    """Backup your media"""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    commands()

    sys.exit(0)
