* shrine create will generate:

* `settings.py`
* `controllers/index.py`
* `manage.py` (for migrations, etc)
* `requirements.txt`
* `Procfile`
* `.gitignore`

* shrine run in the current directory runs the server

* use Model.objects.all().query in a context manager or callback-based function that runs asynchronously through Tornado's mysql async client:

```python
with controller.db.query(Model).objects.all() as queryset:
    # ... do stuff with queryset that was evaluated asynchronously


# or ...

def process_users(controller, queryset, age):
    controller.response.render('template.html', context=dict(users=queryset))


@get('/users/age/(\d+)')
def list_users(controller, age):
    controller.db.query(Model).objects.all().passing(age).to(process_users)
```


* defining controllers:

`@controllers/foo.py`:

```python
from shrine import get, post

@get('/process/(?P<name>\w+)')
def process_user(controller, name):
    with controller.db.persist(User, name=name) as user:
        controller.render('user-saved.html', dict(user=user))

# or ...

def persist_user(controller, user):
    controller.render('user-saved.html', dict(user=user))

@get('/process/(?P<name>\w+)')
def process_user(controller, name):
    controller.db.persist(User, name=name).to(persist_user)

```

## Add controllers as python files under `./controllers/`

They will be found automatically

Example `controllers/friends.py`


```python
from shrine import get
from django.contrib.auth.models import User

@get('/profile')
def render_my_profile(controller):
    with controller.db.query(User, username=controller.session['username']) as me:
        controller.render('admin/profile.html', dict(me=me))
```
