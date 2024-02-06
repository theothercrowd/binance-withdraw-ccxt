import time
import ccxt
from termcolor import cprint
import random
import time
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Union

def unix_to_strtime(unix_time: Union[int, float, str] = None, utc_offset: Optional[int] = None,
                    format: str = '%d.%m.%Y %H:%M:%S') -> str:
    """
    Convert unix to string time. In particular return the current time.
    :param Union[int, float, str] unix_time: a unix time (current)
    :param int utc_offset: hour offset from UTC (None)
    :param str format: format for string time output (%d.%m.%Y %H:%M:%S)
    :return str: the string time
    """
    if not unix_time:
        unix_time = time.time()

    if isinstance(unix_time, str):
        unix_time = int(unix_time)

    if utc_offset is None:
        strtime = datetime.fromtimestamp(unix_time)
    elif utc_offset == 0:
        strtime = datetime.utcfromtimestamp(unix_time)
    else:
        strtime = datetime.utcfromtimestamp(unix_time).replace(tzinfo=timezone.utc).astimezone(
            tz=timezone(timedelta(seconds=utc_offset * 60 * 60)))

    return strtime.strftime(format)

# Set up logging

logging.basicConfig(filename='/binance_withdrawal.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S - %d-%m-%Y')
current_time = unix_to_strtime(time.time())

# Binance withdrawal with logging

def binance_withdraw(address, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET):

    account_binance = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    try:
        account_binance.withdraw(
            code    = symbolWithdraw,
            amount  = amount_to_withdrawal,
            address = address,
            tag     = None,
            params  = {
                "network": network
            }
        )
        cprint(f"{current_time} +++ | {address} | {amount_to_withdrawal} | {symbolWithdraw}", "green")
        logging.info(f'Withdrawal of {amount_to_withdrawal} {symbolWithdraw} to {address} was done.')

    except Exception as error:
        cprint(f"{current_time} --- | {address} | {error}", "red")
        logging.error(f'{address} | {error}')

if __name__ == "__main__":
    
    with open("wallets.txt", "r") as f:
        wallets_list = [row.strip() for row in f]

    symbolWithdraw = 'ETH'
    network        = 'ARBITRUM' # ETH | BSC | AVAXC | MATIC | ARBITRUM | OPTIMISM | APT

    # api_keys of binance
    API_KEY     = "your_api_key"
    API_SECRET  = "your_api_secret"
    AMOUNT_FROM = 0.001
    AMOUNT_TO   = 0.002
    cprint('\a\n/// starting withdrawal process...', 'black')
    cprint('')

    # Iteration with exit on the last wallet and info about timing of the next withdawal

    for i, wallet in enumerate(wallets_list):

        amount_to_withdrawal = round(random.uniform(AMOUNT_FROM, AMOUNT_TO), 6) # amount from ... to ...
        binance_withdraw(wallet, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET)
        if i != len(wallets_list) - 1:
            delay = random.randint(50, 350)
            next_time = unix_to_strtime(time.time() + delay)
            cprint(f"The next one comes in {delay} seconds, at: {next_time}","yellow" )
            time.sleep(delay)


