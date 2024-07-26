import asyncio
from typing import Type

import discord
from discord.ext.commands import Cog

from src import config
from src.bot import Bot
from src.commands import Commands


async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    commands: list[Type[Cog]] = [
        Commands
    ]

    async with Bot(command_prefix='!', intents=intents, custom_commands=commands) as bot:
        await bot.start(config.discord_token)


if __name__ == '__main__':
    asyncio.run(main())
