import argparse
import asyncio
import logging
import os

TOKEN = '3d9a78ce-3daa-11ed-8c47-0242ac110002'

async def chat_writer(host, port, message):
    reader, writer = await asyncio.open_connection(host, port)
    reply = await reader.readline()
    logging.debug(reply)
    writer.write((TOKEN + '\n').encode())
    await writer.drain()
    reply = await reader.readline()
    logging.debug(reply)
    writer.write((message + '\n\n').encode())
    await writer.drain()
    reply = await reader.readline()
    logging.debug(reply)

    writer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='minechat.dvmn.org')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('--msg')
    args = parser.parse_args()

    host = args.host or os.getenv('HOST')
    port = args.port or os.getenv('PORT')
    msg = args.msg

    asyncio.run(chat_writer(host, port, msg))
