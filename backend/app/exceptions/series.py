from fastapi import HTTPException, status


class SeriesAlreadyExistsException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Series already exists',
        *args, **kwargs
    ):
        super().__init__(
            *args, **kwargs,
            status_code=status_code,
            detail=detail
        )
