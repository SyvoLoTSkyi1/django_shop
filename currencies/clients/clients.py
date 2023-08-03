from requests import request


class GetCurrencyBaseClient:
    base_url = None

    def _request(self, method: str, params: dict=None,
                 headers: dict=None, data: dict=None):

        try:
            response = request(
                url=self.base_url,
                method=method,
                params=params or {},
                data=data or {},
                headers=headers or {}
            )
        except Exception:
            # todo logging errors and success results
            ...
        else:
            return response.json()


class PrivatBankAPI(GetCurrencyBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def get_currency(self) -> dict:
        return self._request(
            'get',
            params={'exchange': '', 'coursid': 5, 'json': ''}
        )


class MonoBankAPI(GetCurrencyBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def get_currency(self) -> dict:
        return self._request(
            'get'
        )


class NationalBankAPI(GetCurrencyBaseClient):
    base_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'

    def get_currency(self) -> dict:
        return self._request(
            'get',
            params={'json': ''}
        )


privat_currency_client = PrivatBankAPI()
monobank_currency_client = MonoBankAPI()
nbu_currency_client = NationalBankAPI()
