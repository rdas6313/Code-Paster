from rest_framework.views import exception_handler as super_exception_handler
from rest_framework.exceptions import ErrorDetail


def exception_handler(exc, context):
    """ custom exception handler to change error response messages """
    response = super_exception_handler(exc, context)
    if not response:
        return response
    res = {}
    for field, errors in response.data.items():
        errors = [errors] if field == 'detail' else errors

        res[field] = [
            {
                'message': str(error),
                'code': error.code if isinstance(error, ErrorDetail) else None
            }
            for error in errors
        ]
        if field == 'detail':
            break

    response.data = {'errors': res}

    return response
