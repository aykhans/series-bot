from typing import Annotated, Optional

from pydantic import BaseModel, Field

PageSize = Annotated[
    int,
    Field(30, gt=0)
]
Page = Annotated[
    int,
    Field(1, gt=0)
]
Total = Annotated[
    int,
    Field()
]


class PaginationBase(BaseModel):
    page_size: Optional[PageSize] = Field(30, gt=0, lt=50)
    page: Optional[Page] = 1

    @property
    def skip(self):
        return (self.page - 1) * self.page_size


class UserPagination(PaginationBase):
    ...


class SeriesPagination(PaginationBase):
    page_size: Optional[PageSize] = Field(30, gt=0, lt=50)


class Pagination(BaseModel):
    total: Total
    page: Page
