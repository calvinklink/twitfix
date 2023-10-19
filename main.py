import discord, re, os
from datetime import datetime
from dotenv import load_dotenv
from asyncio import get_event_loop

regex = '(?:https://)(?:twitter.com|x.com)/(\w+)/status/(\d+)(?:\?(t|s|fbclid)=\S+)?(?:&s=[0-9]+)?'

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(
    intents=intents 
)

@bot.event
async def on_ready():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Logged in as {bot.user} (Bot ID: {bot.user.id})")

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id: return

    content = message.content
        
    replacement_message = re.sub(regex, lambda match: f'https://fixupx.com/{match.group(1)}/status/{match.group(2)}', content)
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

if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
