import requests
from duffel_api import Duffel

client = Duffel(access_token='duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7')

url = 'https://api.duffel.com/air/airports'
headers = {
    'Accept-Encoding': 'gzip',
    "Accept": "application/json",
    "Duffel-Version": "v1",
    "Authorization": "Bearer duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7"
}
params = {
    'limit': 200,
    'iata_city_code': 'LON',
    'iata_code': 'LON',
    'after': None,
    'before': None
}

res = requests.get(url=url, headers=headers, params=params)
print(res.text)
