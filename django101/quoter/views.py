from django.views.generic import ListView
from .models import Quote


class QuoteView(ListView):
    model = Quote
    template_name = 'random_quote.html'

    def get_queryset(self):
        return Quote.objects.order_by('?').first()
