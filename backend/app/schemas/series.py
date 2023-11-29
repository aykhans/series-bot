from typing import Annotated, Optional

from pydantic import BaseModel, Field, PastDate

from app.schemas import base, pagination
from app.schemas import user as user_schemas

Title = Annotated[
    str,
    Field(None, max_length=255)
]
WatchedSeason = Annotated[
    int,
    Field(None, gt=0, le=32767)
]
WatchedEpisode = Annotated[
    int,
    Field(None, gt=0, le=32767)
]
LastSeason = Annotated[
    int,
    Field(None, gt=0, le=32767)
]
LastEpisode = Annotated[
    int,
    Field(None, gt=0, le=32767)
]
UnwatchedEpisodesCount = Annotated[
    int,
    Field(0, ge=0, le=32767)
]


class SeriesBase(BaseModel):
    title: Optional[Title] = None
    watched_season: Optional[WatchedSeason] = None
    watched_episode: Optional[WatchedEpisode] = None
    last_season: Optional[LastSeason] = None
    last_episode: Optional[LastEpisode] = None
    unwatched_episodes_count: Optional[UnwatchedEpisodesCount] = 0


class SeriesCreate(SeriesBase):
    title: Title = Field(..., max_length=255)
    watched_season: WatchedSeason = Field(..., gt=0, le=32767)
    watched_episode: WatchedEpisode = Field(..., gt=0, le=32767)
    last_season: LastSeason = Field(..., gt=0, le=32767)
    last_episode: LastEpisode = Field(..., gt=0, le=32767)
    unwatched_episodes_count: UnwatchedEpisodesCount = Field(
        0, ge=0, le=32767
    )


class SeriesUpdate(BaseModel):
    title: Optional[Title] = None
    watched_season: Optional[WatchedSeason] = None
    watched_episode: Optional[WatchedEpisode] = None


class SeriesUpdateAdmin(SeriesUpdate):
    title: Optional[Title] = None
    watched_season: Optional[WatchedSeason] = None
    watched_episode: Optional[WatchedEpisode] = None
    last_season: Optional[LastSeason] = None
    last_episode: Optional[LastEpisode] = None
    unwatched_episodes_count: Optional[UnwatchedEpisodesCount] = 0


class Series(SeriesBase):
    created_at: Optional[base.CreatedAt] = None
    uuid: Optional[base.UUID4] = None

    class Config:
        from_attributes = True


class SeriesUser(Series):
    user: Optional[user_schemas.UserInSeries] = None


class SeriesReduced(BaseModel):
    title: Optional[Title] = None
    unwatched_episodes_count: Optional[UnwatchedEpisodesCount] = 0
    created_at: Optional[base.CreatedAt] = None
    uuid: Optional[base.UUID4] = None

    class Config:
        from_attributes = True


class SeriesUserReduced(SeriesReduced):
    user: Optional[user_schemas.UserInSeries] = None


class SeriesListAdmin(BaseModel):
    series: list[SeriesUserReduced]
    pagination: pagination.Pagination


class SeriesFilterAdmin(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    created_at_start: Optional[PastDate] = None
    created_at_end: Optional[PastDate] = None
