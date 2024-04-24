from discord import Message
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self,
                 extensions: list[str] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_extensions = extensions

    async def setup_hook(self) -> None:
        if self.initial_extensions is not None:
            for extension in self.initial_extensions:
                await self.load_extension(extension)

    async def on_ready(self):
        print(f"Logged in as '{self.user}'")

    async def on_message(self, message: Message) -> None:
        context = await self.get_context(message)

        if context.valid:
            if context.command:
                print(f"'{message.author}' used '{context.command}'")

                await self.process_commands(message)
