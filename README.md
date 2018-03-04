# Django 101 - Project "quote generator"

In the first workshop, we got everyone up to par with their environments, we chose a project to work on (a quotes 
generator), and we started building our project.

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