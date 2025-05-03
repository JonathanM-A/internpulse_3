from .base import *  # noqa


def strip_quotes(value):
    if isinstance(value, str):
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            return value[1:-1]
    return value


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": strip_quotes(env("DB_NAME")),
        "USER": strip_quotes(env("DB_USER")),
        "PASSWORD": strip_quotes(env("DB_PASSWORD")),
        "HOST": strip_quotes(env("DB_HOST")),  # Uses the Docker service name
        "PORT": env.int("DB_PORT"),
    }
}
