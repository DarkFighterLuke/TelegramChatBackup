import os

from telethon import TelegramClient
from pathlib import Path

api_id = 123456789453556
api_hash = 'hash'

name = ''
max_media_bytes=524288000

try:
    f = open('sessioninfo', 'x')
except FileExistsError:
    print('sessioninfo file found.')
    f = open('sessioninfo', 'r')
    name = f.readline()

while name == '':
    name = input('Enter your name: ')

with open('sessioninfo', 'w') as f:
    f.write(name)

client = TelegramClient(name, api_id, api_hash)


def write_to_file(filepath: str, message: str):
    try:
        f = open(filepath, 'x')
    except FileExistsError:
        f = open(filepath, 'a')
    f.write(message)


async def backup():
    me = await client.get_me()
    print(me.stringify())

    username = me.username
    print('Welcome', username, '!')

    dialogs = []
    print('Getting a list of all your private chats, please wait...')
    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            print(dialog.name, 'has ID', dialog.id)
            dialogs.append(dialog)
    print('Done.')
    print()
    print('Starting backup of your private chats, please wait...')
    Path('MyTelegramChatBackup').mkdir(parents=True, exist_ok=True)
    for dialog in dialogs:
        if dialog.name != '':
            print('Currently saving', dialog.name, 'chat')
            dir_path = f'MyTelegramChatBackup/{dialog.name}/'
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        else:
            print('Currently saving chat with no name and id:', dialog.id)
            dir_path = f'MyTelegramChatBackup/{dialog.id}/'
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        async for message in client.iter_messages(dialog):
            if message.from_id is None:
                user = await client.get_entity(message.peer_id)
                first_name = user.first_name
            else:
                first_name = 'me'

            if message.media is None:
                print(f'{first_name}: {message.text}')
                write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt', f'{first_name}: {message.text}')

            if message.photo or message.video or message.gif or message.voice or message.file or message.audio:
                if message.video:
                    print(f'Size: {message.video.size}')
                    if message.video.size > max_media_bytes:
                        write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt',
                                      f'{first_name}: ignored file too large; caption: {message.text}')
                if message.gif:
                    print(f'Size: {message.gif.size}')
                    if message.gif.size > max_media_bytes:
                        write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt',
                                      f'{first_name}: ignored file too large; caption: {message.text}')
                if message.voice:
                    print(f'Size: {message.voice.size}')
                    if message.voice.size > max_media_bytes:
                        write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt',
                                      f'{first_name}: ignored file too large; caption: {message.text}')
                if message.file:
                    print(f'Size: {message.file.size}')
                    if message.file.size > max_media_bytes:
                        write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt',
                                      f'{first_name}: ignored file too large; caption: {message.text}')
                if message.audio:
                    print(f'Size: {message.audio.size}')
                    if message.audio.size > max_media_bytes:
                        write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt',
                                      f'{first_name}: ignored file too large; caption: {message.text}')

                path = await message.download_media()
                print(path)
                Path(f'{dir_path}media/').mkdir(parents=True, exist_ok=True)
                os.replace(path, f'{dir_path}media/{path}')
                print(f'{first_name}: {dir_path}media/{path} caption: {message.text}')
                write_to_file(f'{dir_path}{dialog.name}_{dialog.id}.txt', f'{first_name}: {dir_path}media/{path} caption: {message.text}')


with client:
    client.loop.run_until_complete(backup())
