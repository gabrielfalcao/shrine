# {shrine_name}

Welcome to your awesome web project {shrine_name}.

It comes with these cool things out of the box:
 * Heroku hosting
 * [Tornado](http://www.tornadoweb.org/) HTTP server
 * Session support
 * [Postgres-backed](https://addons.heroku.com/heroku-postgresql) [django models](https://docs.djangoproject.com/en/1.4/topics/db/models/) access from the controllers.
 * [South](http://south.aeracode.org/) migrations compatible
 * [Flask-like](http://flask.pocoo.org/docs/api/#url-route-registrations) routes
 * Python helpers for fluent test writing
  * [A HTTP request mocking tool](https://github.com/gabrielfalcao/HTTPretty)
  * [A fluent assertion library](https://github.com/gabrielfalcao/sure)
  * [Behavior-driven development tool](https://github.com/gabrielfalcao/lettuce)
 * [Twitter Bootstrap](http://twitter.github.com/bootstrap/) basic templates for using right away

## Step 1: Installing the components

```shell
pip install -r requirements.pip
```

## Step 2: Running

You can run this website with the command:

```shell
shrine run
```

## Step 3: Deploy to Heroku

Shrine works with Heroku out of the box.

The files `Procfile` and `requirements.pip` are already in the current
folder, so the [python buildpack](https://github.com/heroku/heroku-buildpack-python) will leverage all the hard work.

### Make sure you are wearing the toolbelt

You will find the toolbelt here: [https://toolbelt.heroku.com/](https://toolbelt.heroku.com/).

Make sure you install and configure it, here is the
[documentation of python](https://devcenter.heroku.com/articles/python)-powered
apps in heroku in case you need.

### Create and deploy the code

```shell
heroru create {shrine_name}
git push -u heroku master
```

### Add ons? Sure!

[Shrine](http://github.com/gabrielfalcao/shrine) has support to a few heroku add ons:

#### Postgres

Ready to go!

#### Mailgun

Edit your `settings.py` file and add:
```shell
MAILGUN_ACCESS_KEY = 'your-mailgun-key'
MAILGUN_SERVER_NAME = 'your-mailgun-server-name'

if PRODUCTION:
    EMAIL_BACKEND = 'shrine.mailgun.EmailBackend'

```

# Credits

{shrine_name} was made using [Shrine Web Framework](http://github.com/gabrielfalcao/shrine)
