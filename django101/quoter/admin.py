from django.contrib import admin

# Register your models here.
from .models import Quote, Author, Category

admin.site.register(Quote)
admin.site.register(Author)
admin.site.register(Category)

