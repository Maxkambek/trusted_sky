from django.urls import path
from skyapp.views import CityCreateView, CitySearchView, FindTicket, TestView

urlpatterns = [
    # path('test/', CityCreateView.as_view()),
    # path('search/', CitySearchView.as_view()),
    # path('find-ticket/', FindTicket.as_view()),
    path('test1/', TestView.as_view())

]
