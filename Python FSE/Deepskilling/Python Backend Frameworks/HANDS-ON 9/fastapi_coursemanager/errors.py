"""
HANDS-ON 8 - Task 2, step 85: standardised error response format.

All errors returned by this API follow:
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Course with id 99 does not exist",
        "field": null
    }
}
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError


def error_body(code: str, message: str, field: str | None = None):
    return {'error': {'code': code, 'message': message, 'field': field}}


async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        404: 'NOT_FOUND',
        409: 'CONFLICT',
        422: 'UNPROCESSABLE_ENTITY',
    }
    code = code_map.get(exc.status_code, 'ERROR')
    return JSONResponse(status_code=exc.status_code, content=error_body(code, str(exc.detail)))


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    field = '.'.join(str(p) for p in first.get('loc', [])) or None
    message = first.get('msg', 'Validation error')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_body('VALIDATION_ERROR', message, field),
    )
