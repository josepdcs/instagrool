#!/usr/bin/env python
"""Instagram Tool"""
import datetime
import sys

import click

from instagrapi import Client


@click.group(name="Instagram Tool")
@click.version_option(version='0.1.0')
def commands():
    """Instagrool - Manage your posted media, stories, etc. You will be able to back
    up of your media or to delete the oldest ones."""


@commands.command(name="delete")
@click.option("--size", '-s', help='The amount of oldest media to be removed')
@click.option("--date", '-d', help='The date before from which you want to remove media (format: '
                                   'YYYY-MM-dd). Ex. 2022-09-23')
@click.option('--username', '-u', envvar='IG_USER', prompt="Username",
              help='Your IG username. Default value is taken from IG_USER env var.')
@click.password_option('--password', '-p', envvar='IG_PASSWORD', confirmation_prompt=False,
                       help='Your IG password. Default value is taken from IG_PASSWORD env '
                            'var.')
def delete_command(username, password, size, date):
    """
    Delete your oldest posted media, stories, etc.

    Examples:\n
        - Delete your last 100 posted media:\n
            python instagrool.py delete -u user -p password -s 100\n
        - Delete posted media before 2022-01-01\n
            python instagrool.py delete -u user -p password -d 2022-01-01\n
    """

    if not size and not date:
        print("Size (with the amount of oldest photos to be backup) or date (with the date before "
              "which you want to do the backup) is missing. One of them has to be provided.")
        sys.exit(1)

    date_before = ''
    if date:
        date_before = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_before = date_before.astimezone(tz=datetime.timezone.utc)

    client, user_id = do_login(username, password)
    print(f'Retrieved user id: {user_id}')

    medias = client.user_medias_v1(user_id, 0)

    if len(medias) == 0:
        print('No media found.')

    i = 1
    if date_before:
        for media in filter(lambda m: m.taken_at < date_before, medias):
            print(f"Trying to back up [{i}]: {media}")
            client.media_delete(media.pk)
            i += 1
    else:
        for media in medias[-int(size):]:
            print(f"Trying to back up [{i}]: {media}")
            client.media_delete(media.pk)
            i += 1


@commands.command(name="backup")
@click.option("--size", '-s', help='The amount of oldest photos to be backup')
@click.option("--date", '-d', help='The date before from which you want to do the backup (format: '
                                   'YYYY-MM-dd). Ex. 2022-09-23')
@click.option('--username', '-u', envvar='IG_USER', prompt="Username",
              help='Your IG username. Default value is taken from IG_USER env var.')
@click.password_option('--password', '-p', envvar='IG_PASSWORD', confirmation_prompt=False,
                       help='Your IG password. Default value is taken from IG_PASSWORD env '
                            'var.')
@click.option("--output", '-o', help='The path where photos are saved')
def backup_command(username, password, size, date, output):
    """
    Backup your oldest photos

    Examples:\n
        - Backup your last 100 photos:\n
            python instagrool.py backup -u user -p password -s 100\n
        - Backup photos before 2022-01-01\n
            python instagrool.py backup -u user -p password -d 2022-01-01\n
    """

    if not size and not date:
        print("Size (with the amount of oldest photos to be backup) or date (with the date before "
              "which you want to do the backup) is missing. One of them has to be provided.")
        sys.exit(1)

    if not output:
        print("Output path is mandatory.")
        sys.exit(1)

    date_before = ''
    if date:
        date_before = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_before = date_before.astimezone(tz=datetime.timezone.utc)

    client, user_id = do_login(username, password)
    print(f'Retrieved user id: {user_id}')

    medias = client.user_medias_v1(user_id, 0)

    if len(medias) == 0:
        print('No media found.')

    i = 1
    if date_before:
        for media in filter(lambda m: m.taken_at < date_before, medias):
            print(f"Trying to back up [{i}]: {media}")
            client.photo_download(int(media.pk), output)
            i += 1
    else:
        for media in medias[-int(size):]:
            print(f"Trying to back up [{i}]: {media}")
            client.photo_download(int(media.pk), output)
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


if __name__ == '__main__':
    commands()

    sys.exit(0)
