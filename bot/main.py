import os, random, asyncio
import discord
from discord.ext import commands
import httpx
from discord_slash import SlashCommand, SlashContext

client = commands.Bot(command_prefix=";")
slash = SlashCommand(client, sync_commands=True)

coingecko = "https://api.coingecko.com/api/v3/simple/price?ids=plant-vs-undead-token&vs_currencies=usd,idr,bnb"
WAIT_DURATION = int(os.environ['WAIT_DURATION'])
TOKEN = os.environ['DISCORD_TOKEN']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
    asyncio.create_task(taskUpdateActivity())


def getCoingeckoData():
    with httpx.Client(timeout=None) as httpx_client:
        response = httpx_client.get(coingecko)
        data = response.json()
        return data


def getWanaPerUSD():
    return float(getCoingeckoData()["plant-vs-undead-token"]['usd'])


def getWanaPerIDR():
    return float(getCoingeckoData()["plant-vs-undead-token"]['idr'])


def getWanaPerBNB():
    return float(getCoingeckoData()["plant-vs-undead-token"]['bnb'])


async def taskUpdateActivity():
    await client.wait_until_ready()
    while not client.is_closed():
        for guild in client.guilds:

            await guild.me.edit(nick="${:.2f}".format(getWanaPerUSD())+"/PVU")

        activityStatus = random.choice(["{:,}".format(round(getWanaPerIDR())) + " IDR", f"{getWanaPerBNB()} BNB"])

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activityStatus))
        print(f"$ {getWanaPerUSD()} - RP {getWanaPerIDR()} - BNB {getWanaPerBNB()}")
        await asyncio.sleep(WAIT_DURATION)

client.run(TOKEN)
