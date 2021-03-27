# spank.py
import os, asyncio, random

from time import sleep

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class SpankingMachine(commands.Bot):

    words = [
        "smack",
        "hit",
        "slap",
        "whap",
        "bap",
        "thwap",
        "smack",
        "whack"
    ]

    vote_threshold = 3

    async def do_spank(self, ctx, target):

        await ctx.send(f"{target.mention} prepare yourself")

        sleep(1)

        await ctx.send("this is going to hurt me a lot more than it'll hurt you")

        sleep(2)

        spank_message = await ctx.send("🖐👀")

        sleep(2)

        await spank_message.edit(content="🖐\n\t\t👀")

        sleep(3)

        await spank_message.edit(content="👀🖐💢🍑😭")

        if not target.dm_channel:
            await target.create_dm()

        for _ in range(0,10):
            word = random.choice(self.words)
            await target.dm_channel.send(f"{target.mention} {word}")
            print(f"{target.mention} {word}")

        sleep(4)

        await ctx.send(f"{target.mention}, I hope you've learned your lesson")

spankbot = SpankingMachine(command_prefix='$')

@spankbot.command(name='spank', help='spank a user')
async def spank(ctx, target: discord.Member):

    unspankablerole = discord.utils.find(lambda r: r.name == 'unspankable', ctx.message.guild.roles)
    spankingmachinerole = discord.utils.find(lambda r: r.name == 'SpankingMachine', ctx.message.guild.roles)

    target_is_owner = await spankbot.is_owner(target)

    if target_is_owner or unspankablerole in target.roles or spankingmachinerole in target.roles:
        await ctx.send(f"{target.name} is unspankable.")
        # await asyncio.sleep(2)
        # await ctx.send(f"{ctx.author.name}, prepare to be spanked for your insolence")
        return

    spanker = discord.utils.find(lambda r: r.name == 'spanker', ctx.message.guild.roles)

    author_is_owner = await spankbot.is_owner(ctx.author)

    if spanker in ctx.author.roles or author_is_owner:
        await spankbot.do_spank(ctx, target)
    else:
        poll = await ctx.send(
            f"Spank request recognized for {target.mention} from non-preapproved spanker\n"
            f"Should @{target.name} be spanked? Vote Yes with 🖐\n"
            f"{spankbot.vote_threshold} votes total are needed to spank in the next minute will confirm Intent to Spank"
        )
        await poll.add_reaction("🖐")

        await asyncio.sleep(60)

        poll = await ctx.fetch_message(poll.id)

        hand_reacts = discord.utils.find(lambda r: r.emoji == "🖐", poll.reactions)

        if hand_reacts.count >= spankbot.vote_threshold:
            await spankbot.do_spank(ctx, target)
        else:
            await ctx.send(
                f"The vote has not passed in the alloted time"
                f"{target.name} is safe for now"
            )

@spankbot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


spankbot.run(TOKEN)
