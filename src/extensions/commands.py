import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.tag_role: discord.Role = None
        self.tagged_member: discord.Member = None
        self.mention_user: bool = False
        self.allow_tagging_role: discord.Role = None
        self.last_tagged_members: list[discord.Member] = None
        self.bounce_limit: int = 1

    @commands.command(name='roles')
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def set_roles(self, context: commands.Context, tag_role: discord.Role, allow_tagging_role: discord.Role):
        self.tag_role = tag_role
        self.allow_tagging_role = allow_tagging_role

        await context.channel.send(
            f'Tagging role has been set to {tag_role.name}. Allow tagging role has been set to {allow_tagging_role.name}.')

    @commands.command(name='bounceLimit')
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def set_bounce_limit(self, context: commands.Context, bounce_limit: int):
        try:
            assert isinstance(bounce_limit, int)
            assert bounce_limit > 1

            self.bounce_limit = bounce_limit
            await context.channel.send(f"Bounce limit has been set to {self.bounce_limit}.")

        except AssertionError:
            await context.channel.send("Bounce limit must be a integer greater than 1.")

    @commands.command(name="start")
    @commands.has_any_role("Server Lead", "Admin", "Moderator")
    async def start(self, context: commands.Context, member: discord.Member):
        if self.tag_role not in member.roles and self.allow_tagging_role in member.roles:
            await member.add_roles(self.tag_role)

            self.last_tagged_members.append(member)

            if len(self.last_tagged_members) >= self.bounce_limit:
                self.last_tagged_members.pop(0)

            await context.channel.send(f'{member.name} has been tagged!')

        else:
            await context.channel.send(
                f"{member.name} could not be tagged. There are multiple reasons for this:\n- {member.name} are already {self.tag_role.name} tagged.\n- {member.name} don't have the {self.allow_tagging_role.name} role.")

    @commands.command(name='tag')
    async def tag_member(self, context: commands.Context, member: discord.Member):
        if self.tag_role in context.author.roles and self.tag_role not in member.roles and self.allow_tagging_role in member.roles and member not in self.last_tagged_members:
            await context.author.remove_roles(self.tag_role)
            await member.add_roles(self.tag_role)

            self.last_tagged_members.append(member)

            if len(self.last_tagged_members) >= self.bounce_limit:
                self.last_tagged_members.pop(0)

            await context.channel.send(f'{member.name} has been tagged!')

        else:
            await context.channel.send(
                f"{member.name} could not be tagged. There are multiple reasons for this:\n- You aren't tagged.\n- {member.name} is already tagged.\n- {member.name} doesn't participate in the tagging game.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
