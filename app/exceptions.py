class AppException(Exception):
    """Base domain exception. All service-layer errors inherit from this."""

    def __init__(self, detail: str = "An application error occurred") -> None:
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail)


class ConflictError(AppException):
    """Raised on duplicate resources, insufficient stock, or invalid state transitions."""

    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(detail)


class BadRequestError(AppException):
    """Raised when the request is semantically invalid (e.g. duplicate product IDs)."""

    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(detail)


class ForbiddenError(AppException):
    """Raised when the user lacks permission (e.g. accessing another user's order)."""

    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(detail)


class AuthenticationError(AppException):
    """Raised when credentials are invalid."""

    def __init__(self, detail: str = "Incorrect email or password") -> None:
        super().__init__(detail)
