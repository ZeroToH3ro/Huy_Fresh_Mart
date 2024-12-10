
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Huy_Fresh_Mart.settings')

application = get_wsgi_application()
