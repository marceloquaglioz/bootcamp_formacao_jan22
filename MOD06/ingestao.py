import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi():
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    def _get_endpoint(self) -> str:
        return f"{self.base_endpoint}/{self.coin}/day-summary/2021/6/21"

    def get_data(self) -> dict:
        endpoint = self._get_endpoint()
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

print(MercadoBitcoinApi(coin='BTC').get_data())

print(MercadoBitcoinApi(coin='LTC').get_data())
