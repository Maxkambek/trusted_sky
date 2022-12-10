import hashlib
import requests

secret_key = '7lWI4rX8pbS8UyEw'

url = 'https://api.paybox.money/init_payment.php'

data = {
    'pg_order_id': '23',
    'pg_merchant_id': '547013',
    'pg_amount': '25',
    'pg_description': 'test',
    'pg_salt': 'molbulak',
    'pg_currency': 'KZT',
    'pg_check_url': 'http://site.kz/check',
    'pg_result_url': 'http://site.kz/result',
    'pg_request_method': 'POST',
    'pg_success_url': 'http://fe3f-213-230-121-237.ngrok.io/airport/success-url/',
    'pg_failure_url': 'http://site.kz/failure',
    'pg_success_url_method': 'GET',
    'pg_failure_url_method': 'GET'
}

string = ''
for i in sorted(data.keys()):
    string = string + str(data[i]) + ';'

q = f'init_payment.php;{string}{secret_key}'
sig = (hashlib.md5(f'init_payment.php;{string}{secret_key}'.encode()).hexdigest())
data['pg_sig'] = sig
res = requests.post(url=url, data=data)
print(res.text)
