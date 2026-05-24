from .base import AppException

class UserNotFoundError(AppException):
    pass

class UserAlreadyExsist(AppException):
    pass
