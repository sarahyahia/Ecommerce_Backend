from django.urls import path
from .views import checkout, OrdersList


urlpatterns = [
    path('checkout', checkout),
    path('myorders', OrdersList.as_view()),
]