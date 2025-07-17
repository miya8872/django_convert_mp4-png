from django.apps import AppConfig
import threading

class AfterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'after'

    def ready(self):#runserver時に起動
        from .remove import start,reset
        threading.Thread(target=reset).start()
        start()
