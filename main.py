import asyncio
import datetime

import aiofiles


async def chat_reader():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    while True:
        line = await reader.readline()
        now = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        if not line:
            break

        message = f'[{now}] {line.decode()}'
        print(message.rstrip())

        async with aiofiles.open('chat.txt', mode='a') as f:
            contents = await f.write(message)

    writer.close()


asyncio.run(chat_reader())
