from flask import jsonify


class AppError(Exception):
    status_code = 500


class DatabaseError(AppError):
    pass


class ValidationError(AppError):
    pass


class TaskError(AppError):
    pass


class BadRequestError(AppError):
    status_code = 400


class UnauthorizedError(AppError):
    status_code = 401


class ForbiddenError(AppError):
    status_code = 403


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class UnprocessableEntityError(AppError):
    status_code = 422


def handle_app_error(error: AppError):
    response = jsonify({'message': str(error)})
    response.status_code = error.status_code

    return response


ERROR_HANDLERS = {
    AppError: handle_app_error,
    DatabaseError: handle_app_error,
    ValidationError: handle_app_error,
    BadRequestError: handle_app_error,
    UnauthorizedError: handle_app_error,
    ForbiddenError: handle_app_error,
    NotFoundError: handle_app_error,
    ConflictError: handle_app_error,
}
