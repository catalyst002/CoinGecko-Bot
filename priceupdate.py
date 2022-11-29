import time
import json
import aiohttp
import asyncio
import ast
import requests
from aiogram import Bot
import sqlite3 as sl

db = sl.connect('test.db')


BOT_TOKEN = ""
CONV_WITH_BOT_ID = 6666666666

bot = Bot(token=BOT_TOKEN)


f = open("coins.txt", "r")
coins = f.read()
coins = ast.literal_eval(coins)


coins = coins[0:101]


async def send_message(message):
    await bot.send_message(CONV_WITH_BOT_ID, message)


def priceupdate(dbcoinname, coin, platform, i):
    base = coin["tickers"][i]["base"]
    target = coin["tickers"][i]["target"]
    newprice = coin["tickers"][i]["converted_last"]["usd"]
    try:
        oldprice = db.execute(
            f'SELECT price FROM {dbcoinname} WHERE pair = "{base}/{target}" AND platform = "{platform}"').fetchone()[0]
        if newprice > oldprice:
            change = newprice / oldprice
            if change > 5:
                asyncio.run(send_message(
                    f'{platform} {coin["tickers"][i]["base"]}/{coin["tickers"][i]["target"]} {change}% increase'))
        else:
            change = (oldprice - newprice) / oldprice
            if change > 5:
                asyncio.run(send_message(
                    f'{platform} {coin["tickers"][i]["base"]}/{coin["tickers"][i]["target"]} {change}% decrease'))
        update = db.execute(
            f'UPDATE {dbcoinname} SET price = {newprice} WHERE pair = "{coin["tickers"][i]["base"]}/{coin["tickers"][i]["target"]}" AND platform = "{platform}"')
    except TypeError as e:
        print("Adding new pair to database")
        print(dbcoinname, base, target, platform, newprice)
        db.execute(
            f'UPDATE {dbcoinname} SET price = {newprice} WHERE pair = "{coin["tickers"][i]["base"]}/{coin["tickers"][i]["target"]}" AND platform = "{platform}"')


for coinname in coins:
    dbcoinname = str(coinname).replace("-", "")
    coin = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{coinname}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false")

    coin = coin.json()
    print(coin)
    tickerslen = len(coin["tickers"])

    for i in range(tickerslen):
        if coin["tickers"][i]["market"]["name"] == "Uniswap (v3)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Uniswap (v3)", i)

        if coin["tickers"][i]["market"]["name"] == "Uniswap (v2)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Uniswap (v2)", i)

        if coin["tickers"][i]["market"]["name"] == "Sushiswap" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Sushiswap", i)
        if coin["tickers"][i]["market"]["name"] == "PancakeSwap (v2)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "PancakeSwap (v2)", i)

        if coin["tickers"][i]["market"]["name"] == "Uniswap (Arbitrum One)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Uniswap (Arbitrum One)", i)

        if coin["tickers"][i]["market"]["name"] == "Optimism" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Optimism", i)
        if coin["tickers"][i]["market"]["name"] == "Uniswap (Polygon)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Uniswap (Polygon)", i)
        if coin["tickers"][i]["market"]["name"] == "Binance" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Binance", i)
        if coin["tickers"][i]["market"]["name"] == "Huobi Global" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "Huobi Global", i)
        if coin["tickers"][i]["market"]["name"] == "KuCoin" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "KuCoin", i)
        if coin["tickers"][i]["market"]["name"] == "FTX" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            priceupdate(dbcoinname, coin, "FTX", i)
    time.sleep(6)
f.close()
