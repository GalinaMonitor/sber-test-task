from datetime import datetime

from starlette.requests import Request

from src.schemas import DatetimeQueryParams


def parse_timestamp_query_params(request: Request) -> DatetimeQueryParams:
    dp = DatetimeQueryParams()
    query_params = request.query_params
    if "from" in query_params:
        try:
            dp.from_timestamp = datetime.fromtimestamp(float(query_params["from"]))
        except Exception:
            pass
    if "to" in query_params:
        try:
            dp.to_timestamp = datetime.fromtimestamp(float(query_params["to"]))
        except Exception:
            pass
    return dp
