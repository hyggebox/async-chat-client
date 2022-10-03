import argparse
import asyncio
import datetime
import os

import aiofiles


async def chat_reader(host, port, history_file):
    reader, writer = await asyncio.open_connection(host, port)

    while True:
        line = await reader.readline()
        now = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        if not line:
            break

        message = f'[{now}] {line.decode()}'
        print(message.rstrip())

        async with aiofiles.open(history_file, mode='a') as f:
            await f.write(message)

    writer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='minechat.dvmn.org')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--history_file', '-f', default='chat.txt')
    args = parser.parse_args()

    host = args.host or os.getenv('HOST')
    port = args.port or os.getenv('PORT')
    history_file = args.history_file or os.getenv('HISTORY_FILE')

    asyncio.run(chat_reader(host, port, history_file))
