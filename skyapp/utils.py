import requests

url = 'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create'
headers = {"x-api-key": "prtl6749387986743898559646983194"}


def func(a):
    kod = str(a)[17:23]
    return kod


def result(data):
    # data = {
    #     "query": {
    #         "market": "UZ",
    #         "locale": "en-GB",
    #         "currency": "UZS",
    #         "query_legs": [
    #             {
    #                 "origin_place_id": {"iata": "TAS"}, "destination_place_id": {"iata": "IST"},
    #                 "date": {"year": 2022, "month": 9, "day": 20}}
    #         ],
    #         "adults": 1,
    #         "cabin_class": "CABIN_CLASS_ECONOMY"
    #     }}

    x = requests.post(url, json=data, headers=headers)
    text = x.json()
    itinars = text['content']['results']['itineraries']
    agents = text['content']['results']['agents']
    # lis = itinars['16759-2209200230--32532-1-12585-2209200900']#['pricingOptions'][0]['price']['amount'])
    prices = []
    myd = {}

    i = 1
    for r in itinars:
        price = int(itinars[r]['pricingOptions'][0]['price']['amount']) / 1000
        prices.append(int(itinars[r]['pricingOptions'][0]['price']['amount']) / 1000)
        kod = func(r)
        carriers = text['content']['results']['carriers'][kod]
        carriers['price'] = price
        myd[i] = carriers
        i += 1

    # print(myd)
    return myd
