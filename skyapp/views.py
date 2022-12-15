from decimal import Decimal
import pandas as pd
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from skyapp.models import Airport
from skyapp.serializers import AirportSerializers
from duffel_api import Duffel

client = Duffel(access_token='duffel_test_yMbiVo4D2-niVT27q2XEy87CSMwsWvSE5Uu4YMm9wD7')


class CityCreateView(generics.GenericAPIView):
    serializer_class = AirportSerializers

    def post(self, request):
        file = request.data.get("file")
        rd = pd.read_csv(f"{file}")
        df = pd.DataFrame(rd)
        for row in df.itertuples():
            if len(row[5]) > 2:
                Airport.objects.get_or_create(
                    iata_code=row[5],
                    name=row[2],
                    municipality=row[3],
                    continent=row[4],
                )
        # for row in df.itertuples():
        #     Airports.objects.get_or_create(
        #         iata=row.iata,
        #         name_ru=row.name_ru,
        #         name_en=row.name_en,
        #         parent_name_en=row.parent_name_en,
        #     )

        return Response("Success")


class CitySearchView(generics.ListAPIView):
    serializer_class = AirportSerializers

    def get_queryset(self):
        query = self.request.GET.get("city")
        queryset = Airport.objects.all()
        if query:
            queryset = queryset.filter(continent__icontains=query)
        if len(queryset) < 1:
            queryset = Airport.objects.filter(municipality__icontains=query)
        if len(queryset) < 1:
            queryset = Airport.objects.filter(name__icontains=query)
        return queryset


def transfer(segments, length):
    seg = []
    for i in range(length):
        seg.append(dict(
            destionation_name=segments[i].destination.name,
            iatacode=segments[i].destination.iata_code,
            depart_at=segments[i].departing_at,
            arriving_at=segments[i].arriving_at,
        ))
        # seg[i] = segments[i].destination.name
        # seg[f'Name {i}'] = segments[i].destination.iata_code
        # seg[f'Depart {i}'] = segments[i].departing_at
        # seg[f'Arriving {i}'] = segments[i].arriving_at
    return seg


def passengers(pas, length):
    passenger = []
    for i in range(length):
        passenger.append(pas[i].passenger_id)
    return passenger


def date_time(date):
    data = date[1:]
    a = ''
    for i in data:
        if not i == 'T':
            a = a + i
        if not i.isdigit():
            a = a + ' '
    return (a.lower()).strip()


class TestView(APIView):

    def post(self, request):
        origin = request.data.get("from")
        destination = request.data.get("to")
        depart = request.data.get("date")
        # cabin_class = self.request.data.get('cabin_class')
        res = self.request.data.get('passengers')
        passess = []
        for i in res:
            if int(i) > 12:
                passess.append({'type': 'adult'})
            if int(i) < 2:
                passess.append({'age': 1})
            if int(i) < 12:
                passess.append({'age': int(i)})
        slices = [
            {
                "origin": origin,
                "destination": destination,
                "departure_date": depart,
            },
        ]
        cabin_class = 'economy'
        offer_request = (
            client.offer_requests.create()
            .passengers([{"type": "adult"}])
            .slices(slices)
            .return_offers('true')
            .execute(cabin_class)
        )
        offers = offer_request.offers
        flights = []
        fly_count = 0
        res = None
        for idx, offer in enumerate(offers):
            # print(len(offer.slices[0].segments))
            if len(offer.slices[0].segments) < 2:
                print(offer)
                flights.append(dict(
                    id=offer.id,
                    length=len(offer.slices[0].segments),
                    name=offer.owner.name,
                    amount=float(offer.total_amount) + float(offer.total_amount) / 20,
                    depart=offer.slices[0].segments[0].departing_at,
                    arriving_at=offer.slices[0].segments[0].arriving_at,
                    duration=date_time(offer.slices[0].duration),
                    ketish_airport=str(offer.slices[0].segments[0].origin.name),
                    airport=offer.slices[0].segments[0].destination.name,
                    iata=offer.slices[0].segments[0].origin.iata_code,
                    iata_2=str(offer.slices[0].segments[0].destination.iata_code),
                    class_type=offer.slices[0].segments[0].passengers[0].cabin_class_marketing_name,
                    passenger_id=passengers(offer.slices[0].segments[0].passengers,
                                            len(offer.slices[0].segments[0].passengers)),
                    other=str(offer.slices[0].segments)
                ))
            if len(offer.slices[0].segments) >= 2:
                flights.append(dict(
                    id=offer.id,
                    length=len(offer.slices[0].segments),
                    name=offer.owner.name,
                    amount=float(offer.total_amount) + float(offer.total_amount) / 20,
                    depart=offer.slices[0].segments[0].departing_at,
                    arriving_at=offer.slices[0].segments[-1].arriving_at,
                    duration=date_time(offer.slices[0].duration),
                    airport=offer.slices[0].segments[-1].destination.name,
                    ketish_airport=offer.slices[0].segments[0].origin.name,
                    airport_2=transfer(offer.slices[0].segments, len(offer.slices[0].segments)),
                    iata=offer.slices[0].segments[0].origin.iata_code,
                    iata_2=str(offer.slices[0].segments[0].destination.iata_code),
                    class_type=offer.slices[0].segments[0].passengers[0].cabin_class_marketing_name,
                    passenger_id=passengers(offer.slices[0].segments[0].passengers,
                                            len(offer.slices[0].segments[0].passengers)),
                    other=str(offer.slices[0].segments)
                ))
            # res = transfer(offer.slices[0].segments, len(offer.slices[0].segments))
            fly_count += 1
            # f"{idx + 1}. {offer.owner.name} flight departing at "
            # + f"{offer.slices[0].segments[0].departing_at} "
            # + f"{offer.total_amount} {offer.total_currency}"
            # )
        return Response({
            'msg': "Success",
            "count": str(fly_count),
            'list': flights,
            'passengers': passess,
            'offer_request_id': offer_request.id
        }, status=status.HTTP_200_OK)


class TestRoundTripView(APIView):

    def post(self, request):
        origin = request.data.get("from")
        destination = request.data.get("to")
        depart = request.data.get("date")
        slices = [
            {
                "origin": "TAS",
                "destination": "NYC",
                "departure_date": "2022-12-26"
            },
            {
                "origin": "NYC",
                "destination": "MOW",
                "departure_date": "2023-01-26"
            },
            {
                "origin": "MOW",
                "destination": "TAS",
                "departure_date": "2023-01-30"
            }
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
            print(len(offer.slices))
        return Response({
            'msg': "Success",
            "count": str(fly_count),
            'list': flights,
            'offer_request_id': offer_request.id
        }, status=status.HTTP_200_OK)


class SeatMapAPIView(APIView):
    def post(self, request):
        selected_offer_id = self.request.data.get('id')
        priced_offer = client.offers.get(selected_offer_id)
        seat_maps = client.seat_maps.get(priced_offer.id)
        print(seat_maps)
        available_seats = []
        print(client.seat_maps.get(selected_offer_id))
        for _idx, row in enumerate(seat_maps[0].cabins[0].rows):
            for _idx, section in enumerate(row.sections):
                for _idx, element in enumerate(section.elements):
                    if (
                            element.type == "seat"
                            and element.available_services is not None
                            and len(element.available_services) > 0
                    ):
                        available_seats.append(element)
                    # else:
                    #     return Response({'message': "Available seats aren't found"}, status=status.HTTP_404_NOT_FOUND)
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
        # print(res.id)
        # print(res.client_token)
        payment_intent_id = res.id
        client_token = res.client_token
        # print(res)
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
        passess = self.request.data.get('passengers')
        offers = client.offer_requests.get(id=offer_id)
        infant = None
        if 1 in list(passess):
            infant = passess.index(1)
        res = []
        for i in list(pas):
            if i == 0 and infant:
                res.append(dict(
                    born_on=i.born_on,
                    email=i.email,
                    family_name=i.family_name,
                    gender=i.gender,
                    given_name=i.given_name,
                    id=offers.passengers[i].id,
                    infant_passenger_id=offers.passengers[infant].id,
                    phone_number=i.phone_number,
                    title=i.title
                ))
            else:
                res.append(dict(
                    born_on=i.born_on,
                    email=i.email,
                    family_name=i.family_name,
                    gender=i.gender,
                    given_name=i.given_name,
                    id=offers.passengers[i].id,
                    phone_number=i.phone_number,
                    title=i.title
                ))
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
            .passengers(res)
            .execute()

        )
        return Response(order)

# {
# "from":"TAS",
# "to":"MOW",
# "date":"2022-12-25",
# "passengers":[15]
# }
