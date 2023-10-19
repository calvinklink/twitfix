import discord, re, os
from datetime import datetime
from dotenv import load_dotenv
from asyncio import get_event_loop

from redis import asyncio as redis
from redis.exceptions import *

class Twitfix(discord.Bot):
    def __init__(self, intents=None):
        self._regex = "(?:https://)(?:twitter.com|x.com)/(\w+)/status/(\d+)(?:\?(t|s|fbclid)=\S+)?(?:&s=[0-9]+)?"
        self._redis_client = redis.Redis()
        discord.Bot.__init__(self, intents=intents)

    async def on_ready(self):
        try:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Redis connected: {await self._redis_client.ping()}")
        except (ConnectionRefusedError, ConnectionError) as e:
            # Cannot connect to redis server, continue without
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> WARNING: Could not connect to Redis server. Continuing without.")
            self._redis_client = None

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Logged in as {self.user} (Bot ID: {self.user.id})")

    async def on_message(self, message):
        if message.author.id == self.user.id: return

        content = message.content
            
        replacement_message = re.sub(self._regex, lambda match: f"https://fixupx.com/{match.group(1)}/status/{match.group(2)}", content)
        if (replacement_message == content): return

        replacement_message = "".join([ f"\n> {paragraph}" if paragraph != "" else "\n" for paragraph in replacement_message.split("\n") ])
        replacement_message = f"## {message.author.mention}:speech_balloon: \n" + replacement_message

        try:
            if message.reference:
                reply = await message.channel.fetch_message(message.reference.message_id)
                await reply.reply(replacement_message)
            else:
                await message.channel.send(replacement_message)
                
            await message.delete()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Fixed new link! (Message ID: {message.id})")
        except discord.errors.Forbidden as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> {e}")

        if self._redis_client:
            try:
                await self._redis_client.incrby("fixed_messages", 1)
            except (ConnectionRefusedError, ConnectionError) as e:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> WARNING: Cannot connect to Redis database!!")   

intents = discord.Intents.default()
intents.message_content = True

twitfix = Twitfix(
    intents=intents
)

@twitfix.slash_command(name="setlink")
async def setlink(ctx: discord.ApplicationContext, link: discord.Option(str, choices=["fixupx", "vxtwitter"])):
    if twitfix._redis_client:
        try:
            await twitfix._redis_client.hset("guild", ctx.guild.id, link)
        except (ConnectionRefusedError, ConnectionError) as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> WARNING: Cannot connect to Redis database!!") 

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Updated link choice. (Guild ID: {ctx.guild.id})")

        await ctx.respond(embed=discord.Embed(
            title="Updated choice",
            description=f"Set Twitter replacement link provider to `{link}`\n\n[Invite me](https://github.com/calvinklink/twitfix/tree/main) | [GitHub](https://github.com/calvinklink/twitfix/tree/main)",
            color=discord.Colour.blue(),
        ))
    else:
        await ctx.respond(embed=discord.Embed(
            title="Bot Error",
            description=f"Cannot complete this action right now. Try again later.\n\n[Invite me](https://github.com/calvinklink/twitfix/tree/main) | [GitHub](https://github.com/calvinklink/twitfix/tree/main)",
            color=discord.Colour.blue(),
        ))

@twitfix.slash_command(name="info")
async def info(ctx):
    try:
        data = await twitfix._redis_client.get("fixed_messages")
        await ctx.respond(embed=discord.Embed(
            title="Twitfix info",
            description=f"Messaged fixed: `{data.decode('utf-8') }`\n\n[Invite me](https://github.com/calvinklink/twitfix/tree/main) | [GitHub](https://github.com/calvinklink/twitfix/tree/main)",
            color=discord.Colour.blue(),
        ))
    except (ConnectionRefusedError, ConnectionError) as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> WARNING: Cannot connect to Redis database!!") 

if __name__ == "__main__":
    load_dotenv()
    twitfix.run(os.getenv("TOKEN"))
