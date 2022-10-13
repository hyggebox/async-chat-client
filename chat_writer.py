import argparse
import asyncio
import json
import logging
import os

import aiofiles


async def authorize_user(reader, writer, account_hash):
    reply = await reader.readline()
    logging.debug(reply)
    writer.write((account_hash + '\n').encode())
    await writer.drain()
    reply = await reader.readline()
    logging.debug(reply)
    if not json.loads(reply):
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')


async def register_user(reader, writer, nickname, data_file_name):
    reader, writer = await asyncio.open_connection(host, port)
    reply = await reader.readline()
    logging.debug(reply)

    writer.write('\n'.encode())
    await writer.drain()
    reply = await reader.readline()
    logging.debug(reply)

    writer.write((nickname + '\n').encode())
    await writer.drain()
    user_details = await reader.readline()
    logging.debug(user_details)
    async with aiofiles.open(data_file_name, mode='w') as f:
        await f.write(json.dumps(json.loads(user_details), indent=4))


async def submit_message(reader, writer, message):
    writer.write((message + '\n\n').encode())
    await writer.drain()
    reply = await reader.readline()
    logging.debug(reply)


def clean_text(text):
    if isinstance(text, str):
        return text.replace('\\', '')
    return text


async def run_chat(host, port, message, nickname):
    reader, writer = await asyncio.open_connection(host, port)
    data_file_name = 'user_details.json'

    try:
        if nickname:
            await register_user(reader, writer, nickname, data_file_name)
        if os.path.exists(data_file_name):
            async with aiofiles.open(data_file_name, 'r') as f:
                data = await f.read()
                account_hash = json.loads(data)['account_hash']
                await authorize_user(reader, writer, account_hash)
        else:
            print('Придумайте ник для регистрации в чате: --nickname / -n')
            return

        await submit_message(reader, writer, message)

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
