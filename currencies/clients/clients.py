from shop.api_clients import BaseClient


class PrivatBankAPI(BaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def get_currency(self):
        currency_list = self._request(
            'get',
            params={'exchange': '', 'coursid': 5, 'json': ''}
        )
        for currency in currency_list:
            if 'err_internal_server_error' in currency.keys() or \
                    'err_incorrect_json' in currency.keys():
                return MonoBankAPI.get_currency()
        return currency_list


class MonoBankAPI(BaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def reformat_currency(self, currency_list):
        iso_codes = {
            980: 'UAH',
            840: 'USD',
            978: 'EUR'
        }
        reform_currency_list = []
        for currency in currency_list:
            if 'err_internal_server_error' in currency.keys() or \
                    'err_incorrect_json' in currency.keys() or \
                    'errorDescription' in currency.keys():
                return NationalBankAPI.get_currency()
            else:
                if iso_codes[currency['currencyCodeB']] == 'UAH' and \
                        currency['currencyCodeA'] in iso_codes.keys():
                    reform_currency_list.append({
                        'ccy': iso_codes[currency['currencyCodeA']],
                        'buy': currency['rateBuy'],
                        'sale': currency['rateSell']
                    })
        return reform_currency_list

    def get_currency(self):
        currency_list = self._request(
            'GET',
            params={'json': ''}
        )
        return self.reformat_currency(currency_list)


class NationalBankAPI(BaseClient):
    base_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'

    def reformat_currency(self, currency_list):
        reform_currency_list = []
        for currency in currency_list:
            reform_currency_list.append({
                'ccy': currency['cc'],
                'buy': currency['rate'],
                'sale': currency['rate']
            })
        return reform_currency_list

    def get_currency(self):
        currency_list = self._request(
            'get',
            params={'json': ''}
        )
        return self.reformat_currency(currency_list)


privat_currency_client = PrivatBankAPI()
monobank_currency_client = MonoBankAPI()
nbu_currency_client = NationalBankAPI()
