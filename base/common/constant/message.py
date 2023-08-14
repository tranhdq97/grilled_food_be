from django.utils.translation import gettext_lazy as _

# Authentication
MUST_HAVE_EMAIL = _("User must have an email address.")
PASSWORD_FAILED = _("At least one uppercase letter, one lowercase letter, one number")
PASSWORD_IDENTICAL_AS_EMAIL = _("The same string sequence as the email address")
PASSWORD_DID_NOT_MATCH = _("Dont match current password. Please check again")
PASSWORD_CHANGE_SUCCESSFUL = _("Change password successfully")
ALREADY_HAVE_SUPER_STAFF = _("Already have the super staff")
EMAIL_OR_PASSWORD_IS_INCORRECT = _("The email address or password is incorrect")
INVALID_TOKEN = _("Invalid token")

# Permission
PERMISSION_DENIED = "permission denied"

# Query database
NOT_EXIST = _("Does not exist")
NO_SERIALIZER_MATCHED = _("There is no serializer matched with this action")
DUPLICATE_ENTRY = _("Duplicate entry")
INVALID_INPUT = "Invalid input"
ALREADY_EXISTS = "Already exists"

# Master
NOT_ALLOWED_TO_CREATE = _("This master is not allowed to create.")

# Order
QUANTITY_IS_ZERO = _("You're trying to order 0 %(name)s. Please change your order.")

# Other
PASSWORD_INAPPROPRIATE = _(
    "Password must contain at least 7 letters, one digit, one lowercase letter, one uppercase letter"
)
PASSWORD_MUST_DIFFER_EMAIL = _("Password must differ email address")
NOT_AVAILABLE = _("Not available")
