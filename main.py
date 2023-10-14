import discord, re, os
from datetime import datetime
from dotenv import load_dotenv

regex = '(?:https://)(?:twitter.com|x.com)/(\w+)/status/(\d+)(?:\?(t|s|fbclid)=\w+)?(?:&s=[0-9]+)?'
urlRegex = '(twitter.com|x.com)'

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(
    intents=intents 
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_message(message: discord.Message):

    if message.author.id == bot.user.id:
        return

    if re.search(regex, message.content):
        msgQuote = False
        msg = []
        now = datetime.now()

        for _ in re.split('(\s)', message.content):
            if y := re.match(regex, _):
                msg.append(re.sub(urlRegex, f'fixupx.com', _))
                print(now.strftime("%Y-%m-%d %H:%M:%S") + f": Detected: {y.group(0)}")
            else:
                msgQuote = True
                msg.append(_)
        fixed = ''.join(msg)

        try:
            if msgQuote:
                await message.channel.send(f"## {message.author.mention}:speech_balloon: \n{fixed}")
            else:
                await message.channel.send(f"## {message.author.mention}\n{fixed}")
        except discord.errors.Forbidden: 
            print(now.strftime("%Y-%m-%d %H:%M:%S") + ': Unable to send message in channel (permissions error).')
            return
        try:
            await message.delete()
        except discord.errors.Forbidden:
            print(now.strftime("%Y-%m-%d %H:%M:%S") + ': Unable to delete original message (permissions error).')
            return

if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
