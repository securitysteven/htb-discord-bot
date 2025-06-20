import asyncio
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()


async def main():
    bot = commands.InteractionBot()

    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")

    @bot.slash_command(name="cpe")
    async def cpe(
        inter: disnake.GuildCommandInteraction,
        name: str = commands.Param(
            name="name", description="Please provide your full name"
        ),
        events: str = commands.Param(
            name="events",
            description="Please provide the events you have attended seperated by comma (Eg 0x01, 0x02)",
        ),
    ):
        """Receive a CPE for your HTB attendance."""
        await inter.response.defer(ephemeral=True)
        # Generate certificates here
        await inter.send(f"Hello {name}, you attended {events}", ephemeral=True)

    await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
