"""

CREATED BY: Gerren B. Keith-Davis
CREATE DATE: 16-FEB-2022

LOGICAL ARCHITECTURE: https://docs.google.com/presentation/d/1ZIgaR_e14T0g2xHBV0q680WeaAGft4jEivLphbIZURA/edit#slide=id.g11500b1f8f6_0_0

# MAJOR POINTS TO ADDRESS
1. Find better API to get price of crypto currency

"""

from coinmarketcapapi import CoinMarketCapAPI as API
from config_secrets import cmc_api_key

def get_price(query):
    cmc = API(cmc_api_key)
    r = cmc.cryptocurrency_info(symbol=query)

    start_index = int(str(r.data.values())[13:-2].find('description'))
    end_index = int(str(r.data.values())[13:-2].find('24 hours'))
    description_str = str(r.data.values())[13:-2][start_index-1:end_index]
    check_list = description_str.split(' ')

    if query in ('BTC', 'ETH'):
        price = round(float(check_list[check_list.index('USD')-1].replace(',', '')), 2)
    else:
        price = round(float(check_list[check_list.index('USD')-1]), 2)

    if price == 0.0:
        return 0
    else:
        return round(price, 2)