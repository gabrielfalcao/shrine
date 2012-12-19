import dj_database_url
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PRODUCTION = not DEBUG

ADMINS = (
    (u'Your Name', 'your@email.com'),
)

MANAGERS = ADMINS
PRODUCT_NAME = '{shrine_name}'
APP_EMAIL_ADDRESS = 'emailer@{shrine_name}.herokuapp.com'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite://./shrine.sqlite')}

TEMPLATE_PATH = './templates'
STATIC_PATH = './media'

MAILGUN_ACCESS_KEY = 'your-mailgun-key'
MAILGUN_SERVER_NAME = 'your-mailgun-server-name'

AUTHENTICATED_HOME = '/admin'

if PRODUCTION:
    EMAIL_BACKEND = 'shrine.mailgun.EmailBackend'
