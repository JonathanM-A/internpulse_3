from .settings import *
from .settings import env

SECRET_KEY = env(
    "TEST_SECRET_KEY", default="s1*du$i#bw&2_shl7v!e1%naw38g5(z!h-f@q*n)g-j8@!^&i2"
)

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# DATABASES = {
#     "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
# }

# DEBUG = False
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
