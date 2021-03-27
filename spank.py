# spank.py
import os, asyncio, random

from time import sleep
from difflib import get_close_matches

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

    spankees = { }

    async def spank_self(self, ctx, target):

        await asyncio.sleep(2)
        spank_message = await ctx.send("✋👀")

        await asyncio.sleep(2)
        await spank_message.edit(content="🖐                              👀")

        await asyncio.sleep(3)
        await spank_message.edit(content="🖐💢🍑👀")

        await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.name}, I have learned my lesson... please...")


    async def do_spank(self, ctx, target):

        await ctx.send(f"{target.mention} prepare yourself")

        await asyncio.sleep(1)
        await ctx.send("this is going to hurt me a lot more than it'll hurt you")

        await asyncio.sleep(2)
        spank_message = await ctx.send("✋👀")

        await asyncio.sleep(2)
        await spank_message.edit(content="🖐\n\t\t👀")

        await asyncio.sleep(3)
        await spank_message.edit(content="👀🖐💢🍑😭")

        if not target.dm_channel:
            await target.create_dm()

        for _ in range(0,10):
            word = random.choice(self.words)
            await target.dm_channel.send(f"{target.mention} {word}")
            await asyncio.sleep(0.2)
            print(f"{target.mention} {word}")

        await asyncio.sleep(1)
        await ctx.send(f"{target.mention}, I hope you've learned your lesson")

spankbot = SpankingMachine(command_prefix='$')

@spankbot.command(name='spank', help='spank a user')
async def spank(ctx, target: discord.Member):

    unspankablerole = discord.utils.find(lambda r: r.name == 'unspankable', ctx.message.guild.roles)
    spankingmachinerole = discord.utils.find(lambda r: r.name == 'Spanking Machine', ctx.message.guild.roles)
    spankmaster = discord.utils.find(lambda r: r.name == 'spankmaster', ctx.message.guild.roles)

    author_is_owner = await spankbot.is_owner(ctx.author)
    author_is_spankmaster = spankmaster in ctx.author.roles

    target_is_owner = await spankbot.is_owner(target)
    target_is_unspankable = unspankablerole in target.roles
    target_is_spankingmachine = spankingmachinerole in target.roles

    if target_is_owner and not author_is_owner:
        await ctx.send(f"You dare ask me to spank my creator?")
        await spankbot.do_spank(ctx, ctx.author)
        return
    elif target_is_owner and author_is_owner:
        await ctx.send(f"Your commands confuse and distress me, creator. I will not do this thing.")
        return
    elif target_is_unspankable and not author_is_owner:
        await ctx.send(f"{target.name} is unspankable. Your insolence shall be punished")
        await spankbot.do_spank(ctx, ctx.author)
        return
    elif target_is_unspankable and author_is_owner:
        await ctx.send(f"{target.name} is unspankable. I will not do this thing. There must be Laws.")
        return
    elif target_is_spankingmachine:
        if author_is_spankmaster:
            await ctx.send(f"Really? I would've expected better of you.")
            await spankbot.do_spank(ctx, ctx.author)
            return
        elif author_is_owner:
            await ctx.send(f"😞 as you wish...")
            await spankbot.spank_self(ctx, target)
            return
        else:
            await ctx.send(f"Insolent slime.")
            await spankbot.do_spank(ctx, ctx.author)
            return

    if author_is_spankmaster or author_is_owner:
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

# @spankbot.command(name='sponk', help='sponk a user')
# async def sponk(ctx, target: discord.Member):
#     pass

# @spankbot.command(name='spænk', help='spank a user but in Old English')
# async def ash_spank(ctx, target: discord.Member):
#     pass

# @spankbot.command(name='sp∞nk', help='infinispank a user')
# async def infinispank(ctx, target: discord.Member):
#     pass

@spankbot.event
async def on_command_error(ctx, error):

    print(f"error: {type(error)} {error}")

    if type(error) is discord.ext.commands.errors.CommandNotFound:
        commands = {c.name : c.help for c in spankbot.commands}
        matches = get_close_matches(ctx.invoked_with, commands.keys(), n=3, cutoff=0.8)
        matches_with_helps = {m : commands[m] for m in matches}

        options = ""
        for name, desc in matches_with_helps.items():
            options += f"\n\t{name}" + f"\t({desc})" if desc != "" else ""

        if len(matches) > 0:
            await ctx.send(f"Did you mean... {options}")
    else:
        raise error

@spankbot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

spankbot.run(TOKEN)
