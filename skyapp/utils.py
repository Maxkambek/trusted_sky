# import requests
#
# url = 'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create'
# headers = {"x-api-key": "prtl6749387986743898559646983194"}
#
#
# def func(a):
#     kod = str(a)[17:23]
#     return kod
#
#
# def result(data):
#     # data = {
#     #     "query": {
#     #         "market": "UZ",
#     #         "locale": "en-GB",
#     #         "currency": "UZS",
#     #         "query_legs": [
#     #             {
#     #                 "origin_place_id": {"iata": "TAS"}, "destination_place_id": {"iata": "IST"},
#     #                 "date": {"year": 2022, "month": 9, "day": 20}}
#     #         ],
#     #         "adults": 1,
#     #         "cabin_class": "CABIN_CLASS_ECONOMY"
#     #     }}
#
#     x = requests.post(url, json=data, headers=headers)
#     text = x.json()
#     itinars = text['content']['results']['itineraries']
#     agents = text['content']['results']['agents']
#     # lis = itinars['16759-2209200230--32532-1-12585-2209200900']#['pricingOptions'][0]['price']['amount'])
#     prices = []
#     myd = {}
#
#     i = 1
#     for r in itinars:
#         price = int(itinars[r]['pricingOptions'][0]['price']['amount']) / 1000
#         prices.append(int(itinars[r]['pricingOptions'][0]['price']['amount']) / 1000)
#         kod = func(r)
#         carriers = text['content']['results']['carriers'][kod]
#         carriers['price'] = price
#         myd[i] = carriers
#         i += 1
#
#     # print(myd)
#     return myd
#
#
# # class CityCreateView(generics.GenericAPIView):
# #     serializer_class = AirportSerializer
# #
# #     def post(self, request):
# #         file = request.data.get("file")
# #         rd = pd.read_csv(f"{file}")
# #         df = pd.DataFrame(rd)
# #
# #         # for row in df.itertuples():
# #         #     Airports.objects.get_or_create(
# #         #         iata=row.iata,
# #         #         name_ru=row.name_ru,
# #         #         name_en=row.name_en,
# #         #         parent_name_en=row.parent_name_en,
# #         #     )
# #
# #         # with open('airport_2.csv', encoding="utf8") as f:
# #         #     reader = csv.reader(f)
# #         #
# #         #     new_row = []
# #         #     reader = list(reader)
# #         #     # print(
# #         #     #     type(reader)
# #         #     # )
# #         #     print(reader[2])
# #         #     print(reader[2][2])
# #         #     for i in range(10):
# #         #         print(reader[i][2])
# #         # for row in reader:
# #         #     # print(row[0])
# #         #     print((row))
# #         # for r in row:
# #         # r.strip('""')
# #         # r = r.replace('""', '')
# #         # r.replace(' ', '')
# #         # new_row.append(r)
# #         # print(r[0])
# #         # print(new_row)
# #         # for i in new_row:
# #         #
# #         #     print(i[0])
# #
# #         return Response("Success")
# # class FindTicket(APIView):
# #
# #     def post(self, request):
# #         here = request.data.get('here')
# #         where = request.data.get('where')
# #         year = request.data.get('year')
# #         month = request.data.get('month')
# #         day = request.data.get('day')
# #
# #         data = {
# #             "query": {
# #                 "market": "UZ",
# #                 "locale": "en-GB",
# #                 "currency": "UZS",
# #                 "query_legs": [
# #                     {
# #                         "origin_place_id": {"iata": here}, "destination_place_id": {"iata": where},
# #                         "date": {"year": year, "month": month, "day": day}}
# #                 ],
# #                 "adults": 1,
# #                 "cabin_class": "CABIN_CLASS_ECONOMY"
# #             }}
# #         res = result(data)
# #         return Response({'success': True, 'data': res})

# class CityCreateView(generics.GenericAPIView):
#     serializer_class = AirportSerializers
#
#     def post(self, request):
#         file = request.data.get("file")
#         rd = pd.read_excel(f"{file}")
#         df = pd.DataFrame(rd)
#         query = Airport.objects.all()
#         for row in df.itertuples():
#             for i in query:
#                 if row[4] == i.iata_code:
#                     i.city = row[1]
#                     i.city_code = row[2]
#                     i.save()
#             # print(row[4])
#
#             # if len(row[5]) > 2:
#             #     Airport.objects.get_or_create(
#             #         iata_code=row[5],
#             #         name=row[2],
#             #         municipality=row[3],
#             #         continent=row[4],
#             #     )
#         # for row in df.itertuples():
#         #     Airports.objects.get_or_create(
#         #         iata=row.iata,
#         #         name_ru=row.name_ru,
#         #         name_en=row.name_en,
#         #         parent_name_en=row.parent_name_en,
#         #     )
#
#         return Response("Success")
