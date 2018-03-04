from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.QuoteView.as_view(), name='random-quote'),
]
