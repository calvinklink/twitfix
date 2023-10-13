import discord, re, os
from datetime import datetime
from dotenv import load_dotenv
from asyncio import get_event_loop

regex = '(?:https://)(?:twitter.com|x.com)/(\w+)/status/(\d+)(?:\?(t|s|fbclid)=\w+)?(?:&s=[0-9]+)?'

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(
    intents=intents 
)

def parse_message(message):
    content = message.content
    if not (matches := [x for x in re.finditer(regex, content)]): return

    for match in matches:
        content = content[:match.start()] + f"https://fixupx.com/{match.group(1)}/status/{match.group(2)}" + content[match.end():]

    # if link(s) are not the only thing in the message, parse message to quote paragraphs.
    if len(content) > matches[len(matches) - 1].end() - matches[0].start():
        content = "".join([ f"\n> {paragraph}" if paragraph != "" else "\n" for paragraph in content.split("\n") ])
        content = f"## {message.author.mention}:speech_balloon: \n" + content
    else:
        content = f"## {message.author.mention}\n" + content

    return content

@bot.event
async def on_ready():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Logged in as {bot.user} (Bot ID: {bot.user.id})")

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id: return

    # Parse messages on separate thread as the code is slow and blocks event loop
    if not (replacement_message := await get_event_loop().run_in_executor(None, parse_message, message)): return

    try:
        await message.channel.send(replacement_message)
        await message.delete()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> Fixed new link! (Message ID: {message.id})")
    except discord.errors.Forbidden as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-> {e}")

if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
