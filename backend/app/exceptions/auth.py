from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )

class InactiveUserException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Inactive user',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )

class NotSuperuserException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You do not have permission to perform this action',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )

class UserNotFoundException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )

class UserAlreadyExistsException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User already exists',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )

class UserNotExistsException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User does not exist',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )
