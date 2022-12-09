#!/usr/bin/env python
"""Instagram Tool"""

import sys

import click
from instagrapi import Client


@click.group(name="Instagram Tool")
@click.version_option(version='0.1.0')
def commands():
    """Instagrool - Manage your posted media, stories, etc. You will be able to back
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

    if not size:
        print("Size (with the amount of media to be removed) is mandatory.")
        sys.exit(1)

    client, user_id = do_login(username, password)
    print(f'Retrieved user id: {user_id}')

    medias = client.user_medias_v1(user_id, 0)

    if len(medias) == 0:
        print('No media found.')

    i = 1
    for media in medias[-int(size):]:
        print(f"Trying to delete [{i}]: {media}")
        client.media_delete(media.pk)
        i += 1


@commands.command(name="backup")
@click.option("--size", '-s', help='The amount of oldest photos to be removed')
@click.option('--username', '-u', envvar='IG_USER', prompt="Username",
              help='Your IG username. Default value is taken from IG_USER env var.')
@click.password_option('--password', '-p', envvar='IG_PASSWORD', confirmation_prompt=False,
                       help='Your IG password. Default value is taken from IG_PASSWORD env '
                            'var.')
def backup_command(username, password, size):
    """Backup your media"""

    if not size:
        print("Size (with the amount of media to be back up) is mandatory.")
        sys.exit(1)

    client, user_id = do_login(username, password)
    print(f'Retrieved user id: {user_id}')

    medias = client.user_medias_v1(user_id, 0)

    if len(medias) == 0:
        print('No media found.')

    i = 1
    for media in medias[-int(size):]:
        print(f"Trying to back up [{i}]: {media}")
        i += 1


def do_login(username, password) -> (Client, int):
    """ Do log in and return the user id"""

    if not username:
        print("Username is mandatory.")
        sys.exit(1)

    if not password:
        print("Password is mandatory.")
        sys.exit(1)

    client = Client()
    client.login(username, password)

    return client, int(client.user_id_from_username(username))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    commands()

    sys.exit(0)
