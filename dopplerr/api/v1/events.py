# coding: utf-8

# Standard Libraries
import logging

# Third Party Libraries
from sanic import Blueprint
from schematics.models import Model
from schematics.types import IntType
from schematics.types import ListType
from schematics.types import ModelType
from schematics.types import StringType

# Dopplerr
from dopplerr.api.add_route import describe_add_route
from dopplerr.db import DopplerrDb

log = logging.getLogger(__name__)


class Event(Model):
    timestamp = StringType()
    type = StringType()
    message = StringType()


class Events(Model):
    events = ListType(ModelType(Event))


class RecentSerie(Model):
    added_timestamp = StringType()
    series_title = StringType()
    season_number = IntType()
    episode_number = IntType()
    episode_title = StringType()
    quality = StringType()
    video_languages = IntType(required=False)
    subtitle_language = StringType()


class RecentSeries(Model):
    events = ListType(ModelType(RecentSerie))


bp = Blueprint('events', url_prefix="/api/v1/recent")


@describe_add_route(bp, paths="/events/{num}", methods="GET")
async def recent_events_num(num: int = 10) -> Events:
    num = int(num)
    if num > 100:
        num = 100
    res = {"events": DopplerrDb().get_recent_events(num)}
    return res


@describe_add_route(bp, paths="/events/", methods="GET")
async def recent_events_10() -> Events:
    res = {"events": DopplerrDb().get_recent_events(10)}
    return res


@describe_add_route(bp, paths="/series/{num}", methods="GET")
async def recent_fetched_series_num(num: int = 10) -> RecentSeries:
    num = int(num)
    if num > 100:
        num = 100
    res = {"events": DopplerrDb().get_last_fetched_series(num)}
    return res
