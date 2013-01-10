# Shrine
0.0.7
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

![https://raw.github.com/gabrielfalcao/shrine/master/console.png?login=gabrielfalcao&token=b80fdab4fbebb1a02f5e56154fc50095](https://raw.github.com/gabrielfalcao/shrine/master/console.png?login=gabrielfalcao&token=b80fdab4fbebb1a02f5e56154fc50095)

### will become this

![https://raw.github.com/gabrielfalcao/shrine/master/web.png?login=gabrielfalcao&token=588e5f10c88e637c5918a9499306c0ea](https://raw.github.com/gabrielfalcao/shrine/master/web.png?login=gabrielfalcao&token=588e5f10c88e637c5918a9499306c0ea)

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
