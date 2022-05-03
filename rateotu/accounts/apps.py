from django.apps import AppConfig


class AccountsAppConfig(AppConfig):
    name = "rateotu.accounts"
    verbose_name = "Accounts"

    def ready(self):
        try:
            from rateotu.accounts import signals  # noqa F401
        except ImportError:
            pass
