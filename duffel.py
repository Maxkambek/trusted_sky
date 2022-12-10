import requests

url = 'https://api.duffel.com/air/seat_maps/'

headers = {
    "Accept-Encoding": "gzip",
    "Accept": "application/json",
    "Duffel-Version": "v1",
    "Authorization": "Bearer duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7"
}
params = {
    'offer_id': "off_0000AQS7qWCSziqRJ398q0"
}
res = requests.get(url=url, headers=headers, params=params)

print(res.text)
