class RegistrationError(Exception):
    """Raised when a registration fails."""

    pass


class LoginError(Exception):
    """Raised when a login fails."""

    pass


class MongoException(Exception):
    """Raised when a mongo operation fails."""

    pass
