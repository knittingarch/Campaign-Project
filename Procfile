#web: waitress-serve --call --port=$PORT campaign.wsgi:application
web: gunicorn campaign.wsgi
#web: waitress-serve --call --port=$PORT django.core.wsgi:get_wsgi_application
