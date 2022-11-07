import pandas as pd
import json
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from skyapp.models import Airports
from skyapp.serializers import AirportSerializer
from translate import to_latin
from .utils import result
from duffel_api import Duffel

duffel = Duffel(access_token='duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7')


class CityCreateView(generics.GenericAPIView):
    serializer_class = AirportSerializer

    def post(self, request):
        file = request.data.get("file")
        rd = pd.read_csv(f"{file}")
        df = pd.DataFrame(rd)

        # for row in df.itertuples():
        #     Airports.objects.get_or_create(
        #         iata=row.iata,
        #         name_ru=row.name_ru,
        #         name_en=row.name_en,
        #         parent_name_en=row.parent_name_en,
        #     )

        # with open('airport_2.csv', encoding="utf8") as f:
        #     reader = csv.reader(f)
        #
        #     new_row = []
        #     reader = list(reader)
        #     # print(
        #     #     type(reader)
        #     # )
        #     print(reader[2])
        #     print(reader[2][2])
        #     for i in range(10):
        #         print(reader[i][2])
        # for row in reader:
        #     # print(row[0])
        #     print((row))
        # for r in row:
        # r.strip('""')
        # r = r.replace('""', '')
        # r.replace(' ', '')
        # new_row.append(r)
        # print(r[0])
        # print(new_row)
        # for i in new_row:
        #
        #     print(i[0])

        return Response("Success")


class CitySearchView(generics.ListAPIView):
    serializer_class = AirportSerializer

    def get_queryset(self):
        query = self.request.GET.get("city")
        city = to_latin(query)
        queryset = Airports.objects.all()
        if city:
            queryset = queryset.filter(name_en__istartswith=city).order_by('name_en')
            # queryset = queryset.extra(where=["%s LIKE name_en||'%%'"], params=[city])
        return queryset


class FindTicket(APIView):

    def post(self, request):
        here = request.data.get('here')
        where = request.data.get('where')
        year = request.data.get('year')
        month = request.data.get('month')
        day = request.data.get('day')

        data = {
            "query": {
                "market": "UZ",
                "locale": "en-GB",
                "currency": "UZS",
                "query_legs": [
                    {
                        "origin_place_id": {"iata": here}, "destination_place_id": {"iata": where},
                        "date": {"year": year, "month": month, "day": day}}
                ],
                "adults": 1,
                "cabin_class": "CABIN_CLASS_ECONOMY"
            }}
        res = result(data)
        return Response({'success': True, 'data': res})


class TestView(APIView):

    def post(self, request):
        client = Duffel(access_token='duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7')
        origin = request.data.get("from")
        destination = request.data.get("to")
        depart = request.data.get("date")
        slices = [
            {
                "origin": origin,
                "destination": destination,
                "departure_date": depart,
            },
        ]
        offer_request = (
            client.offer_requests.create()
            .passengers([{"type": "adult"}])
            .slices(slices)
            .return_offers()
            .execute()
        )
        print(f"Created offer request: {offer_request.id}")

        offers = client.offers.list(offer_request.id)
        offers_list = list(enumerate(offers))

        print(f"Got {len(offers_list)} offers")

        selected_offer = offers_list[0][1]

        # print(f"Selected offer {selected_offer.id} to book")

        priced_offer = client.offers.get(selected_offer.id)

        # print(
        #     f"The final price for offer {priced_offer.id} is {priced_offer.total_amount} ({priced_offer.total_currency})"
        # )

        seat_maps = client.seat_maps.get(priced_offer.id)

        available_seats = []
        for _idx, row in enumerate(seat_maps[0].cabins[0].rows):
            for _idx, section in enumerate(row.sections):
                for _idx, element in enumerate(section.elements):
                    if (
                            element.type == "seat"
                            and element.available_services is not None
                            and len(element.available_services) > 0
                    ):
                        available_seats.append(element)

        available_seat = available_seats[0]
        print(available_seat)
        available_seat_service = available_seat.available_services[0]

        return Response("Zo'r")
        # offers = offer_request.offers
        # flights = []
        # fly_count = 0
        # for idx, offer in enumerate(offers):
        #     abc = offer.slices
        #     for i, o in enumerate(abc):
        #         print(o.segments)
        #     flights.append(dict(
        #         id=offer.id,
        #         name=offer.owner.name,
        #         amount=float(offer.total_amount) + float(offer.total_amount) / 20,
        #         depart=offer.slices[0].segments[0].departing_at,
        #         duration=offer.slices[0].duration,
        #         airport=offer.slices[0].segments[0].destination.name,
        #         iata=offer.slices[0].segments[0].origin.iata_code,
        #         class_type=offer.slices[0].segments[0].passengers[0].cabin_class_marketing_name,
        #         other=str(offer.slices[0])
        #     ))
        #     fly_count += 1
        #     # f"{idx + 1}. {offer.owner.name} flight departing at "
        #     # + f"{offer.slices[0].segments[0].departing_at} "
        #     # + f"{offer.total_amount} {offer.total_currency}"
        #     # )
        # return Response(flights)
        # return Response(flights)
        # Response({
        #     'msg': "Success",
        #     'list': flights
        # }, status=status.HTTP_200_OK)

# {
# "from":"TAS",
# "to":"IST",
# "date":"2022-11-11"
# }
