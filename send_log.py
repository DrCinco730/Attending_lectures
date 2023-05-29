from telethon import TelegramClient


class Login:
    def __init__(self, text):
        self.text = text
        with TelegramClient('anon', 14660906, "3d4a210e1d846b2e57d8d2c0b757b149") as client:
            for x in ["+967701748581", "967775057605"]:
                client.loop.run_until_complete(client.send_message(x, self.text))
