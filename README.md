# Django 101 - Project "quote generator"

In the first workshop, we got everyone up to par with their environments, we chose a project to work on (a quotes 
generator), and we started building our project.

Here are the [slides that were used during the workshop](http://slides.com/canweb/django-101/#/).

## Step 1 - Making the environment ready

We need to install Python3 and pipenv, as well as an IDE of our choice. For the purpose of this workshop, I used 
PyCharm, but Atom, Sublime Text 3, Eclipse or even Vim can do the job. In the end, it's a question of preference.

### For MacOS X
```
/usr/bin/ruby -e \
   "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
pip3 install --user pipenv
```

### For Linux
```
sudo apt install python3 python3-pip python3-dev rake ruby-dev
pip3 install --upgrade pip
pip3 install --user pipenv
```

## Step 2 - Start the project

A Django application is composed of a "project", as well as one or multiple "applications".

From [Django's website](https://docs.djangoproject.com/en/2.0/intro/tutorial01/):

> In Django, a "project" is a collection of settings for an instance of Django, including database configuration, 
> Django-specific options and application-specific settings.
> 
> An "application" consists of a Python package that follows a certain convention. Django comes with a utility that 
> automatically generates the basic directory structure of an app, so you can focus on writing code rather than creating
> directories.
> 
> What’s the difference between a project and an app? An app is a Web application that does something – e.g., a Weblog 
> system, a database of public records or a simple poll app. A project is a collection of configuration and apps for a 
> particular website. A project can contain multiple apps. An app can be in multiple projects.

Let's start an empty project and run it :

```
cd ~/projects
mkdir django101                          # This is the root directory
cd django101
pipenv install Django                    # Creates the pipenv environment
pipenv shell                             # Activates the pipenv environment
django-admin startproject django101      # Starts the project
cd django101                             # - which creates a dir. in your root dir.
./manage.py migrate                      # Adds the base tables in your database
./manage.py runserver                    # Starts a development server
```

At this point, if you go to [http://127.0.0.1:8000](http://127.0.0.1:8000), you should see a nifty little rocket!

To stop your development server, you just have to hit ```CONTROL-C``` on your keyboard.

## Step 3 - Start the "quoter" app

Now that we have our project started, let's create our first app: "quoter":

```
./manage.py startapp quoter
```

This will create a directory named "quoter", which will contain the basic files your app needs to function within your 
project.

In order for your project to use this app, you will need to register it in your settings. In 
```django101/django101/settings.py```, you need to add it to INSTALLED_APPS:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quoter', # YOU NEED TO ADD THIS
]
```

## Step 4 - Create your models

I usually like to start my apps by defining the data models they're going to need.  I find it's a good way to structure 
your understanding of the application you're developing.

In the first part of the workshop, we had time to define the Author, Category and Quote models.  Once we created them,
we created migrations for them, and executed the migrations, which created a table in our database for each 
corresponding model:

```
./manage.py makemigrations
./manage.py migrate
```

One of the most useful features of Django is it's automagically generated admin panel, in which you can list, create, 
edit or delete instances of your models from the database.  To enable this feature for each of your models, you need to
add them to the ```admin.py``` file in your quoter app:

```
from .models import Quote, Author, Category

admin.site.register(Quote)
admin.site.register(Author)
admin.site.register(Category)
```

And that's pretty much where we were at at the end of the first workshop.  I'll commit this on the project's GitHub 
repository and tag it "workshop-1".

## Step 5 - Creating the views, URL schemes and template

The first thing we need to do is to create the views.  One thing that's great with Django is its class-based views.

In Django, views can be functions in which, for instance, data is retrieved from the database and passed along to a 
specified template.

They can also be a class, which means they can inherit behaviors from a lot of "generic" views which are provided with
Django, and implement a default behavior for a lot of common use cases, such as :

- TemplateView, which associates a specified template to the view
- ListView, which lists instances of a specified model
- DetailView, which shows the details of a single model instance
- CreateView, UpdateView and DeleteView, which allow to create, edit and delete a single model instance, respectively
- etc.

For the purpose of this tutorial, we'll be using a modified ListView, to which we will give a random Quote model 
instance to display.  The reason why we use a ListView instead of a DetailView is that a DetailView needs a reference
to a single model instance, but we're not providing one as we are selecting a model instance randomly.

```
# quoter/views.py
from django.views.generic import ListView
from .models import Quote


class QuoteView(ListView):
    model = Quote  # This defines the model associated with this view
    template_name = 'random_quote.html'  # This defines the template associated with this view

    def get_queryset(self):
        # This is a "mixin", a method defined in the generic view ListView (or one of its ancestors)
        return Quote.objects.order_by('?').first()  # This returns a random quote in the queryset

```

Then we create an URL scheme in our quoter app:

```
# quoter/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.QuoteView.as_view()),
]
```

And we add a reference to this app urls file in our project urls file:

```
# django101/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('quoter/', include('quoter.urls')),  # Add this line
    path('admin/', admin.site.urls),
]

```

Finally, we create a template which will display the quote:

```
<!-- quoter/templates/random_quote.html -->
<figure>
    <blockquote>
        {{ object_list.quote }}
    </blockquote>
    <figcaption>{{ object_list.author }}</figcaption>
</figure>
```

That's it! You have a functional random quote generator.  Celebrate!

## Step 6 - Refactor the template with some beauty

Of course, we want our page to be not just functional, but beautiful.  In order to do that, we can use a base template,
which will contain the general layout of the application's pages, and then extend that template in our random_quote.html
template.

```
<!-- quoter/templates/_base.html -->
<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" 
          crossorigin="anonymous">

    <title>Quoter App</title>
</head>
<body class="text-center">
    {% block page_content %}
    {% endblock %}

    <script src="//code.jquery.com/jquery-3.2.1.slim.min.js"
            integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
</body>
</html>
```

In the base template above, the block identified with {% block page_content %}{% endblock %} is the part which will be
extended in the random quote template:

```
{% extends "_base.html" %}

<!-- quoter/templates/random_quote.html -->
{% block page_content %}
<div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
    <header class="masthead mb-auto"></header>
    <main role="main" class="inner cover">
          <h1 class="cover-heading">{{ object_list.quote }}</h1>
          <p class="lead">&ndash; {{ object_list.author }}</p>
    </main>
    <footer class="mastfoot mt-auto"></footer>
</div>
{% endblock %}
```

And voilà!  A much more interesting visual proposition for our random quote page. I've added a bit more custom CSS in
the Github repository, you can check it out!

## Step 7 - Let's use a quote generating API to populate our database... muah ah ah...

Now that our quotes are displayed nicely, we could use an outside source to add quotes to our database. The way I'm
proposing to do this is to modify our view so that it either randomly selects a quote from our database, OR it selects
a quote from an outside source, adds it to our database, and displays it.

Here is how I propose to do that:

```
# quoter/views.py

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

```

Then, we need to modify our model to make the author's birthdate nullable:

```
# quoter/models.py

class Author(models.Model):
    name = models.CharField(max_length=150)
    birthdate = models.DateField(null=True)  # null=True has been added

    def __str__(self):
        return self.name

```

And there you have it!
