import time
import json
import aiohttp
import asyncio
import ast
import requests
import sqlite3 as sl

db = sl.connect('test.db')


f = open("coins.txt", "r")
coins = f.read()
coins = ast.literal_eval(coins)


def insertdata(coinname, coin, i):
    with db:
        sql = f'INSERT INTO {coinname} (pair, platform, price) VALUES (?, ?, ?)'
        data = [
            (f'{coin["tickers"][i]["base"]}/{coin["tickers"][i]["target"]}', coin["tickers"][i]["market"]["name"],
             coin["tickers"][i]["converted_last"]["usd"]
             )
        ]
        db.executemany(sql, data)


coins = coins[0:250]

for coinname in coins:
    dbcoinname = str(coinname).replace("-", "")
    coin = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{coinname}?localization=false&tickers=true&market_data=false&community_data=false&developer_data=false&sparkline=false")

    with db:
        db.execute(f"""
					CREATE TABLE {dbcoinname} (
					pair TEXT,
					platform TEXT,
					price int
					);
				""")

    coin = coin.json()
    print(coin)
    tickerslen = len(coin["tickers"])

    for i in range(tickerslen):
        if coin["tickers"][i]["market"]["name"] == "Uniswap (v3)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Uniswap (v2)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Sushiswap" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "PancakeSwap (v2)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Uniswap (Arbitrum One)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Optimism" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Uniswap (Polygon)" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Binance" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "Huobi Global" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "KuCoin" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
        if coin["tickers"][i]["market"]["name"] == "FTX" and coin["tickers"][i]["converted_last"]["usd"] > 0 and coin["tickers"][i]["converted_volume"]["usd"] > 10000:
            insertdata(dbcoinname, coin,  i)
    time.sleep(6)
f.close()
