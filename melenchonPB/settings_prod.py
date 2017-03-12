import os
DEBUG = bool(os.environ['DEBUG'])
CALLHUB_API_KEY=os.environ['CALLHUB_API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()
SESSION_COOKIE_SECURE = bool(os.environ['SESSION_COOKIE_SECURE'])
SECURE_BROWSER_XSS_FILTER = bool(os.environ['SECURE_BROWSER_XSS_FILTER'])
SECURE_CONTENT_TYPE_NOSNIFF = bool(os.environ['SECURE_CONTENT_TYPE_NOSNIFF'])
CSRF_COOKIE_SECURE = bool(os.environ['CSRF_COOKIE_SECURE'])
CSRF_COOKIE_HTTPONLY = bool(os.environ['CSRF_COOKIE_HTTPONLY'])
X_FRAME_OPTIONS = os.environ['X_FRAME_OPTIONS']

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "callcenter.routing.channel_routing",
    },
}
