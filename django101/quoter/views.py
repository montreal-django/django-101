import json
import urllib
import html
from random import choice
from django.views.generic import ListView
from .models import Author, Category, Quote


class QuoteView(ListView):
    model = Quote
    template_name = 'random_quote.html'

    def get_queryset(self):
        if choice([True, False]) is True:
            return Quote.objects.order_by('?').first()

        with urllib.request.urlopen("http://quotesondesign.com/wp-json/posts?filter[orderby]=rand") as url:
            data = json.loads(url.read().decode())

            category, created = Category.objects.get_or_create(
                name='Quote from quotesondesign.com'
            )

            author, created = Author.objects.get_or_create(
                name=data[0]['title']
            )

            quote, created = Quote.objects.get_or_create(
                quote=html.unescape(data[0]['content'].replace('<p>', '').replace('</p>', '')),
                defaults={'author': author, 'category': category}
            )

            return quote
