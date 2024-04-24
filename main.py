import asyncio
import os

import discord
from dotenv import dotenv_values

from src.bot import Bot


async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    extensions = [
        f"src.extensions.{extension.rstrip('.py')}"
        for extension in os.listdir("src/extensions")
        if extension.endswith(".py")
    ]

    async with Bot(command_prefix="!", intents=intents, extensions=extensions) as bot:
        await bot.start(dotenv_values()['DISCORD_TOKEN'])


if __name__ == '__main__':
    asyncio.run(main())
