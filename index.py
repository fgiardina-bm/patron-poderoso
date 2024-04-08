import ccxt
import talib
import numpy as np
from datetime import datetime, timezone
import pandas as pd
from binance.client import Client
import time
import sys

exchange = ccxt.binance()
client = Client("", "", tld="com")


def obtener_datos(symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    ohlcv = [
        [
            datetime.fromtimestamp(x[0] / 1000, tz=timezone.utc),
            x[1],
            x[2],
            x[3],
            x[4],
            x[5],
        ]
        for x in ohlcv
    ]

    return ohlcv


def calcular_rsi(closes, window=14):
    rsi = talib.RSI(np.array(closes), timeperiod=window)
    return rsi


def get_bb_data(symbol, timeframe):
    continuous_klines = client.futures_klines(
        symbol=symbol, interval=timeframe, limit=30
    )

    data = []
    for ck in continuous_klines:
        item = {
            "open": float(ck[1]),
            "high": float(ck[2]),
            "low": float(ck[3]),
            "close": float(ck[4]),
            "volume": float(ck[5]),
        }

        data.append(item)

    df_bb = pd.DataFrame(data)
    return df_bb


def verificar_patron_poderoso(symbol, timeframe):
    ohlcv = obtener_datos(symbol, timeframe)
    closes = [x[4] for x in ohlcv]

    df_bb = get_bb_data(symbol, timeframe)

    upper_bb, lower_bb = bollinger_bands(df_bb, 20, 2)
    upper_band = upper_bb.iloc[-1]
    lower_band = lower_bb.iloc[-1]
    rsi = calcular_rsi(closes)

    if closes[-1] > upper_band and rsi[-1] > rsi_up:
        print()
        print("POSIBLE SHORT")
        print(
            f"Patrón poderoso detectado en {symbol} en el intervalo de tiempo {timeframe}"
        )
        print(f"Bollinger Upper Band: {upper_band}")
        print(f"Bollinger Lower Band: {lower_band}")
        print(f"Close: {closes[-1]}")
        print(f"RSI: {rsi[-1]}")
        print()
    elif closes[-1] < lower_band and rsi[-1] < rsi_down:
        print()
        print("POSIBLE LONG")
        print(
            f"Patrón poderoso detectado en {symbol} en el intervalo de tiempo {timeframe}"
        )
        print(f"Bollinger Upper Band: {upper_band}")
        print(f"Bollinger Lower Band: {lower_band}")
        print(f"Close: {closes[-1]}")
        print(f"RSI: {rsi[-1]}")
        print()


def buscarticks():
    ticks = []
    lista_ticks = client.futures_symbol_ticker()

    for tick in lista_ticks:
        if tick["symbol"][-4:] != "USDT":
            continue
        ticks.append(tick["symbol"])

    print("Numero de monedas encontradas en el par USDT: #" + str(len(ticks)))

    return ticks


def bollinger_bands(data, n_loockback, n_std=2):
    hlc_avg = (data.high + data.low + data.close) / 3
    mean, std = hlc_avg.rolling(n_loockback).mean(), hlc_avg.rolling(n_loockback).std()
    upper, lower = mean + std * n_std, mean - std * n_std

    return upper, lower


timeframe = sys.argv[1]
rsi_up = 80
rsi_down = 20


def buscar_pares():
    symbols = buscarticks()
    for symbol in symbols:
        verificar_patron_poderoso(symbol, timeframe)


while True:
    print()
    print("Buscando patrones poderosos...")
    print(f"{timeframe} {datetime.now().strftime('%H:%M')}")
    buscar_pares()
    print("Esperando 60 segundos...")
    time.sleep(60)
