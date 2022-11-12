import json
from decimal import Decimal
import pandas as pd
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from skyapp.models import Airports
from skyapp.serializers import AirportSerializer
from translate import to_latin
from duffel_api import Duffel

client = Duffel(access_token='duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7')


class CityCreateView(generics.GenericAPIView):
    serializer_class = AirportSerializer

    def post(self, request):
        file = request.data.get("file")
        rd = pd.read_csv(f"{file}")
        df = pd.DataFrame(rd)

        for row in df.itertuples():
            Airports.objects.get_or_create(
                iata=row.iata,
                name_ru=row.name_ru,
                name_en=row.name_en,
                parent_name_en=row.parent_name_en,
            )

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


class TestView(APIView):

    def post(self, request):
        # origin = request.data.get("from")
        # destination = request.data.get("to")
        # depart = request.data.get("date")
        # cabin_class = self.request.data.get('cabin_class')
        # res = self.request.data.get('passengers')
        # passengers = []
        # for i in res:
        #     if int(i) > 12:
        #         passengers.append({'type': 'adult'})
        #     if int(i) < 12:
        #         passengers.append({'age': int(i)})
        slices = [
            {
                "origin": "TAS",
                "destination": "UGC",
                "departure_date": "2022-12-12",
            },
        ]
        cabin_class = 'economy'
        offer_request = (
            client.offer_requests.create()
            .passengers([{"type": "adult"}])
            .slices(slices)
            .return_offers()
            .execute(cabin_class)
        )
        offers = offer_request.offers
        flights = []
        fly_count = 0
        for idx, offer in enumerate(offers):
            flights.append(dict(
                id=offer.id,
                name=offer.owner.name,
                amount=float(offer.total_amount),  # + float(offer.total_amount) / 20,
                depart=offer.slices[0].segments[0].departing_at,
                duration=offer.slices[0].duration,
                airport=offer.slices[0].segments[0].destination.name,
                iata=offer.slices[0].segments[0].origin.iata_code,
                class_type=offer.slices[0].segments[0].passengers[0].cabin_class_marketing_name,
                other=str(offer.slices[0])
            ))
            fly_count += 1
            # f"{idx + 1}. {offer.owner.name} flight departing at "
            # + f"{offer.slices[0].segments[0].departing_at} "
            # + f"{offer.total_amount} {offer.total_currency}"
            # )
        return Response({
            'msg': "Success",
            "count": str(fly_count),
            'list': flights
        }, status=status.HTTP_200_OK)


class SeatMapAPIView(APIView):
    def post(self, request):
        selected_offer_id = self.request.data.get('id')
        priced_offer = client.offers.get(selected_offer_id)
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
                    else:
                        return Response({'message': "Available seats aren't found"}, status=status.HTTP_404_NOT_FOUND)
        seats = []
        for i, row in enumerate(available_seats):
            seats.append(dict(
                seat=row.designator,
                id=row.available_services[0].id,
                passenger_id=row.available_services[0].passenger_id,
                total_amount=row.available_services[0].total_amount,
                total_currency=row.available_services[0].total_currency
            ))
        return Response({'data': seats})


class ChoiceSeatAPIView(APIView):
    def post(self, request):
        selected_offer_id = self.request.data.get("id")
        seat_amount = self.request.data.get('amount')
        priced_offer = client.offers.get(selected_offer_id)
        total_amount = str(
            Decimal(priced_offer.total_amount)
            + Decimal(float(seat_amount))
        )
        res = (
            client.payment_intents.create()
            .payment({
                "amount": total_amount,
                "currency": "USD"
            })
            .execute()
        )
        payment_intent_id = res['data']['id']
        client_token = res['data']['client_token']

        return Response({
            'payment_intent_id': payment_intent_id,
            'client_token': client_token,
            'total_amount': total_amount
        }, status=status.HTTP_200_OK)


class OrderAPIView(APIView):
    def post(self, request):
        payment_intent_id = self.request.data.get('payment_intent_id')
        selected_offer_id = self.request.data.get('id')
        total_amount = self.request.data.get('total_amount')
        client.payment_intents.confirm(payment_intent_id)
        pas = self.request.data.get('passengers')
        offer_id = self.request.data.get('offer_id')
        offers = client.offer_requests.get(id=offer_id)
        pas = list(pas)
        n = 0
        for i in pas:
            i['id'] = offers.passengers[n].id
            try:
                infant_passenger_id = offers.passengers[n + 1].id
                i['infant_passenger_id'] = infant_passenger_id
            except:
                pass
            n = n + 1

        order = (
            client.orders.create()
            .selected_offers([selected_offer_id])
            .payments([
                {
                    "type": "balance",
                    "amount": total_amount,
                    "currency": "USD"
                }
            ])
            .metadata({
                "payment_intent_id": payment_intent_id
            })
            .passengers(pas)
            .execute()

        )
        return Response(order)
