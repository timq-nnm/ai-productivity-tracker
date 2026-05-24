from fastapi import FastAPI

from core.exceptions.users_exceptions import UserNotFoundError, UserAlreadyExsist

from core.handlers.users_handlers import user_not_found_handler, user_already_exist_handler


def register_exception_handlers(app: FastAPI):
    """Register custom exception handlers."""
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExsist, user_already_exist_handler)
