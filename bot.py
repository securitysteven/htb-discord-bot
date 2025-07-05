import asyncio
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from certificate_generator import generate_certificate

load_dotenv()

async def main():
    bot = commands.InteractionBot()

    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")

    @bot.slash_command(
        name="cpe",
        default_member_permissions=disnake.Permissions(manage_guild=True),
    )
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
        

        events_list = [e.strip() for e in events.split(',')]
        num_events = len(events_list)
        credits = 3  # Each event is 3 credits

        await inter.send(
            f"Hello {name}, you attended {num_events} events: {', '.join(events_list)}.\n"
            f"Generating your certificates ({credits} CPE credits per event)…",
            ephemeral=True
        )

        # Generate certificate
        files = []
        for event in events_list:
            pdf_buffer = generate_certificate(name=name, events=[event], credits=credits)
            filename = f"{name.replace(' ', '_')}_{event}_certificate_of_attendance.pdf"
            files.append(disnake.File(fp=pdf_buffer, filename=filename))

        await inter.send(content="Here are your certificates:", files=files, ephemeral=True)

    await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
