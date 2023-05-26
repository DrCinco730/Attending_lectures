from telethon import TelegramClient


client = TelegramClient('anon', 14660906, "3d4a210e1d846b2e57d8d2c0b757b149")




async def main():
    await client.send_message("me","hi")


with client:
    client.loop.run_until_complete(main())
