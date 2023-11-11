from typing import Optional

from pydantic import BaseModel, Field


class PaginationBase(BaseModel):
    page_size: Optional[int] = Field(30, gt=0)
    page: Optional[int] = Field(1, gt=0)

    @property
    def skip(self):
        return (self.page - 1) * self.page_size

class UserPagination(PaginationBase):
    page_size: Optional[int] = Field(30, lt=50, gt=0)

class Pagination(BaseModel):
    total: int
