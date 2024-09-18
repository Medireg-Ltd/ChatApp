from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate


class AccountsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
