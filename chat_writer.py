import argparse
import asyncio
import json
import logging
import os

import aiofiles


async def authorize_user(reader, writer, account_hash):
    reply = await reader.readline()
    logging.debug(reply)
    reply = await submit_message(reader, writer, account_hash)
    if not json.loads(reply):
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')


async def register_user(reader, writer, nickname, data_file_name):
    reply = await reader.readline()
    logging.debug(reply)

    await submit_message(reader, writer, ' ')

    user_details = await submit_message(reader, writer, nickname)
    async with aiofiles.open(data_file_name, mode='w') as f:
        await f.write(user_details.decode())


async def submit_message(reader, writer, message):
    writer.write(add_line(message).encode())
    await writer.drain()
    reply = await reader.readline()
    logging.debug(reply)
    return reply


def clean_text(text):
    if isinstance(text, str):
        return text.replace('\\', '')
    return text


def add_line(text):
    return f'{text}\n'


async def run_chat(host, port, message, nickname):
    reader, writer = await asyncio.open_connection(host, port)
    user_details_filename = 'user_details.json'

    try:
        if nickname:
            await register_user(reader, writer, nickname, user_details_filename)
        elif os.path.exists(user_details_filename):
            async with aiofiles.open(user_details_filename, 'r') as f:
                user_details = await f.read()
                account_hash = json.loads(user_details)['account_hash']
                await authorize_user(reader, writer, account_hash)
        else:
            print('Придумайте ник для регистрации в чате: --nickname / -n')
            return

        await submit_message(reader, writer, add_line(message))

    finally:
        writer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='minechat.dvmn.org')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('--message', '-m', required=True)
    parser.add_argument('--nickname', '-n')
    args = parser.parse_args()

    host = args.host or os.getenv('WRITER_HOST')
    port = args.port or os.getenv('WRITER_PORT')
    msg = clean_text(args.message)
    nickname = args.nickname or 0

    asyncio.run(run_chat(host, port, msg, clean_text(nickname)))
