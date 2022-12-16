from django.urls import path
from skyapp.views import CitySearchView, TestView
from . import views

urlpatterns = [
    # path('test/', CityCreateView.as_view()),
    path('search/', CitySearchView.as_view()),
    path('ticket/', TestView.as_view()),
    path('round-trip/', views.TestRoundTripView.as_view()),
    path('seat-map/', views.SeatMapAPIView.as_view()),
    path('choice/', views.ChoiceSeatAPIView.as_view()),
    path('order/', views.OrderAPIView.as_view())
    # path('success-url/', freedom.SuccessUrl.as_view())
]
