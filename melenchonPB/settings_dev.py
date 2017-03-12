import os
DEBUG = bool(os.environ.get('DEBUG', True))
CALLHUB_API_KEY=os.environ.get('CALLHUB_API_KEY','b23384fd45686c6b4e5603ad261400a063f748e5')
SECRET_KEY = os.environ.get('SECRET_KEY','lolilolilol')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','127.0.0.1 localhost ngrok.io').split()
SESSION_COOKIE_SECURE = bool(os.environ.get('SESSION_COOKIE_SECURE', False))
SECURE_BROWSER_XSS_FILTER = bool(os.environ.get('SECURE_BROWSER_XSS_FILTER', False))
SECURE_CONTENT_TYPE_NOSNIFF = bool(os.environ.get('SECURE_CONTENT_TYPE_NOSNIFF', False))
CSRF_COOKIE_SECURE = bool(os.environ.get('CSRF_COOKIE_SECURE', False))
CSRF_COOKIE_HTTPONLY = bool(os.environ.get('CSRF_COOKIE_HTTPONLY', False))
X_FRAME_OPTIONS = bool(os.environ.get('X_FRAME_OPTIONS', False))

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "callcenter.routing.channel_routing",
    },
}
