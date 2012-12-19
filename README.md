# Shrime

Tornado + Django

Leverages Heroku deployment + mailgun support and asynchronous query
of Django models.

## install

```bash
pip install shrine
```

## create a project

```bash
shrine create FriendList
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
