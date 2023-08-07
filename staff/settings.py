from base.settings import *

ROOT_URLCONF = "staff.urls"

WSGI_APPLICATION = "staff.wsgi.application"

# ---------------------------------------------------------------------------- #
#                                 SWAGGER                                      #
# ---------------------------------------------------------------------------- #
SPECTACULAR_SETTINGS["TITLE"] = "Staff Api"

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "base.auth.permissions.permission.IsStaff"
]
